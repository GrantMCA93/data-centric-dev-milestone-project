# data-centric-dev-milestone-project

1. Heroku App: https://data-centric-dev-milestone-pro.herokuapp.com/
2. Heroku git: https://git.data-centric-dev-milestone-pro.git
3. GitHub: https://github.com/GrantMCA93/data-centric-dev-milestone-project

Project 4 data-centric-dev-milestone-project

This project is designed to allow users to search through recipes in an interactive way, to find a new and exciting recipe to cook.
The website allows you to create you own recipes aswell as vote for other users recipe you like.


## UX

This website is designed for people searching for recipes there interested in cooking. This is achieved by creating a visually appearing easy to interact with website.

The process for designing this website was to create a cooking website with interactive features.
[1] ,[2] & [3] were the websites initiallly used for design ideas
1. https://www.bbc.com/food
2. https://www.bbcgoodfood.com/
3. https://www.delish.com/

## Features

    *-app.py-*
The app.py file - is used to store and retrieve my recipes database information from mlab using mongodb.
    app.py is also used to store and retrieve login information for each used Email, Username, First Name, Last Name and Password
    app.py is used to retrieve information when searching for a particular recipe .
    allong with deleteing and editing and voting on recipes, searching for recipes using different parameters categoies, cuisine and allergens.
    The app.py also using to link to statistics.py what is used to provide the table, pie and bar charts for the websitestats.html page.
     
     *-statistics.html-*  
The statistics.html file in linked to the json file that provides the data used for the table, pie and bar charts for the websitestats.html page.
    The code to retrieve the correct information for the table, pie and bar charts exists in this file.

    *-requirements.txt-*
contains the programs used to create the webiste.

    *-Procfile-*
used to link the app.py file to the requirements.txt file



## page by page walkthrough of website features
1. base.html- This is an unviewable webpage that's used to create continuity in design for all the website pages. 
2. index.html - This is the start page of the website, it displays a welcome message and the ability to sign in/register for an account.
3. addcategory.html - This page allows you to create categories to be used for the recipes.
4. managecategories.html - This page allows you to view and managed the categories that exist
5. editcategory.html - This page is connect to the managecategories.html page and is designed to edit the existing categoies 
6.editrecipe.html - This page allows you to recipe existing recipes.
7. myrecipe.html - This page is the first page viewed when a user logs into an account. It allows you to view the recipes created by that account. 
8. recipesearch.html - This page is designed to allow people to search through the existing recipes and find a recipe from different parameters.
9. viewrecipe.html - The page is conneted to the recipesearch.html and index.html page allow you to view more information about each recipe.
10. recipesearchresults.html - This page is used to provide the recipe results on the recipesearch.html page 
11. addrecipe.html - This page is used to add recipes for other users to search and view and recipe is also added to your myrecipe.html page.
12. websitestats.html - This page contains tabes, pie and bar charts displaying the number of each category, cuisine and allergen in the recipe database.
The graphs used for the websitestats.html page exist at path /static/img/graphs

## Potential future features
On The website statistics pages I didnt know how to get the graphs and tables to update automatically so it has to be done manually. 

## Technologies Used

1. Bootstrap	
2. JQuery
3. Python
4. Json
5. mlab


## Code Testing

I’ve tested the code in chrome, Firefox, Microsoft edge browser and safari as well as the mobile versions of these browsers.
I used W3C for CSS https://jigsaw.w3.org/css-validator/and HTML https://validator.w3.org/ to remove errors.



## Code Deployment

The project is pushed to github
process used -
link cloud9 to github
git remote add origin https://github.com/GrantMCA93/data-centric-dev-milestone-project.git
git add .
git commit -m "" <-- in quote marks describe changes made -->
git push -u origin master

The projects is hosted on Github pages
Heroku
mlab

## Credits 
app.py
#Used https://github.com/Sonnerz/project04-data-centric-cookbook/blob/master/app.py#L426 to help me with my app.py code
The login form used for website used the basic template from https://bootsnipp.com/snippets/8y25



## Media
The images used for each continent are all images founds from Google images, all the images licenses are Free to modify, share and use commerically.
images path location /static/img/recipes
1. "errorimage.jpg" This image is used when an error occurs displaying the desired Image for the recipe. The images source location is "https://cdn.pixabay.com/photo/2018/01/16/10/36/mistake-3085712_1280.jpg"
2. "likebutton.png" This image is used for the vote button of each recipe. The images source location is "http://pngimg.com/uploads/like/like_PNG29.png"
3. "pizza-wallpaper.jpeg" This image is used as the background on the Homepage of the website. The iamges source location is "https://cdn.pixabay.com/photo/2017/09/30/15/12/pizza-2802337_1280.jpg"
4. "print.png" This image is used for the print icon on the viewrecipe.html page. The images source location is "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Human-gnome-dev-printer.svg/128px-Human-gnome-dev-printer.svg.png"

## Acknowledgements 

Mentor:- Chris Zielinski  ckz8780@gmail.com 




