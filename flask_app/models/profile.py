from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date

class Profile:
    db_name = 'pet_finder'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.gender = db_data['gender']
        self.city = db_data['city']
        self.number = db_data['number']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM profiles WHERE profile_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM profiles WHERE id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

