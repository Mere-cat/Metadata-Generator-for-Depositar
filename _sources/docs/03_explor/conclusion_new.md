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

# Project Result
Now, let's integrate the two aspects of our project. This integration will yield an interactive interface that enables users to input their dataset information. Consequently, they will receive the suggested Wikidata keywords along with the most fitting location that accurately characterizes the dataset.

:::{tip}
You can choose a particular dataset by its index and explore the geographic information recommendations provided. To proceed, follow these steps:
1. Click on the "rocket icon" located in the top-right corner.
2. Select the option labeled `Live Code` from the menu.
3. Once the environment is launched, you'll be able to manually execute **each** code cell.

For any hidden code cells, simply click on `Show code cell source` and subsequently click `run` within each respective cell section.
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
Just expend it and click `run`

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
        
def search_osm_place(query):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "polygon_geojson": "1",  # Request GeoJSON polygons
        "limit": 7
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

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
    
def wiki_output(result):
    if(result == -1):
        print("At least one of the fields should be completed. Leaving all of them empty is not permissible.")
        return
    else:
        for item in result:
            print(item)
            wiki_search(item)
            print('-------------------------------------------')

def geoInfo_output(result):
    if(result == -1):
        print("At least one of the fields should be completed. Leaving all of them empty is not permissible.")
        return
    else:
        for item in result:
            respond = search_osm_place(item)
            if respond:
                print(f"OSM result for {item} is:")
                for place in respond:
                    print("📍", place["display_name"])
                    print(str(place["geojson"]).replace("'", "\""))
                print('-------------------------------------------')
            else:
                    print("No geoInfo provided.")
```

### Input
✨ You can type information of your own dataset here:

```{code-cell} ipython3
title = ''
description = ''
resource_names = []
resource_descriptions = []
organization_title = ""
organization_description = ""

result = gen_keyword(title, description, resource_names, resource_descriptions, organization_title, organization_description)
```

## Result

+++

### Wikidata Keyword Recommendation:

```{code-cell} ipython3
wiki_output(result)
```

### Geographic Information Recommendation:

```{code-cell} ipython3
geoInfo_output(result)
```

#### Preview the Location in OSM

+++

Select one of the location above, copy the geoJSON and paste to the below cell:

```{code-cell} ipython3
geoInfo = ''
```

```{code-cell} ipython3
:tags: [hide-input]

import folium

center_coords = [25.041415686746607, 121.61472689731077]  # Sinica
m = folium.Map(location=center_coords, zoom_start=12)

if(len(geoInfo) == 0):
    print("please paste the geoJSON in the 'geoInfo' string.")
else:
    geojson = eval(geoInfo)
    folium.GeoJson(geojson).add_to(m)
    m.fit_bounds(m.get_bounds())
    display(m)
```
