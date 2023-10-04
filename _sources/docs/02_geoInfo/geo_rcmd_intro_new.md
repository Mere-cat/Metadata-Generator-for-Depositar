---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: 2023-sinica-intern
  language: python
  name: python3
---

# Intro to GeoInfo Generator
## Motivation
Despite the fact that Depositar provides a convenient interface that allows users to select points, lines, or areas to describe the spatial aspects of their dataset, drawing a complex boundary such as a city boundary can be challenging. This challenge is amplified, especially for users who are not familiar with geographic information formats like geoJSON.

Below is the interactive map that Depositar apply:

```{code-cell} ipython3
:tags: [remove-input]

import folium
from folium.plugins import Draw

center_coords = [25.041415686746607, 121.61472689731077]  # Sinica

m = folium.Map(location=center_coords, zoom_start=15.5)

# drawing tool
draw = Draw(export=True)
draw.add_to(m)

# display
m
```

Thus, we aims to develop a geographic information generator, to help users find the apporporiate wikidata keywords to describe their dataset.

## Method
In this seciton, we provide a 2-step pipeline to achieve the goal:
```{figure} ../../images/geo_pipeline.png
---
name: depositar interface
---
A pipeline for the keyword generator project

+++

### Stpe 1: NER
After obtaining the input metadata for the current dataset, we will utilize Named Entity Recognition (NER) on the input data to selectively extract words that could potentially correspond to Wikidata Q-items.

To achieve this goal, we will utilize the `ckiplab/bert-base-chinese-ner` NLP task model.

The `ckiplab/bert-base-chinese-ner` model is part of the [**CKIP Transformers**](https://github.com/ckiplab/ckip-transformers) project, which offers transformer models specifically designed for traditional Chinese language processing.

We have selected the `ckiplab/bert-base-chinese-ner` model due to its superior F1 score in NER when compared to other models provided by CKIP Lab.

### Step 2: OSM API Search
After obtaining a list of named entities, we will use the Nominatim API to search for locations that match our input words.

For more information, check for [Nominatim API](https://nominatim.org/release-docs/develop/api/Overview/)
