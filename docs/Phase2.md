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

See if researchers increasingly work with people whose research backgrounds are different from their own.

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
