# Executing with Pure Python
While our Jupyter Book offers an interactive platform for executing this program, please be aware that initiating the environment on myBinder might result in extended loading times owing to the NER model's loading and utilization. 

Furthermore, if you prefer to exclusively implement this feature within your own project, we have also included a Python function. This function can be executed anywhere you require it, offering enhanced flexibility and convenience.

## Acquire the Script
Within our project's GitHub [repo](https://github.com/Mere-cat/Metadata-Generator-for-Depositar/tree/main), you can navigate to `metadata_generator/code/metadata_generator.py` in order to obtain this program.

## Usage

First, you need to create a dataset object and initialize its information:
```python
# fulfill metadata of a dataset 
title = ''
description = ''
resource_names = []
resource_descriptions = []
organization_title = ""
organization_description = ""

# Create a dataset object
your_dataset_obj = dataset(title, description, resource_names, resource_descriptions, organization_title, organization_description)
```

Then, you can execute this line to obtain the generated meatdata:
```python
# generate recommended wikidata key words and geographic information
your_dataset_obj.gen_meta()
```

The generated Wikidata keywords are stored within `your_dataset_obj.wiki_keyword_list`, while the corresponding geographic information resides in `your_dataset_obj.geoInfo_list`. Both of these structures utilize a list format, with each element representing a recommended metadata entry.