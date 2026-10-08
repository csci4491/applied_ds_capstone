# Project Proposal (Phase 1)

## Description

This project will study how scientific collaboration has changed across arXiv fields over time. Are researchers collaborating with people from different research areas more than they used to? We will look at whether research teams are becoming larger and whether researchers are increasingly working with people from different research areas. Using author information, paper categories, titles, abstracts, and document embeddings.
	
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

## List of relevant papers

- [Collaboration and Topic Switches in Science](https://www.nature.com/articles/s41598-024-51606-6)
    The relationship between collaboration and changes in researchers' topics
- [On time-varying collaboration networks](https://www.sciencedirect.com/science/article/abs/pii/S1751157712001162)
    How scientific collaboration networks change over time (arXiv data)


## Team Responsibilities

- Mira: download the arXiv metadata, select needed variables, clean the dataset, and work on the team-size question (subquestion1).
- Guy: work on the cross-field collaboration question (subquestion2).
- Ibrahim: work on the author research-topic distance question (subquestion3).
