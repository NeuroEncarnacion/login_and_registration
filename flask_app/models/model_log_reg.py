from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


db = 'login_and_registration'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# Get all users method
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
            return users


# Save user information to the database
    @ classmethod
    def save(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(pw_hash)s);
                """
        return connectToMySQL(db).query_db(query, data)


# Get the id of one user
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])


# Check if an email already exists in the database 
    @ classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


# Validate the information a user is inputing into a form
    @ staticmethod
    def user_validation(data):
        EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name needs to be more than 2 characters.', 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name needs to be more than 2 characters.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address.', 'register')
            is_valid = False
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                """
        results = connectToMySQL(db).query_db(query, data)
        if len(results) != 0:
            flash('This email is already in use.', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password needs to be more than 8 characters.', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Your passwords must be matching.', 'register')
            is_valid = False
        return is_valid
