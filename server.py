"""File that deals with server."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, 
                    session, Markup)

from flask_debugtoolbar import DebugToolbarExtension

from model import * 


app = Flask(__name__) # this is the instance of the flask application

app.secret_key = "ABC" # Required to use Flask sessions and debug toolbar

app.jinja_env.undefined = StrictUndefined # Raises error for undefined vars


## Routes here #############################################################

# use a lot of RESTful API stuff here (mostly single-page app, will use AJAX/React)

@app.route("/")
def index():
    """Homepage.""" 

    return render_template("homepage.html")


@app.route("/register", methods=["GET"])
def display_registration_form():
    """Display registration form for a new user."""

    return render_template("registration_form.html")


@app.route("register", methods=["POST"])
def execute_user_registration():
    """Adds new user to database."""

    username = request.form.get("username")
    password = request.form.get("password")
    default_home_address = request.form.get("default_home_address")
    default_destination_address = request.form.get("default_destination_address")

    user = User(username=username, password=password, 
                default_home_address=default_home_address, 
                default_destination_address=default_destination_address)

    db.session.add(user)
    db.session.commit()

    return redirect('/')


@app.route("/login", methods=["GET"])
def display_login_page():
    """Display login page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def check_login_credentials():
    """Check user email and password against the database, login user."""

    username = request.form.get("username") # get username from form
    password = request.form.get("password") # get username from form
    user = User.query.filter_by(username=username).one() # queries the db for the user object

    if (user.username and user.password):  # if the user already has a username and password
        if user.password == password:  # check if the password is the same
            session['user'] = user.user_id # adds user to the session
            flash("You are now logged in.")
            return redirect(f"/{username}/dashboard")  # create dashboard route later (includes task vault, gameplan, and maps API)

@app.route("/logout")
def log_out_user():
    """Log user out."""

    session['user'] = None  # clears the user's data from the session
    flash("You are now logged out.")

    return redirect("/")


@app.route("/tasks")
def task_list():
    """Show list of tasks.""" # this is going to be the task vault, all tasks

    tasks = Task.query.all()
    return render_template("task_list.html")


@app.route("/add_new_task")
def add_new_task():
    """Add a new task to user's task list."""

##### finish this one 


@app.route("/<username>/settings")
def show_user_settings():
    """Show user's settings."""

    user_id = session['user'] # get the user_id from the session dictionary
    user = User.query.get(user_id) # use the user_id to get the user object
    username = user.username # get the username from the user object
    user_settings = UserSetting.query.filter_by(user_id=user_id).all()

    return render_template("user_settings.html", username=username, 
                            user_settings=user_settings)

@app.route("update_user_settings")
def update_user_settings():
    """Update settings for a user."""

#### finish this one


@app.route("/<username>/gameplan")
def show_user_gameplan():
    """Show user's morning gameplan."""

    user_id = session['user'] # get the user_id from the session dictionary
    user = User.query.get(user_id) # use the user_id to get the user object
    username = user.username # get the username from the user object
    gameplan_tasks = GameplanTask.query.filter_by(username=username).all()

    return render_template("user_gameplan.html", username=username,
                            gameplan_tasks=gameplan_tasks)


@app.route("/update_gameplan")
def update_gameplan():
    """Update user's gameplan."""

##### finish this one



