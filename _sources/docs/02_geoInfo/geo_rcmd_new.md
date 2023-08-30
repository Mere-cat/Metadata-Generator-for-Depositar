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

# Intro to GeoInfo Generator

+++

To automatically recommend locations along with their geographic information to users, we need to accomplish two key objectives.

To begin with, we will tokenize the input string to identify potential keywords for the given input. To achieve this, we will utilize a Natural Language Processing (NLP) tool developed by the ckiplab at Academic Sinica, called `ckiplab/bert-base-chinese-ner`. With the assistance of this tool, we can perform Named Entity Recognition (NER) on the input sentence, thereby extracting keywords that could potentially match Wikidata keywords.

Subsequently, once we have compiled a list of potential words, our next step involves verifying whether these words correspond to actual locations across the globe. For this purpose, we will make use of the Nominatim API to retrieve search results for the list of potential keywords.

Upon successfully completing these two steps, we will have a comprehensive compilation of locations and their associated geographic information. To provide users with an interactive preview of OpenStreetMap (OSM), we have implemented [folium](http://python-visualization.github.io/folium/index.html). This enables users to select a location from the aforementioned list, input its geographic details, and visualize it on the map.

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

## Step 2: Searching through OSM Nominatim API
After searching each potential word obtained in previous step, now we are going to check if each word is a wikidata keyword.

### Requeest Nominatim API

```{code-cell} ipython3
:tags: [hide-input]

import requests

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
```

### OSM Search Result
Now, we'll obtain a list of possible location for each named entity.

```{code-cell} ipython3
for item in keyword_map:
    result = search_osm_place(item)
    if result:
        print(f"OSM result for {item} is:")
        for place in result:
            print("📍", place["display_name"])
            print(str(place["geojson"]).replace("'", "\""))
        print('-------------------------------------------')
    else:
            print("No geoInfo provided.")
```

### Input geoJSON
Select one of the location above, copy the geoJSON and paste to the below cell:

```{code-cell} ipython3
geoInfo = ''
```

### Preview the Location in OSM
Now, we can see the location you previously chosen displayed below:

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
