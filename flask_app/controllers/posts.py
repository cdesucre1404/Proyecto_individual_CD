from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_app.models.profile import Profile


@app.route('/new/post')
def new_post():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_post.html',user=User.get_by_id(data))

@app.route('/create/post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/new/post')
    data = {
        "summary": request.form["summary"],
        "breed": request.form["breed"],
        "color": request.form["color"],
        "location": request.form["location"],
        "status": int(request.form["status"]),
        "user_id": session["user_id"]
    }

    Post.save(data)
    return redirect('/dashboard')


