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
After obtaining the input metadata for the current dataset, we will utilize Named Entity Recognition (NER) on the input data to selectively extract words that could potentially correspond to Wikidata Q-items.

We use the `ckiplab/bert-base-chinese-ner` NLP task model to achieve this goal.

`ckiplab/bert-base-chinese-ner` is a NLP model under the project [**CKIP Transformers**](https://github.com/ckiplab/ckip-transformers), which provides transformer models specifically designed for traditional Chinese.

We chose `ckiplab/bert-base-chinese-ner` due to its high F1 score in NER compared to other models provided by CKIP Lab.

### Step 2: Wikidata API Search
Here, we send a search request through the Wikidata API. By using `action=wbsearchentities`, we can search the Wikidata database using labels and aliases, thus finding the corresponding items that match our input potential keyword.

For more information, check for [Media Wiki help: action=wbsearchentities](https://www.wikidata.org/w/api.php?action=help&modules=wbsearchentities)