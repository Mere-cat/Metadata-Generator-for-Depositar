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

# Recommend Keywords
In order to auto recommend wikidata keywords to users, here're two things we need to achieve. 

First, we'll tokenization the input string and find out which ones can be the keyword for the sentence. We'll introduce a NLP tool develop by the ckiplab of Academic Sinica called ckip-tagger. Within its help, we can do NER to the input stence and hence obtain keywords which are potentially be wikidata keywords.

Second, after getting a list of potential words, we'll check if they are wikidata keyword. Here we send request through the wikidata API, to search if the keyword is recorded in wikidata.

Finishing the two step works, we'll finally obtain a list of keywords in the input string, and also are wikidata keywords. That result is what we recommend to the users.

:::{tip}
You can choose a particular dataset by its index and explore the geographic information recommendations provided. To proceed, follow these steps:
1. Click on the "rocket icon" located in the top-right corner.
2. Select the option labeled `Live Code` from the menu.
3. Once the environment is launched, you'll be able to manually execute **each** code cell.

For any hidden code cells, simply click on `Show code cell source` and subsequently click `run` within each respective cell section.
:::

+++

## Load Data
Before we start trying this feature, we'll load the input data from Depositar.

Previously, we downloaded metadata of datasets from Depositar through its API, randomly selected 10 datasets, and stored them in a file named `example_depositar_data.json` in the `assets/` directory. Since we'll only use this as an example input, there's no need to update this file, and the code for calling the API is not included in this notebook.

+++

### Obtain metadata from datasets

```{code-cell} ipython3
:tags: [hide-input, hide-output]

import json
import pandas as pd
import warnings

# function definition
def get_metadata(data_path, data_index):
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        data = pd.read_json(data_path)

        title = data.loc[data_index, 'title']
        notes = data.loc[data_index, 'notes']

        resources_names = []
        resources_desps = []
        for item in data.loc[data_index, 'resources']:
            if 'name' in item:
                resources_names.append(item['name'])
                resources_desps.append(item['description'])

        organization_title = data.loc[data_index, 'organization']['title']
        organization_desp = data.loc[data_index, 'organization']['description']

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

We can chose one datasets by its index:

```{code-cell} ipython3
dataset_idx = 6
```

✨ You can change the index to see the result of different dataset. (from 0 to 99)

+++

### Show dataset content
Below displays the information of our selected dataset:

```{code-cell} ipython3
:tags: [hide-input]

if(dataset_idx < 100 and dataset_idx > 1):
    data_path = 'https://mere-cat.github.io/Metadata-Generator-for-Depositar/assets/example_depositar_data.json'
    df = get_metadata(data_path, dataset_idx)
    input_list = []
    for entity in df:
        print(entity, ':', df[entity][0])
        input_list.append(df[entity][0])
else:
    print('input number in the interval from 0 to 99')
```

## Step 1: NER task

+++

### Import Models
Here we import the transformer models, and do the NER to our input data.

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# NLP task model
from ckip_transformers.nlp import CkipNerChunker
ner_driver = CkipNerChunker(model="bert-base")
```

### NER task

```{code-cell} ipython3
:tags: [hide-input, remove-output]

# NER task
ner = ner_driver(input_list)
```

### Output
Below is the output list of the NER result:

```{code-cell} ipython3
:tags: [hide-input]

# Show results
avoid_class = ['QUANTITY', 'CARDINAL', 'DATE', 'ORDINAL']
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
After searching each potential word obtained in previous step, now we are going to check if each word is a wikidata keyword.

+++

### Request Wikidata API

```{code-cell} ipython3
:tags: [hide-input]

import requests

def wiki_search(search_term):
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search={search_term}&language=zh"

    response = requests.get(url)
    data = response.json()

    # organize the response
    if "search" in data:
        for result in data["search"]:
            qid = result["id"]
            label = result["label"]
            description = result.get("description", "No description available")
            print(f"QID: {qid}, Label: {label}, Description: {description}")
    else:
        print("No results found.")
```

### Output

+++

Here is the output of searching result:

```{code-cell} ipython3
:tags: [hide-input]

for item in keyword_map:
    print(item)
    wiki_search(item)
    print('-------------------------------------------')
```
