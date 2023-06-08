from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.user_model import User
from flask import flash
from flask_bcrypt import Bcrypt

db = 'recipe_dashboard'


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.ingredients = data['ingredients']
        self.total_time = data['total_time']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_recipe(cls, data):
        query = 'INSERT into recipes(recipe_name, description, ingredients, total_time, instructions, user_id) VALUES (%(recipe_name)s, %(description)s, %(ingredients)s, %(total_time)s, %(instructions)s, %(user_id)s)'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def select_recipe_20(cls, data):
        query = 'SELECT * FROM recipes WHERE total_time <= 20'
        return connectToMySQL(db).query_db(query, data)
