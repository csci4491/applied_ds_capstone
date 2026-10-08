# Project Proposal (Phase 2)
	
## Main Research Question

How has collaboration in scientific research changed across arXiv fields over time?

## Subquestions

### 1. Has the average size of research teams changed over time across different arXiv fields?

Find whether papers are being written by larger teams than they used to be.

Steps :

- Count the number of authors on each paper.
- Group papers by year and field 
- Plot the results over time (mean/median number of authors)
- Compare earlier and later years to answer (Did team size increase?, Which fields changed the most?, Which fields stayed relatively stable?)


### 2. Has the amount of cross-field collaboration increased over time?

See if research increasingly connects different arXiv fields over time.

### What I Have Done

- Loaded the cleaned arXiv metadata dataset
- Used paper categories to identify broad research fields
- Defined a paper as cross-field when its categories represent more than one broad research field
- Calculated the percentage of cross-field papers by year
- Compared cross-field trends across the six largest arXiv fields
- Removed field-year groups with fewer than 100 papers before interpreting the trends
- Created graphs showing overall and field-specific cross-field trends

### Results

- Cross-field research does not show a steady increase over time
- Cross-field activity reached about 36.9% in 2020 and decreased to about 26.5% in 2025
- Different fields show different trends
- `hep-ph` shows one of the highest cross-field rates among the large fields analyzed
- `math` and `cond-mat` show more gradual changes
- `cs` increased during some periods but declined in recent years

### What Is Going Well

- The category-based method is feasible with the current dataset
- It allows us to compare long-term trends across fields
- The results show clear differences between research fields
- Filtering small field-year groups makes the comparisons more reliable

### Problems or Challenges

- Some early field-year groups contain very few papers and can produce misleading percentages
- We use arXiv category cross-listings as a proxy for cross-field research
- A cross-listed paper does not necessarily prove that the individual authors have different research backgrounds
- We still need to refine how broad fields are defined
- The original embedding approach overlaps with Subquestion 3 and would require more computation

### Plan Before Next Check-In (Phase 3 Analyze)

- Refine and justify the broad-field definitions
- Compare earlier and later periods to measure which fields changed the most
- Investigate which fields are driving the increases and decreases in cross-field research
- Test whether the conclusions remain similar under different field-grouping choices
- Decide whether the category-based approach is sufficient or whether an embedding-based extension adds useful information

Steps :

- Take each paper's title + abstract
- Convert the text into numbers representing the paper's topic (embedding) to find similar papers
- Look at the author's previous papers to find their research area.
- Compare the embeddings of the authors' previous research.
- For papers with multiple authors, calculate the average research difference between the authors.
- Group that measurement by year.
- Plot the results over time 


### 3. Are researchers increasingly collaborating with authors whose research interests are different from their own?

Author Research-Topic Distance

Steps :

- Get each author's previous papers.
- Use the title and abstract of those papers.
- Create embeddings for the papers. (like 2nd sub question)
- Create a research profile for each author by combining the embeddings of that author's previous papers.
- Compare the two authors' profiles using cosine similarity/distance
- For a paper with several authors, calculate the average difference between the authors.
- Group the results by year.
- Compare the trend across fields.
