# Intro to Keyword Generator

## Motivation
While uploading dataset to Depositar, find wikidata keyword for a dataset can be trivious and tedious.

In the current Depositar website, users have to fill in wikidata keyword by their own:

```{figure} ../../images/wiki.png
---
name: depositar interface
scale: 60%
---
A screenshot of the Depositar interface for inputting Wikidata keywords
```

Thus, we aims to develop a metadata generator, to help users find the apporporiate wikidata keywords to describe their dataset.

## Method
In this seciton, we provide a 2-step pipeline to achieve the goal:
```{figure} ../../images/wiki_pipeline.png
---
name: depositar interface
---
A pipeline for the keyword generator project
```

### Stpe 1: NER


### Step 2: Wikidata API Search