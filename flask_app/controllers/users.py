from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.profile import Profile
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/signup',methods=['POST', 'GET'])
def sing_up():
    if not User.validate_register(request.form):
        return redirect('/register')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST', 'GET'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Correo electrónico no es válido","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Contraseña incorrecta","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    data ={ 
        'id': session['user_id']
    }
    ad=Post.get_all()
    if 'user_id' not in session:
        return redirect('/logout')

    return render_template("dashboard.html", user=User.get_by_id(data), ad = ad)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')