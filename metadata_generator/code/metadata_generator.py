# Packages Import ============================================================
# Need to import those pasckages and model before using the 
import requests

# NLP task model
from ckip_transformers.nlp import CkipNerChunker
ner_driver = CkipNerChunker(model="bert-base")

# Class Defination ============================================================
class dataset:
    def __init__(self, title, description, resource_names, resource_descriptions, organization_title, organization_description):
        """ Init data in a dataset object

        Args:
            title: the title of your dataset
            decription: description of your dataset
            resource_names: file names in your dataset
            resource_descriptions: the description of files in your dataset
            organization_title: the tilte of the affiliatedorganization
            organization_description: the description of the affiliatedorganization 
        """
        self.title = title
        self.description = description
        self.resource_names = resource_names
        self.resource_descriptions = resource_descriptions
        self.organization_title = organization_title
        self.organization_description = organization_description

        self.wiki_keyword_list = []
        self.geoInfo_list = []
        self.ner_map = {}

    def make_ner_map(self):
        """ Utilize NER to the information in the dataset object and store the result.

        Returns:
            keyword_map: a dictionary of potential keywords. Key is the word itself, and the value is the NER category.
        """
        # prepare data to do NER
        input_list = [self.title, self.description, self.resource_names, self.resource_descriptions, self.organization_title, self.organization_description]
        if all(not item for item in input_list):
            print("At least one of the fields should be completed. Leaving all of them empty is not permissible.")

        # NER task
        ner = ner_driver(input_list)

        # Build ner_map to store potential words
        avoid_class = ['QUANTITY', 'CARDINAL', 'DATE', 'ORDINAL']
        for sentence_ner in ner:
            for entity in sentence_ner:
                if(entity[1] in avoid_class):
                    continue
            self.ner_map[entity[0]] = entity[1]
        return
    
    def wiki_search(self, search_term):
        """ Search a item by label and alias in wikidata. For the words which are an item in wikidata, append them to wiki_keyword_list of the current dataset object.

        Args:
            search_term: the word we want to search
        """
        url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&search={search_term}&language=zh"

        response = requests.get(url)
        data = response.json()
        word = {}

        # organize the response
        if "search" in data:
            for result in data["search"]:
                # Get wikidata keyword
                qid = result["id"]
                label = result["label"]

                # Print out each search result
                #description = result.get("description", "No description available")
                #print(f"QID: {qid}, Label: {label}, Description: {description}")

                # append wikidata keyword to self
                word = {"qid": qid, "label": label}
                self.wiki_keyword_list.append(word)
        else:
            print("No results found.")
        return
    
    def osm_search(self, search_term):
        """ Search a item in OpenStreetMap. For the locaiton which exists in OSM, append them to geoInfo_list of the current dataset object.

        Args:
            search_term: the word/location we want to search
        """
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": search_term,
            "format": "json",
            "polygon_geojson": "1",  # Request GeoJSON polygons
            "limit": 7
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            for place in data:
                loc = str(place["geojson"]).replace("'", "\"")
                self.geoInfo_list.append(loc)
        else:
            print("No results found.")
        return

    def gen_meta(self):
        """ Generate wikidata keywords and geographic information to the current dataset object
        """
        # do the NER
        self.make_ner_map()

        for item in self.ner_map:
            self.wiki_search(item)
            self.osm_search(item)
        return

# Example Usage ============================================================
# fulfill metadata of a dataset 
title = ''
description = ''
resource_names = []
resource_descriptions = []
organization_title = ""
organization_description = ""

# Create a dataset object
my_dataset = dataset(title, description, resource_names, resource_descriptions, organization_title, organization_description)

# generate recommended wikidata key words and geographic information
my_dataset.gen_meta()

# print
print(my_dataset.wiki_keyword_list[0]) # print the first element of wiki keywords
print(my_dataset.geoInfo_list[0]) # print the first element of geoInfo
