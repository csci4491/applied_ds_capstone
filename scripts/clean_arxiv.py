#!/usr/bin/env python3
"""Download, clean, and sample arXiv metadata by year and primary category."""

from __future__ import annotations

import argparse
import errno
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FULL_RAW_FILE = PROJECT_ROOT / "data" / "raw" / "arxiv-metadata-oai-snapshot.zip"
FULL_CLEAN_FILE = PROJECT_ROOT / "data" / "processed" / "arxiv_metadata_clean.csv"

KAGGLE_URL = "https://www.kaggle.com/api/v1/datasets/download/Cornell-University/arxiv"

KEEP_COLUMNS = [
    "paper_id",
    "title",
    "abstract",
    "submitted_year",
    "submitted_date",
    "categories",
    "primary_category",
    "authors",
    "doi",
    "journal_ref",
    "license",
    "update_date",
]

IMPORTANT_COLUMNS = ["paper_id", "title", "abstract", "submitted_year", "categories", "authors"]
PAPERS_PER_GROUP = 1_000
SAMPLE_GROUP_COLUMNS = ["submitted_year", "primary_category"]
RANDOM_SEED = 42


def clean_text(value) -> str:
    """Turn missing values into blanks and collapse extra spaces."""

    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return " ".join(str(value).split())


def pick_first(row, names: list[str]):
    """Pick the first useful value from a row."""

    for name in names:
        value = row.get(name, "")
        if clean_text(value):
            return value
    return ""


def download_full_snapshot(output_file: Path, force: bool = False) -> None:
    """Download the full Kaggle arXiv metadata snapshot."""

    output_file.parent.mkdir(parents=True, exist_ok=True)
    if output_file.exists() and not force:
        print(f"Using existing full snapshot: {output_file}")
        return

    partial_file = output_file.with_suffix(output_file.suffix + ".partial")

    with requests.get(KAGGLE_URL, stream=True, timeout=60) as response:
        response.raise_for_status()
        total_bytes = int(response.headers.get("content-length", 0))
        downloaded_bytes = 0

        with partial_file.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                output.write(chunk)
                downloaded_bytes += len(chunk)

                downloaded_mb = downloaded_bytes / 1_000_000
                if total_bytes:
                    total_mb = total_bytes / 1_000_000
                    print(f"\rDownloaded {downloaded_mb:.1f} of {total_mb:.1f} MB", end="")
                else:
                    print(f"\rDownloaded {downloaded_mb:.1f} MB", end="")

    print()
    partial_file.replace(output_file)
    print(f"Saved full snapshot to {output_file}")


def read_raw_metadata(raw_file: Path, chunksize: int):
    """Read a JSONL file or the Kaggle zip file in small pieces."""

    if raw_file.suffix == ".zip":
        with zipfile.ZipFile(raw_file) as archive:
            json_files = [name for name in archive.namelist() if name.endswith(".json")]
            if not json_files:
                raise FileNotFoundError(f"No JSON file found inside {raw_file}")

            with archive.open(json_files[0]) as metadata_file:
                yield from pd.read_json(metadata_file, lines=True, chunksize=chunksize)
    else:
        yield from pd.read_json(raw_file, lines=True, chunksize=chunksize)


def submitted_date(row) -> str:
    """Use the first version date when available; otherwise use a simple date field."""

    versions = row.get("versions", "")
    if isinstance(versions, list) and versions:
        first_version = versions[0]
        if isinstance(first_version, dict):
            return clean_text(first_version.get("created", ""))

    return clean_text(pick_first(row, ["created", "published", "updated", "update_date"]))


def authors(row) -> str:
    """Use the author string when available; otherwise build names from parsed authors."""

    author_text = clean_text(row.get("authors", ""))
    if author_text:
        return author_text

    parsed_authors = row.get("authors_parsed", "")
    if not isinstance(parsed_authors, list):
        return ""

    names = []
    for author in parsed_authors:
        if not isinstance(author, list):
            continue

        last_name = clean_text(author[0]) if len(author) > 0 else ""
        first_name = clean_text(author[1]) if len(author) > 1 else ""
        full_name = clean_text(f"{first_name} {last_name}")
        if full_name:
            names.append(full_name)

    return ", ".join(names)


def prepare_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Select the columns we need and make them easier to analyze."""

    clean = pd.DataFrame()

    clean["paper_id"] = chunk.apply(
        lambda row: clean_text(pick_first(row, ["id", "paper_id", "identifier"])),
        axis=1,
    )
    clean["paper_id"] = clean["paper_id"].str.replace(r"v\d+$", "", regex=True)
    clean["paper_id"] = clean["paper_id"].str.replace("oai:arXiv.org:", "", regex=False)

    clean["title"] = chunk.apply(lambda row: clean_text(row.get("title", "")), axis=1)
    clean["abstract"] = chunk.apply(
        lambda row: clean_text(pick_first(row, ["abstract", "summary"])),
        axis=1,
    )
    clean["categories"] = chunk.apply(lambda row: clean_text(row.get("categories", "")), axis=1)
    clean["primary_category"] = clean["categories"].str.split().str[0].fillna("")
    clean["authors"] = chunk.apply(authors, axis=1)
    clean["doi"] = chunk.apply(lambda row: clean_text(row.get("doi", "")), axis=1)
    clean["journal_ref"] = chunk.apply(
        lambda row: clean_text(pick_first(row, ["journal-ref", "journal_ref"])),
        axis=1,
    )
    clean["license"] = chunk.apply(lambda row: clean_text(row.get("license", "")), axis=1)
    clean["update_date"] = chunk.apply(
        lambda row: clean_text(pick_first(row, ["update_date", "updated"])),
        axis=1,
    )

    date_text = chunk.apply(submitted_date, axis=1)
    try:
        dates = pd.to_datetime(date_text, errors="coerce", utc=True, format="mixed")
    except TypeError:
        dates = pd.to_datetime(date_text, errors="coerce", utc=True)

    clean["submitted_date"] = dates.dt.strftime("%Y-%m-%d").fillna("")
    clean["submitted_year"] = dates.dt.year.astype("Int64").astype(str).replace("<NA>", "")

    return clean[KEEP_COLUMNS]


def clean_metadata(
    raw_file: Path,
    clean_file: Path,
    chunksize: int = 100_000,
    papers_per_group: int = PAPERS_PER_GROUP,
    random_seed: int = RANDOM_SEED,
) -> None:
    """Sample each year/category pair with complete essential fields."""

    if chunksize <= 0 or papers_per_group <= 0:
        raise ValueError("chunksize and papers_per_group must be positive.")

    clean_file.parent.mkdir(parents=True, exist_ok=True)

    seen_ids = set()
    random_generator = np.random.default_rng(random_seed)
    group_samples = {}
    summary = {
        "raw_records": 0,
        "eligible_records": 0,
        "clean_records": 0,
        "dropped_duplicates": 0,
        "dropped_missing_important_values": 0,
        "dropped_by_group_cap": 0,
        "papers_per_group": papers_per_group,
        "sampling_group_columns": SAMPLE_GROUP_COLUMNS,
        "random_seed": random_seed,
        "records_per_year": {},
        "records_per_year_category": {},
        "important_columns": IMPORTANT_COLUMNS,
        "kept_columns": KEEP_COLUMNS,
    }

    print(f"Sampling up to {papers_per_group:,} papers per submission year and primary category.")

    for raw_chunk in read_raw_metadata(raw_file, chunksize):
        summary["raw_records"] += len(raw_chunk)
        clean_chunk = prepare_chunk(raw_chunk)

        before_missing_drop = len(clean_chunk)
        required_values = clean_chunk[IMPORTANT_COLUMNS]
        missing_values = required_values.isna() | required_values.eq("")
        clean_chunk = clean_chunk[~missing_values.any(axis=1)]
        summary["dropped_missing_important_values"] += before_missing_drop - len(clean_chunk)

        before_duplicate_drop = len(clean_chunk)
        clean_chunk = clean_chunk.drop_duplicates(subset="paper_id", keep="first")
        clean_chunk = clean_chunk[~clean_chunk["paper_id"].isin(seen_ids)]
        summary["dropped_duplicates"] += before_duplicate_drop - len(clean_chunk)

        seen_ids.update(clean_chunk["paper_id"])
        summary["eligible_records"] += len(clean_chunk)

        # Keep the smallest random priorities to sample across every raw chunk.
        clean_chunk = clean_chunk.copy()
        clean_chunk["_sample_priority"] = random_generator.random(len(clean_chunk))
        for group_key, group_chunk in clean_chunk.groupby(SAMPLE_GROUP_COLUMNS, sort=True):
            if group_key in group_samples:
                group_chunk = pd.concat([group_samples[group_key], group_chunk], ignore_index=True)
            group_samples[group_key] = group_chunk.nsmallest(papers_per_group, "_sample_priority")

        sampled_records = sum(len(sample) for sample in group_samples.values())
        print(f"Processed {summary['raw_records']:,} raw papers; retaining {sampled_records:,} papers.")

    summary_file = clean_file.with_suffix(clean_file.suffix + ".summary.json")
    partial_file = clean_file.with_suffix(clean_file.suffix + ".partial")
    partial_summary_file = summary_file.with_suffix(summary_file.suffix + ".partial")

    try:
        with partial_file.open("w", encoding="utf-8", newline="") as output:
            pd.DataFrame(columns=KEEP_COLUMNS).to_csv(output, index=False)
            for year, category in sorted(group_samples):
                group_sample = group_samples[(year, category)].drop(columns="_sample_priority")
                group_sample.to_csv(output, header=False, index=False)
                group_count = len(group_sample)
                summary["records_per_year"][year] = summary["records_per_year"].get(year, 0) + group_count
                summary["records_per_year_category"].setdefault(year, {})[category] = group_count
                summary["clean_records"] += group_count

        summary["dropped_by_group_cap"] = summary["eligible_records"] - summary["clean_records"]
        summary["clean_file_bytes"] = partial_file.stat().st_size
        partial_summary_file.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

        # The summary marks completion only after the full CSV is in place.
        summary_file.unlink(missing_ok=True)
        partial_file.replace(clean_file)
        partial_summary_file.replace(summary_file)
    except OSError as error:
        if error.errno == errno.ENOSPC:
            raise OSError(
                errno.ENOSPC,
                f"Not enough disk space to save the year/category sample in {clean_file.parent}. "
                "Free disk space and rerun the cleaner.",
            ) from error
        raise
    finally:
        partial_file.unlink(missing_ok=True)
        partial_summary_file.unlink(missing_ok=True)

    print(f"Saved clean data to {clean_file}")
    print(f"Saved cleaning summary to {summary_file}")
    display_summary = {
        key: value for key, value in summary.items() if key != "records_per_year_category"
    }
    print(json.dumps(display_summary, indent=2))


def clean_file_is_current(
    clean_file: Path,
    papers_per_group: int = PAPERS_PER_GROUP,
    random_seed: int = RANDOM_SEED,
) -> bool:
    """Check that a completed CSV matches the current sampling and cleaning settings."""

    summary_file = clean_file.with_suffix(clean_file.suffix + ".summary.json")
    try:
        summary = json.loads(summary_file.read_text(encoding="utf-8"))
        return (
            isinstance(summary, dict)
            and summary.get("papers_per_group") == papers_per_group
            and summary.get("sampling_group_columns") == SAMPLE_GROUP_COLUMNS
            and summary.get("random_seed") == random_seed
            and summary.get("important_columns") == IMPORTANT_COLUMNS
            and summary.get("kept_columns") == KEEP_COLUMNS
            and summary.get("clean_file_bytes") == clean_file.stat().st_size
        )
    except (OSError, ValueError):
        return False


def run_full(
    raw_file: Path = FULL_RAW_FILE,
    clean_file: Path = FULL_CLEAN_FILE,
    force_download: bool = False,
    chunksize: int = 100_000,
    papers_per_group: int = PAPERS_PER_GROUP,
    random_seed: int = RANDOM_SEED,
) -> None:
    """Download the snapshot, then clean and sample each year/category pair."""

    download_full_snapshot(Path(raw_file), force=force_download)
    clean_metadata(
        Path(raw_file),
        Path(clean_file),
        chunksize=chunksize,
        papers_per_group=papers_per_group,
        random_seed=random_seed,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download, clean, and randomly sample arXiv metadata by year and primary category."
    )
    parser.add_argument("--raw-output", type=Path, default=FULL_RAW_FILE)
    parser.add_argument("--clean-output", type=Path, default=FULL_CLEAN_FILE)
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--chunksize", type=int, default=100_000)
    parser.add_argument(
        "--papers-per-group",
        type=int,
        default=PAPERS_PER_GROUP,
        help="Maximum papers kept per year/primary-category pair (default: 1,000).",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=RANDOM_SEED,
        help="Random seed for reproducible yearly sampling (default: 42).",
    )

    args = parser.parse_args()
    if args.chunksize <= 0 or args.papers_per_group <= 0:
        parser.error("--chunksize and --papers-per-group must be positive.")

    run_full(
        raw_file=args.raw_output,
        clean_file=args.clean_output,
        force_download=args.force_download,
        chunksize=args.chunksize,
        papers_per_group=args.papers_per_group,
        random_seed=args.random_seed,
    )


if __name__ == "__main__":
    main()
