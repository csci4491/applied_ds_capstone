# Phase 3 

## Main Research Question

How has collaboration in scientific research changed across arXiv fields over time?

## 1. Has the average size of research teams changed over time across different arXiv fields?

### What I Have Done

- Counted authors per paper and compared yearly mean and median team sizes from 1992 to 2025.
- Compared average team sizes in 1996–2010 and 2011–2025 across the eight fields with the most papers.
- Extended Question: Do the four selected fields still show growth in average team size when we compare older and newer papers on similar topics?
- Selected astrophysics, physics, computer science, and condensed matter for a follow-up based on the team-size growth chart.
- Sampled 125 papers per field per period, for 1,000 papers total.
- Used SBERT to turn titles and abstracts into embedding vectors. Split long text into chunks and averaged their vectors.
- Matched older and newer papers within each field by text similarity. Kept the closest 60% of pairs, giving 75 pairs per field.
- Compared average author counts across the matched papers and all sampled papers.

### Results

- The overall average rose from about 2.2 authors per paper in 1992 to 7.1 in 2025.
- The SBERT comparison gave the following changes in average authors per paper from 1996–2010 to 2011–2025.

| Field | All Sampled Papers | Topic-Matched Papers |
| --- | ---: | ---: |
| Astrophysics | +1.17 | −0.27 |
| Physics | +0.50 | −1.08 |
| Computer science | +1.31 | +0.80 |
| Condensed matter | +0.16 | −0.07 |

- Computer science showed an increase after topic matching. The other three fields showed decreases in this matched sample.


## 2. Has the amount of cross-field collaboration increased over time?

### Work Completed

- Used category cross-listings to identify papers spanning more than one broad arXiv field.
- Compared cross-field percentages over time and across the six largest fields.
- Excluded field-year groups with fewer than 100 papers from the field-level comparison.

### Current Findings

- Cross-field activity peaked around 2020 and then declined.
- Trends varied across fields.
- Category cross-listings describe the fields covered by a paper. Measuring individual authors’ backgrounds would require additional analysis.

### Phase 3 Analysis

- Sample papers from several major arXiv fields.
- Use titles and abstracts to create SBERT document embeddings.
- Use chunking for texts that exceed the model input length and average the chunk embeddings.
- Cluster the paper embeddings to identify semantic research groups.
- Compare the embedding-based clusters with the official arXiv broad-field labels.
- Use the results to evaluate whether the category-based definition of cross-field research should be refined.

## 3. Are researchers increasingly collaborating with authors whose research interests differ from their own?

### Current Status

- Set up the notebook and data-loading steps.
- The coauthor topic-distance analysis and results are pending.
