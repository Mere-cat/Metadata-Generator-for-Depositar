---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.1
kernelspec:
  display_name: 2023-sinica-intern
  language: python
  name: python3
---

# Recommend a Key
In order to auto recommend wikidata keywords to users, here're two things we need to achieve. 

First, we'll tokenization the input string and find out which ones can be the keyword for the sentence. We'll introduce a NLP tool develop by the ckiplab of Academic Sinica called ckip-tagger. Within its help, we can do NER to the input stence and hence obtain keywords which are potentially be wikidata keywords.

Second, after getting a list of potential words, we'll check if they are wikidata keyword. Here we send request through the wikidata API, to search if the keyword is recorded in wikidata.

Finishing the two step works, we'll finally obtain a list of keywords in the input string, and also are wikidata keywords. That result is what we recommend to the users.

+++

## Load Data
Before we starting to try this feature, we'll load the input data from Depositar.

We previously downloaded metadata of datasets through its API, and store it as file 'datasets.json.' Since we'll only use it as anexample input, here's no need to update this file, and the code for calling the API is not include in this notebook.

```{code-cell} ipython3
import json
import pandas as pd
# function definition
def get_metadata(data, data_index):
    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)

        title = data[data_index]['title']
        notes = data[data_index]['notes']

        resources_names = []
        resources_desps = []
        for item in data[data_index]['resources']:
            if 'name' in item:
                resources_names.append(item['name'])
                resources_desps.append(item['description'])

        organization_title = data[data_index]['organization']['title']
        organization_desp = data[data_index]['organization']['description']

    df = pd.DataFrame({
        'Title': [title],
        'Notes': [notes],
        'Resource Names': [resources_names],
        'Resource Descriptions': [resources_desps],
        'Organization Title': [organization_title],
        'Organization Description': [organization_desp]
    })

    return df
```

We can chose one datasets by its index:(from 0 to 9)

```{code-cell} ipython3
dataset_idx = 9
```

```{code-cell} ipython3
if(dataset_idx < 100 and dataset_idx > 1):
    df = get_metadata('datasets_10.json', dataset_idx)
    input_list = []
    #data_string = df.to_string(index=False, header=False)
    for entity in df:
        print(entity, ':', df[entity][0])
        input_list.append(df[entity][0])
else:
    print('input number in the interval from 0 to 99')
```

## Step 1: NER task

```{code-cell} ipython3
# Import model
from transformers import (
   BertTokenizerFast,
   AutoModelForMaskedLM,
   AutoModelForCausalLM,
   AutoModelForTokenClassification,
)
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
model = AutoModelForTokenClassification.from_pretrained('ckiplab/bert-tiny-chinese-ner')

# NLP task model
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
ws_driver  = CkipWordSegmenter(model="bert-base")
pos_driver = CkipPosTagger(model="bert-base")
ner_driver = CkipNerChunker(model="bert-base")
```

```{code-cell} ipython3
# NER task
import pandas as pd
import json
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

ner = ner_driver(input_list)
```

```{code-cell} ipython3
# Show results
avoid_class = ['QUANTITY', 'CARDINAL', 'DATE']
keyword_map = {}
for sentence_ner in ner:
   for entity in sentence_ner:
      if(entity[1] in avoid_class):
        continue
      keyword_map[entity[0]] = entity[1]

for key, value in keyword_map.items():
  print(key, ':', value)
```

## Step 2: Searching through Wikidata API

```{code-cell} ipython3
import requests

def wiki_search(search_term):
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search={search_term}&language=zh"

    response = requests.get(url)
    data = response.json()

    # 處理回傳的數據
    if "search" in data:
        for result in data["search"]:
            qid = result["id"]
            label = result["label"]
            description = result.get("description", "No description available")
            print(f"QID: {qid}, Label: {label}, Description: {description}")
    else:
        print("No results found.")
```

```{code-cell} ipython3
for item in keyword_map:
    print(item)
    wiki_search(item)
    print('-------------------------------------------')
```
