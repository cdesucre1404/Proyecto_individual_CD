from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.profile import Profile

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    profile= Profile.get_one()
    return render_template("profile.html",user=User.get_by_id(data),profile=profile)