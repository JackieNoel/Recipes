from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe_model import Recipe
from flask import flash
from flask_bcrypt import Bcrypt
import re

email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'recipe_dashboard'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []


    @classmethod
    def save_user(cls, data):
        query = 'INSERT INTO users(first_name, last_name, username, email, password) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s)'
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def show_one_user(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        result = connectToMySQL(db).query_db(query, {'id':id})
        return cls(result[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL(db).query_db(query, data)
        if len(result) ==0:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_with_recipes(cls, data):
        query = 'SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(users_id)s'
        results = connectToMySQL(db).query_db(query, data)
        one_user = cls(results[0])
        for recipe in results: 
            one_recipe = {
                'id': recipe['recipes.id'],
                'recipe_name': recipe['recipe_name'],
                'description': recipe['description'],
                'ingredients': recipe['ingredients'],
                'total_time': recipe['total_time'],
                'instructions': recipe['instructions'],
                'created_at': recipe['recipes.created_at'],
                'updated_at': recipe['recipes.updated_at']
            }
            one_user.recipes.append(Recipe(one_recipe))
        return one_user
    
    @staticmethod
    def user_validator(user):
        is_valid = True
        if len(user['first_name']) < 5:
            flash("Your name must be at least 5 characters.")
            is_valid = False
        if len(user['last_name']) < 5:
            flash("Your name must be at least 5 characters.")
            is_valid = False
        if len(user['username']) < 5:
            flash("Your username must be at least 5 characters.")
            is_valid = False
        if not email_REGEX.match(user['email']):
            flash("Your email or password is invalid.")
            is_valid = False
        if len(user['password']) < 5:
            flash("Your email or password is invalid.")
            is_valid = False
        return is_valid #CHECK FOR BUGS
