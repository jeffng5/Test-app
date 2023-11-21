from flask import Flask, redirect, render_template, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
# from flask.ext.bcrypt import Bcrypt
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jeffreyng'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.debug=True
# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_RECORD_QUERIES'] = True


@app.route("/")
def home():

    return redirect('/register')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        u = User.register(username, password)

        user_details= User(username=u.username, password=u.password, email = email, first_name = first_name, last_name= last_name)

        db.session.add(user_details)
        db.session.commit()
       
        flash('User added')
        return redirect('/register')

    else:
        return render_template('register.html', form=form)
    

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        session['email'] = user.email
        session['first_name']= user.first_name
        session['last_name']= user.last_name
        if user:
            flash(f"Welcome back {user.username}!")
            session['user_id']= user.id
            session['username']= user.username
  
            return redirect(f"users/{username}")
        else:
            return f'User not found'
    return render_template('login.html', form = form)


@app.route('/users/<username>')
def user_page(username):
    username= session['username']
    if "user_id" not in session:
        flash("Please login")
        return redirect('/login')
    elif "user_id" in session:
        username= session['username']
        email = session['email']
        first_name = session['first_name']
        last_name= session['last_name']
        
        # title=Feedback.query.get_or_404()
        

        
    return render_template('secret.html', username=username, email=email, first_name=first_name, last_name=last_name)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback(username):
    username= session['username']
    form = FeedbackForm()
    if form.validate_on_submit():
        title= form.title.data
        content= form.content.data
        username= session['username']
        #content = Feedback.join.content.get_or_404(session['id'])
        fb = Feedback(title=title, content=content, username=username)
        db.session.add(fb)
        db.session.commit()
        return redirect('/user/<username>')
    else:
        return render_template('add_feedback.html', form = form)