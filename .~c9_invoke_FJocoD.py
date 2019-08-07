import pandas
import os
import re
import pymongo
import json
from flask import Flask, jsonify, json
from flask_pymongo import PyMongo
import matplotlib.pyplot as plt


statistics = Flask(__name__)
statistics.debug = False
statistics.config["MONGO_DBNAME"] = 'data-centric-dev'
statistics.config["MONGO_URI"] = 'mongodb://admin1234:admin1234@ds121295.mlab.com:21295/data-centric-dev'

mongo = PyMongo(statistics)

RECIPES_DATA_PATH = 'static/data/recipes.json'
main_ingredient_list = mongo.db.main_ingredient.find()
category_list = mongo.db.recipe_category.find()
allergen_list = mongo.db.allergens.find()

# READ JSON FILE
def read_json(file_path):
    results = []
    with open(RECIPES_DATA_PATH) as recipes_file:
        for recipes in recipes_file:
            try:
                recipe = json.loads(recipes)
                results.append(recipe)
            except ValueError:
                pass
        return results


# SEARCH JSON FOR TEXT
def is_text_in_field(token, recipe_content):
    token = token.lower()
    recipe_content = ''.join(recipe_content).lower()
    match = re.search(token, recipe_content)
    if match:
        return True
    return False

results = read_json(RECIPES_DATA_PATH)




# TABLE OF COUNTS - CATEGORY
def cat_dataframe():
    recipesCatDataFrame = pandas.DataFrame()
    recipesCatDataFrame['recipe_category'] = [recipe['recipe_category']
                                              for recipe in results]
    recipe_by_category = recipesCatDataFrame['recipe_category'].value_counts()
    return recipe_by_category


# TABLE OF COUNTS - Main Ingredient
def main_dataframe():
    recipesmainDataFrame = pandas.DataFrame()
    recipesmainDataFrame['main_ingredient'] = [recipe['main_ingredient']
                                            for recipe in results]
    recipe_by_main_ingredient = recipesmainDataFrame['main_ingredient'].value_counts()
    return recipe_by_main_ingredient





# RUN FUNCTIONS
cat_dataframe()
main_dataframe()