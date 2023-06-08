from flask import Flask, render_template, request, session, redirect
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask import flash


@app.route('/new_recipe')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/add_new_recipe', methods=['post'])
def add_new_recipe():
    data = {
        'recipe_name': request.form['recipe_name'],
        'description': request.form['description'],
        'ingredients': request.form['ingredients'],
        'total_time': request.form['total_time'],
        'instructions': request.form['instructions'],
        'user_id': session['user_id']
    }
    recipe = Recipe.save_recipe(data)
    return redirect('/success')

@app.route('/twenty_min_recipe')
def twenty_recipe():
    return render_template('20_min_recipes.html')

@app.route('/forty_min_recipe')
def forty_recipe():
    return render_template('40_min_recipes.html')

@app.route('/sixty_min_recipe')
def sixty_recipe():
    return render_template('60_min_recipes.html')

@app.route('/find_recipe', methods=['post'])
def find_recipe():
    print(type(request.form['total_time']))
    if int(request.form['total_time']) <= 20:
        return redirect('/twenty_min_recipe') 
    if int(request.form['total_time']) >= 21 and int(request.form['total_time']) <= 40:
        return redirect('/forty_min_recipe')
    if int(request.form['total_time']) >=41 and int(request.form['total_time']) <=60:
        return redirect('/sixty_min_recipe')
    if int(request.form['total_time']) >= 61:
        flash("Please enter a minute amount less than one hour!") #NOT RUNNING FLASH MESSAGE, GETTING ERROR INSTEAD
        return redirect('/success') 
