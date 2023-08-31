# Metadata Generator
Depositar is an online repository dedicated to housing research data curated by Academia Sinica, Taiwan. As is the case with any data repository, the role of metadata cannot be understated—it serves as the cornerstone when users embark on the quest to discover datasets that align with their specific requirements.

Nonetheless, the task of accurately and comprehensively filling in metadata remains a formidable challenge for dataset providers. When users upload their datasets, they often find themselves uncertain about which Wikidata keywords would best suit their content. Moreover, grappling with the intricacies of spatial coverage can be a considerably intricate endeavor.

Thus, this project aims to develop a metadata generator. Based on textual dataset information such as descriptions or source file names, this program will automatically recommend to users certain Wikidata keywords and spatial coverage information that will assist them in completing the metadata for their dataset.

## Usage

### 📘 Building the book

If you'd like to develop and/or build the metadata_generator book, you should:

1. Clone this repository
2. Run `pip install -r requirements.txt` (it is recommended you do this within a virtual environment)
3. (Optional) Edit the books source files located in the `metadata_generator/` directory
4. Run `make` to build the book
5. Run `make clean` to delete the book

A fully-rendered HTML version of the book will be built in `metadata_generator/_build/html/`.

### 🔧 Using only the function

If you'd only like to use the python function to obtain the result metadata, you can simply download the code available in `metadata_generator/code/metadata_generator.py`.

Here are a few basic usage examples:
#### Creating a Dataset Object and Initializing It
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

#### Generating the Metadata for the Current Dataset Object
```python
# generate recommended wikidata key words and geographic information
your_dataset_obj.gen_meta()
```
#### Access to the Result
The generated Wikidata keywords are stored within `your_dataset_obj.wiki_keyword_list`, while the corresponding geographic information resides in `your_dataset_obj.geoInfo_list`. Both of these structures utilize a list format, with each element representing a recommended metadata entry.

### 🚀 Hosting the book

Please see the [Jupyter Book documentation](https://jupyterbook.org/publish/web.html) to discover options for deploying a book online using services such as GitHub, GitLab, or Netlify.

For GitHub and GitLab deployment specifically, the [cookiecutter-jupyter-book](https://github.com/executablebooks/cookiecutter-jupyter-book) includes templates for, and information about, optional continuous integration (CI) workflow files to help easily and automatically deploy books online with GitHub or GitLab. For example, if you chose `github` for the `include_ci` cookiecutter option, your book template was created with a GitHub actions workflow file that, once pushed to GitHub, automatically renders and pushes your book to the `gh-pages` branch of your repo and hosts it on GitHub Pages when a push or pull request is made to the main branch.

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/dquqb/metadata_generator/graphs/contributors).

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
