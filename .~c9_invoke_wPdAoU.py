import matplotlib
matplotlib.use('Agg')
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
cuisine_list = mongo.db.cuisine.find()

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
    token = str(token).lower()

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
    
    

# TABLE OF COUNTS - CUISINE
def cuis_dataframe():
    recipesmainDataFrame = pandas.DataFrame()
    recipesmainDataFrame['cuisine'] = [recipe['cuisine']
                                                for recipe in results]
    recipe_by_cuisine = recipesmainDataFrame['cuisine'].value_counts()
    return recipe_by_cuisine


# TOP MAIN INGREDIENT PIE CHART
recipesDataFrame = pandas.DataFrame()
recipesDataFrame['main_ingredient'] = [recipe['main_ingredient'] for recipe in results]
for c in main_ingredient_list:
    recipesDataFrame[
        c['main_ingredient']] = recipesDataFrame['main_ingredient'] \
        .apply(lambda recipe: is_text_in_field(c['main_ingredient'], recipe))


# TOP CATEGORY PIE CHART
def category_pie():
    fig = plt.figure()
    slices = recipesDataFrame['chicken'].value_counts()[True],\
        recipesDataFrame['test'].value_counts()[True],\
        recipesDataFrame['test2'].value_counts()[True],\
        recipesDataFrame['test3'].value_counts()[True]

    activities = ["chicken", "test", "test2", "test3"]
    cols = ['c', 'm', 'r', 'b']

    plt.pie(slices, colors=cols, labels=activities,
            startangle=90, shadow=True,  autopct='%1.1f%%')

    fig.savefig('static/img/graphs/piechart-category.svg')
    # plt.show()


# TOP CUISINE PIE CHART
def cuisine_pie():
    fig = plt.figure()
    slices = recipesDataFrame['Africa'].value_counts()[True],\
        recipesDataFrame['American'].value_counts()[True],\
        recipesDataFrame['Russian'].value_counts()[True],\
        recipesDataFrame['Cajun'].value_counts()[True]

    activities = ["Africa", "American", "Russian", "Cajun"]
    try :
        print(slices["American"])
    except KeyError:
        print("KeyError encountered")
    
    cols = ['c', 'm', 'r', 'b']

    plt.pie(slices, colors=cols, labels=activities,
            startangle=90, shadow=True,  autopct='%1.1f%%')

    fig.savefig('static/img/graphs/piechart-cuisine.svg')
    # plt.show()
    
# BAR CHARTS - CATEGORY
fig = plt.figure()
fig.subplots_adjust()

ax1 = fig.add_subplot(2, 1, 1)

ax1.tick_params(axis='x', labelsize=15)
ax1.tick_params(axis='y', labelsize=15)
ax1.set_xlabel('Category', fontsize=12)
ax1.set_ylabel('Number of recipes', fontsize=12)
ax1.xaxis.label.set_color('#393d3f')
ax1.yaxis.label.set_color('#393d3f')
ax1.tick_params(axis='x', colors='#393d3f')
ax1.tick_params(axis='y', colors='#393d3f')
ax1.set_title('Top 10 Categories', fontsize=15, color='#393d3f')

# plot the top 10 Category
recipe_by_category = cat_dataframe()
recipe_by_category[:10].plot(ax=ax1, kind='bar', color='#586a7a')

# plot the top 10 Cusine
recipe_by_cuisine = cuis_dataframe()
recipe_by_cuisine[:10].plot(ax=ax1, kind='bar', color='#586a7a')

# colour the spines(borders)
for spine in ax1.spines.values():
    spine.set_edgecolor('#393d3f')

# render the graph
# plt.show()

# Save the figure
fig.savefig('static/img/graphs/barchart-category.svg')

# BAR CHARTS - CUISINE
fig1 = plt.figure()
fig1.subplots_adjust()

ax2 = fig1.add_subplot(2, 1, 1)

ax2.tick_params(axis='x', labelsize=15)
ax2.tick_params(axis='y', labelsize=15)
ax2.set_xlabel('Cuisine', fontsize=12)
ax2.set_ylabel('Number of recipes', fontsize=12)
ax2.xaxis.label.set_color('#393d3f')
ax2.yaxis.label.set_color('#393d3f')
ax2.tick_params(axis='x', colors='#393d3f')
ax2.tick_params(axis='y', colors='#393d3f')
ax2.set_title('Top Cuisine', fontsize=15, color='#393d3f')

# plot the top 10 main
recipe_by_cuisine = main_dataframe()
recipe_by_cuisine[:10].plot(ax=ax2, kind='bar', color='#62929e')

# colour the spines(borders)
for spine in ax2.spines.values():
    spine.set_edgecolor('#393d3f')

# render the two graphs at once
# plt.show()

# Save the figure
fig1.savefig('static/img/graphs/barchart-cuisine.svg')

# endregion





# RUN FUNCTIONS
cat_dataframe()
main_dataframe()
cuis_dataframe()
category_pie()
cuisine_pie()
