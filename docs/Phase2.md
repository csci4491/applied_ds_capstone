# Project Proposal (Phase 2 explore the data)
	
## Main Research Question

How has collaboration in scientific research changed across arXiv fields over time?

## Subquestions

### 1. Has the average size of research teams changed over time across different arXiv fields?

Find whether papers are being written by larger teams than they used to be.

### What I Have Done

- Cleaned the arXiv metadata dataset
- Kept the main fields (paper ID, year, category, title, abstract, authors)
- Remove rows with missing main field values
- Count authors per paper
- Grouped papers by year and broad field ( ex: cs.AI, cs.LG -> cs )
- Created mean/median team-size plots

### Results
- Use 1,669,891 arXiv papers from 1992 to 2026
- Average team size increased from about 2.2 to 6.3 authors per paper

### What Is Going Well
- The dataset is large enough to show long-term trends
- The cleaning process works well
- 1st subquestion has a clear direction
- Mean and median help show the effect of very large teams

### Problems or Challenges
- Some fields, especially physics, have very large collaborations that raise the average
- The 2026 data is incomplete
- The next questions are more complex

### Plan Before Next Check-In (Phase 3 analyze)
- Check team-size trends by field
- Decide how to handle 2026

### 2. Has the amount of cross-field collaboration increased over time?

See if researchers increasingly work with people whose research backgrounds are different from their own.

### 3. Are researchers increasingly collaborating with authors whose research interests are different from their own?

Author Research-Topic Distance




