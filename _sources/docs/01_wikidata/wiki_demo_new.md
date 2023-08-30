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

# Live Demo

You can try this feature with your own data in this page. 

:::{tip}
You can input the information of your own dataset to try this feature.

First select the "rocket icon" on the right-top, then select `Live Code`. After the launching is done, you can run each code cell manually.

For the hidden code cell, click `Show code cell source` then click `Run` in each cell section.
:::

Here're the information you may input:
* `title`: the title of your dataset
* `description`: description of your dataset
* `resource_names`: file names in your dataset
* `resource_descriptions`: the description of files in your dataset
* `organization_title`: the tilte of the affiliatedorganization 
* `organization_description`: the description of the affiliatedorganization 

```{warning} Notice
At least one of the fields should be completed. Leaving all of them empty is not permissible.
```

+++

## Function Definations
Just expend it and click `Run`

```{code-cell} ipython3
:tags: [remove-output, hide-input]

# Packages Import ============================================================
import requests

# NLP task model
from ckip_transformers.nlp import CkipNerChunker
ner_driver = CkipNerChunker(model="bert-base")

# Function Definstion =========================================================
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

def make_keyword_map(input_list):
    # NER task
    ner = ner_driver(input_list)

    # Build keyword_map to store potential words
    avoid_class = ['QUANTITY', 'CARDINAL', 'DATE', 'ORDINAL']
    keyword_map = {}
    for sentence_ner in ner:
        for entity in sentence_ner:
            if(entity[1] in avoid_class):
                continue
        keyword_map[entity[0]] = entity[1]
    
    return keyword_map

def gen_keyword(title, description, resource_names, resource_descriptions, organization_title, organization_description):
    input_list = [title, description, resource_names, resource_descriptions, organization_title, organization_description]

    if all(not item for item in input_list):
        return -1
    else:
       keyword_map = make_keyword_map(input_list)
       return keyword_map

def output(result):
    if(result == -1):
        print("At least one of the fields should be completed. Leaving all of them empty is not permissible.")
        return
    else:
        for item in result:
            print(item)
            wiki_search(item)
            print('-------------------------------------------')
```

### Input
✨ You can type information of your own dataset here:

```{code-cell} ipython3
:tags: [remove-output]

title = ''
description = ''
resource_names = []
resource_descriptions = []
organization_title = ""
organization_description = ""

result = gen_keyword(title, description, resource_names, resource_descriptions, organization_title, organization_description)
```

### Output
Below's our recomnned wikidata keyword(s) for your dataset:

```{code-cell} ipython3
output(result)
```
