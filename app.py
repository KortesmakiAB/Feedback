from flask import Flask, redirect, render_template, session, flash
from models import *
from forms import *
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "GimmeSomeFeedback!Pls"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def show_homepage():
    """Display Homepage"""

    return  redirect('/register')


@app.route('/register', methods = ['GET', 'POST'])
def register_user():
    """Show a form that when submitted will register/create a user (GET). This form should accept a username, password, email, first_name, and last_name.
    Process the registration form by adding a new user (POST)."""

    form = AddUserForm()

    if form.validate_on_submit():
        username    = form.username.data
        password    = form.password.data
        email       = form.email.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        return redirect('/secret')
    
    else:
        return render_template('user_register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login_user():
    """Show a form that when submitted will login a user (GET).
    Process the login form, ensuring the user is authenticated and going to /secret if so."""

    form = LoginForm()

    if form.validate_on_submit():
        username    = form.username.data
        password    = form.password.data

        user        = User.login(username, password)

        if user:
            flash(f'Welcome Back, {user.username}!', 'primary')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        
        else:
            form.username.errors = ['Invalid username/password.']

    else:
        return render_template('user_login.html', form = form)


@app.route('/logout')
def logout_user():
    """Logout the user, clear any information from the session and redirect to root route"""

    session.pop(user)
    flash('Goodbye!', 'info')

    # ???????????? TODO
    db.session.rollback()

    return redirect('/')


@app.route('/users/<username>')
def show_user_details(username):
    """Display a template the shows information about that user (everything except for their password)"""

    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/')
    
    else:
        user    = User.query.get_or_404(username)
        return render_template('user_details.html', user = user)


@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):
    """Remove the user from the database and make sure to also delete all of their feedback. 
    Clear any user information in the session and redirect to /."""


    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/')
    
    else:
        user    = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        flash("User account deleted!", "info")

        return render_template('user_details.html', user = user)

   
@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def handle_feedback(username):
    
    """Display a form to add feedback (GET)
    Add a new piece of feedback and redirect to /users/<username> """
    
    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/')

    form = FeedbackForm()

    if form.validate_on_submit():
        title       = form.title.data
        content     = form.content.data

        feedback    = Feedback(title = title, content = content, username = session['username'])
        
        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('feedback_form.html', form = form)


@app.route('/feedback/<int:id>/update', methods = ['GET', 'POST'])
def handle_feedback_edit(id):
    """Display a form to edit feedback.
    Update a specific piece of feedback and redirect to /users/<username>."""

    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/')

    feedback    = Feedback.query.get_or_404(id)
    form        = FeedbackForm(obj = feedback)

    if form.validate_on_submit() and feedback.username == session['username']:
        feedback.title      = form.title.data
        feedback.content    = form.content.data

        db.session.commit()

        return redirect(f'/../../users/{feedback.user.username}')

    elif feedback.username == session['username']:

        return render_template('feedback_form.html', form = form)


@app.route('/feedback/<int:id>/delete', methods = ['POST'])
def delete_feedback(id):
    """Delete a specific piece of feedback and redirect to /users/<username>."""

    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/')

    feedback    = Feedback.query.get_or_404(id)
    # raise
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", "info")

        return redirect(f'/../../users/{feedback.user.username}')

