from flask import render_template,redirect,session, request, flash, url_for
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from werkzeug.utils import secure_filename
import os
import urllib.request

UPLOAD_FOLDER = 'pet_finder/flask_app/static/uploads/'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16*800*800

ALLOWED_EXTENTIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

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

@app.route('/edit/post/<int:id>')
def edit_post(id):
    session['id']= id
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_post.html",edit=Post.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/post', methods=['POST'])
def update_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/new/appointment')
    data = {
        "summary": request.form["summary"],
        "breed": request.form["breed"],
        "color": request.form["color"],
        "location": request.form["location"],
        "status": int(request.form["status"]),
        "id": session.get("id")
    }
    Post.update(data)
    return redirect('/dashboard')

@app.route('/delete/post/<int:id>')
def delete_post(id):
    session['id']= id
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Post.delete(data)
    return redirect('/dashboard')

@app.route('/upload', methods = ['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('Archivo no existe')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No se seleccionó ninguna imagen')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Imagen cargada correctamente')
        return render_template('dashboard.html', filename=filename)
    else:
        flash('Imagen debe ser de tipo png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/dislay/<filename>')
def display_image(filename):
    #print('display_image filename:' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)