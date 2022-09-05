from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date

class Post:
    db_name = 'pet_finder'