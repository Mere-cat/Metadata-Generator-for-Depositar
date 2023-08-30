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

You can try this feature with your won data in this page. 

Fulfill the cell below and run it to see the result:
* `title`: the title of your dataset
* `description`: description of your dataset
* `resource_names`: file names in your dataset
* `resource_descriptions`: the description of files in your dataset
* `organization_title`: the tilte of the affiliatedorganization 
* `organization_description`: the description of the affiliatedorganization 

```{warning} Notice
At least one of the fields should be completed. Leaving all of them empty is not permissible.
```

```{code-cell} ipython3
from IPython.display import display
import ipywidgets as widgets

button = widgets.Button(description="Click Me!")
output = widgets.Output()

display(button, output)

def on_button_clicked(b):
    with output:
        print("Button clicked.")

button.on_click(on_button_clicked)
```

```{code-cell} ipython3
:tags: [remove-output, hide-input]

# Packages Import ============================================================
import requests

# Import model
# from transformers import (
#    BertTokenizerFast,
#    AutoModelForTokenClassification,
# )
# tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
# model = AutoModelForTokenClassification.from_pretrained('ckiplab/bert-tiny-chinese-ner')

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

    if all(item != "" for item in input_list):
        print("-1")
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

```{code-cell} ipython3
output(result)
```
