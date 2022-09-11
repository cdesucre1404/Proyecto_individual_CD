from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date, datetime
import math

class Post:
    db_name = 'pet_finder'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.summary = db_data['summary']
        self.breed = db_data['breed']
        self.color = db_data['color']
        self.location = db_data['location']
        self.status = db_data['status']
        self.posted_at = db_data['posted_at']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (summary, breed, color, location, status, user_id) VALUES (%(summary)s,%(breed)s,%(color)s,%(location)s, %(status)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)


    def time_span(self):
        now = datetime.now()
        delta = now - self.posted_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts,users WHERE users.id = posts.user_id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_posts = []
        for row in results:
            all_posts.append( cls(row) )
        return all_posts

    @classmethod
    def list_all(cls, data):
        query = "SELECT * FROM posts, users WHERE posts.id = user_id"
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        list_posts = []
        for row in results:
            list_posts.append( cls(row) )
        return list_posts

    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET summary=%(summary)s, breed=%(breed)s, color=%(color)s, location=%(location)s, status=%(status)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['summary']) < 0:
            is_valid = False
            flash("Resumen no puede estar en blanco","post")
        return is_valid


