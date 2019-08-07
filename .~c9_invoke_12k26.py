import os
import pymongo
import math
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from bson.json_util import dumps
from bson import json_util
from datetime import datetime
from math import ceil
from statistics import cat_dataframe, cuis_dataframe, aller_dataframe

app = Flask(__name__)
app.debug = False
app.secret_key = "super secret key"
app.config["MONGO_DBNAME"] = 'data-centric-dev'
app.config["MONGO_URI"] = 'mongodb://admin1234:admin1234@ds121295.mlab.com:21295/data-centric-dev'

mongo = PyMongo(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('isLoggedin'):
            return f(*args, **kwargs)
        else:
            flash("You need to be logged in, to view this page", 'info')
            return render_template("index.html")
    return wrap

def compare_password(hashedpw, formpw):
    compare_pw = check_password_hash(hashedpw, formpw)
    return compare_pw
    
    
def get_user(username):
    row = mongo.db.users.find_one({'username': username.lower()})
    return row
    
    
def get_user_recipes(current_user_id):

        rows = [recipe for recipe in mongo.db.recipes.find(
            {
                '$query':
                {
                    'author_name': current_user_id}, '$orderby': {'votes': -1}
                }
            )]

        return rows
        
def get_votes_recipes():
    rows = mongo.db.recipes.find().sort('votes', -1).limit(3)
    return rows
        
        
def get_random_recipes():
        random_recipes = [
            random_recipe for random_recipe in mongo.db.recipes.aggregate(
                [
                    {'$sample': {'size': 12}}, {'$sort': {'votes': -1}}
                ]
            )]
        return random_recipes
        
def get_recent_recipes():
    
        recipes = [ recipe for recipe in mongo.db.recipes.find()
            .sort('_id', -1).limit(3)]
    
        return recipes
        


def get_difficulty():
    
    difficulty = [difficulty for difficulty in mongo.db.difficulty.find()]
    return difficulty

#Home page containing all recipes
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("index.html",
    recipes=mongo.db.recipes.find())
    
    
    
# get main ingredient
def get_main_ingredient():
    
    main_ingredient = [main_ingredient for main_ingredient in mongo.db.main_ingredient.find()]
    return main_ingredient

# get Cuisine
def get_cuisine():
    
    cuisine = [cuisine for cuisine in mongo.db.cuisine.find()]
    return cuisine
    
# get Allergens
def get_allergens():

    allergens = [allergens for allergens in mongo.db.allergens.find()]
    return allergens

    
# get Category    
def get_categories():
    
    categories = [category for category in mongo.db.recipe_category.find()]
    return categories

    
    


# pressing the signout button activated the logout function
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # get value from get request and clear sessions values
    if request.method == 'GET':
        session.pop('username', None)
        session.pop('userid', None)
        session['isLoggedin'] = False
        session.pop('_flashes', None)
        # display successful logout message
        flash("You are logged out", 'success')
    return redirect(url_for('get_recipes'))


    
#add recipe form  
@app.route('/add_recipe')
@login_required
def add_recipes():
    recipe_category = get_categories()
    cuisine = get_cuisine()
    allergens = get_allergens()
    difficulty = get_difficulty()
    main_ingredient = get_main_ingredient()
    return render_template("addrecipe.html", recipe_category=recipe_category, cuisine=cuisine, allergens=allergens, difficulty=difficulty, main_ingredient=main_ingredient)
    
# insert recipe to collection
@app.route('/insert_recipe', methods=['GET', 'POST'])   
@login_required
def insert_recipe():
    current_user_id = session['userid']
    recipes = mongo.db.recipes
    main_ingredient = mongo.db.main_ingredient
    cuisine = mongo.db.cuisine
    allergens = mongo.db.allergens
    ingred_list = request.form.getlist('ingredient')
    ingred_list_no_blanks = [i for i in ingred_list if i != ""]
    instruct_list = request.form.getlist('instruction')
    instruct_list_no_blanks = [i for i in instruct_list if i != ""]
    new_recipe = {
        'recipe_category': request.form.get('recipe_category'),
        'cuisine': request.form.get('cuisine'),
        'allergens': request.form.getlist('allergens'),
        'recipe_name': request.form.get('recipe_name').capitalize(),
        'author_name': current_user_id,
        'description': request.form.get('description'),
        'recipe_url': request.form.get('recipe_url'),
        'difficulty': request.form.get('difficulty'),
        'serves': request.form.get('serves'),
        'prep_time': request.form.get('prep_time').upper(),
        'cook_time': request.form.get('cook_time').upper(),
        'images': request.form.get('images'),
        'main_ingredient': request.form.get('main_ingredient').capitalize(),
        'ingredients': ingred_list_no_blanks,
        'instructions': instruct_list_no_blanks,
        'votes': int(0),
        'dateCreated': datetime.now(),
        'dateModified': datetime.now()
    }
    recipes.insert_one(new_recipe)
    return redirect(url_for('get_recipes'))
    
# edit recipe     
@app.route('/edit_recipe/<recipe_id>')
@login_required
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    recipe_category = get_categories()
    main_ingredient = get_main_ingredient()
    cuisine = get_cuisine()
    allergens = get_allergens()
    category_list = [category for category in recipe_category]
    main_ingredient_list = [main_ingredient for main_ingredient in main_ingredient]
    difficulty = get_difficulty()
    difficulty_list = [difficulty for difficulty in difficulty]
    return render_template('editrecipe.html', recipe=recipe, recipe_category=category_list, main_ingredient=main_ingredient_list, cuisine=cuisine, allergens=allergens, difficulty=difficulty_list )

# update recipe in collection
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
@login_required
def update_recipe(recipe_id):
    current_user_id = session['userid']
    recipes = mongo.db.recipes
    main_ingredient = mongo.db.main_ingredient
    cuisine = mongo.db.cuisine
    allergens = mongo.db.allergens
    ingred_list = request.form.getlist('ingredient')
    ingred_list_no_blanks = [i for i in ingred_list if i != ""]
    instruct_list = request.form.getlist('instruction')
    instruct_list_no_blanks = [i for i in instruct_list if i != ""]
    recipes.update_one({'_id': ObjectId(recipe_id)},
                       {'$set':
                        {
        'recipe_category': request.form.get('recipe_category'),
        'cuisine': request.form.get('cuisine'),
        'allergens': request.form.getlist('allergens'),
        'recipe_name': request.form.get('recipe_name').capitalize(),
        'author_name': current_user_id,
        'description': request.form.get('description'),
        'recipe_url': request.form.get('recipe_url'),
        'difficulty': request.form.get('difficulty'),
        'serves': request.form.get('serves'),
        'prep_time': request.form.get('prep_time').upper(),
        'cook_time': request.form.get('cook_time').upper(),
        'images': request.form.get('images'),
        'main_ingredient': request.form.get('main_ingredient').capitalize(),
        'ingredients': ingred_list_no_blanks,
        'instructions': instruct_list_no_blanks,
        
        'dateModified': datetime.now()
            }
        }
    )

    return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
# delete recipe from collection on viewrecipe page
@app.route('/viewrecipe_delete_recipe/<recipe_id>', methods=["POST"])
@login_required
def viewrecipe_delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipesearch'))
    
# delete recipe from collection on myrecipe page
@app.route('/myrecipes_delete_recipe/<recipe_id>', methods=["POST"])
@login_required
def myrecipes_delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('myrecipes'))

    

    
 # get categories collection
@app.route('/get_recipe_category')
@login_required
def get_recipe_category():
    return render_template('managecategories.html',
    recipe_category=mongo.db.recipe_category.find())
    
    
# delete category from recipe_categories collection   
@app.route('/delete_category/<category_id>', methods=["POST"])
@login_required
def delete_category(category_id):
    mongo.db.recipe_category.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))

# edit category 
@app.route('/edit_category/<category_id>')
@login_required
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.recipe_category.find_one({'_id': ObjectId(category_id)}))
    
 # update category within recipe_categories in database
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.recipe_category.update(
        {'_id': ObjectId(category_id)},
        {'recipe_category' : request.form.get('recipe_category')})
    return redirect(url_for('get_categories'))

# insert category in recipe_categories collection in database
@app.route('/insert_category', methods=['POST'])
def insert_category():
    recipe_category = mongo.db.recipe_category
    category_doc = {'recipe_category': request.form.get('recipe_category')}
    recipe_category.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
# add categories form
@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


# details page for recipe
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    the_author = mongo.db.users.find_one(
        {"_id": ObjectId(the_recipe['author_name'])
         })
    allergens_list = list(get_allergens())
    
    # list comprehension used to get allergen name from allergen_list
    allergens_list = [allergen_item["allergens"]
                      for allergen_item in allergens_list]
    allergens_list = (', '.join(map(str, allergens_list)))
    return render_template("viewrecipe.html",
                          allergens_list=allergens_list, recipe=the_recipe, recipeauthor_name=the_author)
    
# update vote recipe
@app.route('/update_vote/<recipe_id>', methods=['POST'])
def update_vote(recipe_id):
    current_user = session['username']
    recipes_voted_for = get_user(current_user)
    if recipe_id in recipes_voted_for['recipe_votes']:
        return 'fail'
    else:
        votes = None
        # get data from ajax post, set votes to data value
        votes = int(request.get_data())
        this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        current_vote = int(this_recipe['votes'])
        new_vote = current_vote + votes
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                    {'$set':
                                        {
                                            'votes': (new_vote)
                                        }
                                     }) 
        mongo.db.users.update_one({"username": current_user},
                                  {'$push':
                                   {
                                        'recipe_votes': recipe_id
                                    }
                                   })                                     
        # updated recipe votes
        this_recipe_updated = mongo.db.recipes.find_one(
                                {"_id": ObjectId(recipe_id)})                                     
        updated_recipe_vote = this_recipe_updated['votes']    
        return str(updated_recipe_vote)
        
# view myrecipes page
@app.route('/myrecipes')
@login_required
def myrecipes():
    
    current_user = dict(get_user(session['username']))
    # initiate the data, search recipes by author
    user_recipes_starting_id = [recipe for recipe in mongo.db.recipes.find(
                                {'author_name': session['userid']})]
    # get authors total count of recipes
    total_count = len(user_recipes_starting_id)

    if not user_recipes_starting_id:
        return render_template("myrecipes.html", total_count=total_count)
        

    # get updated data greater than the last doc _id displayed
    recipes = [recipe for recipe in mongo.db.recipes.find(
        {'$and': [{'author_name': session['userid']},
                  ]})]


    return render_template("myrecipes.html",
                           total_count=total_count,
                           recipes=recipes
                           )


                            
@app.route('/recipesearch', methods=['POST', 'GET'])
def recipesearch():
    recent_recipes = get_recent_recipes()
    highest_voted_recipe = get_votes_recipes()
    recipes = get_random_recipes()
    recipe_category = get_categories()
    cuisine = get_cuisine()
    allergens = get_allergens()
    difficulty = get_difficulty()
    main_ingredient = get_main_ingredient()
    
    return render_template("recipesearch.html",
                            recipes=recipes,
                            recipe_category=recipe_category,
                            cuisine=cuisine,
                            allergens=allergens,
                            recentrecipes=recent_recipes,
                            highestvotes=highest_voted_recipe,
                            difficulty=difficulty,
                            main_ingredient=main_ingredient
                            )
 
                            
@app.route('/recipesearchquery', methods=['POST', 'GET'])
def recipesearchquery():
    filteredRecipes = None
    query = request.get_data()
    query = str(query)
    query = query[1:]
    query = query.strip('\'"')
    
    try:
        filteredRecipes = [recipe for recipe in mongo.db.recipes.find(
                           {'$text': {'$search': query}})]
    except:
        # Ajax will return the error message
        return

    if filteredRecipes:
        # return recipes by category exist
        return render_template("recipesearchresults.html",
                               reciperesults=filteredRecipes)


# function get recipes by cuisine
@app.route('/filter_by_cuisine/<cuisine>', methods=['POST', 'GET'])
def filter_by_cuisine(cuisine):
    filteredRecipes = None
    cuisine = cuisine

    
    filteredRecipes = [recipe for recipe in mongo.db.recipes.find(
            {'$query':
                {'cuisine': cuisine},
                '$orderby': {'votes': -1}}
            )]
    return render_template("recipesearchresults.html",
                       reciperesults=filteredRecipes)
                     
# function get recipes by allergens
@app.route('/filter_by_allergens/<allergens>', methods=['POST', 'GET'])
def filter_by_allergens(allergens):
    filteredRecipes = None
    allergens = allergens

    
    filteredRecipes = [recipe for recipe in mongo.db.recipes.find(
            {'$query':
                {'allergens': allergens},
                '$orderby': {'votes': -1}}
            )]
    return render_template("recipesearchresults.html",
                       reciperesults=filteredRecipes)


# Function get recipes by category
@app.route('/filter_by_category/<category>', methods=['POST', 'GET'])
def filter_by_category(category):
    filteredRecipes = None
    recipe_category = category
    
    filteredRecipes = [recipe for recipe in mongo.db.recipes.find(
                             {
                                '$query':
                                    {'recipe_category': recipe_category},
                                    '$orderby': {'votes': -1}
                             }
                           )]
    return render_template("recipesearchresults.html",
                               reciperesults=filteredRecipes)
 
                            
#signup form
@app.route('/signup_user', methods=['POST'])
def signup_user():
    check_user = get_user(request.form.get('signupUsername'))
    if not check_user:
        users = mongo.db.users
        new_user = {
                'username': request.form.get('signupUsername').lower(),
                'hashed_password': generate_password_hash(
                                    request.form.get('signupPassword'),
                                    "sha256"),
                'firstname': request.form.get('firstName'),
                'lastname': request.form.get('lastName'),
                'recipe_votes': []
        }
        if new_user:
            users.insert_one(new_user)
            return redirect(url_for('get_recipes'))
    else:
        message = "fail"
        return message
    return

# login in to account     
@app.route('/login_user', methods=['POST'])
def login_user():
    pw = request.form.get('loginPassword')
    user = get_user(request.form.get('loginUsername').lower())
    if user:
        check_password = compare_password(user['hashed_password'], pw)
        if check_password:
            session['username'] = user['username']
            session['userid'] = str(user['_id']) 
            session['isLoggedin'] = True
            return redirect(url_for('get_recipes'))
            # message to user
            message = "Welcome back, " + user['username'] + "." \
                + "<br />""You will be redirected to your MyRecipes page."
            id = str(user['_id'])
            response = {
                "username": user['username'], "_id": id, "message": message
                }
            return jsonify(response)
        elif not check_password:
            message = "1"
            # This password is wrong
            return message
    else:
        # no user has than username
        message = "2"
        return message
   

# Stats Page
@app.route('/websitestats') 
def websitestats():
    cuis_data = cuis_dataframe()
    cat_data = cat_dataframe()
    aller_data = aller_dataframe()
    
    cuis_data_dict = {}
    for k, v in cuis_data.iteritems():
        cuis_data_dict.update({k: v})

    
    cat_data_dict = {}
    for k, v in cat_data.iteritems():
        cat_data_dict.update({k: v})
    
    
    aller_data_dict = {}
    for k, v in aller_data.iteritems():
        aller_data_dict.update({k: v})


    return render_template("websitestats.html",
                               cuis_data=cuis_data_dict,
                                cat_data=cat_data_dict,
                                aller_data=aller_data_dict)




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)