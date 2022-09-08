from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date

class Post:
    db_name = 'pet_finder'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.summary = db_data['summary']
        self.breed = db_data['breed']
        self.color = db_data['color']
        self.location = db_data['location']
        self.status = db_data['status']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (summary, breed, color, location, status, user_id) VALUES (%(summary)s,%(breed)s,%(color)s,%(location)s, %(status)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts,users WHERE users.id = posts.user_id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_posts = []
        for row in results:
            all_posts.append( cls(row) )
        return all_posts
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET summary=%(summary)s, breed=%(breed)s, color=%(color)s, location=%(location)s, status=%(status)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)