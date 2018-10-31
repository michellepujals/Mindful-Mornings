"""File that deals with server for Mindful Mornings site."""

import flask_login 
from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, 
                    session, Markup)
from flask_debugtoolbar import DebugToolbarExtension
from model import *  # import everything from model.py

app = Flask(__name__) # this is the instance of the flask application

app.secret_key = "ABC" # Required to use Flask sessions and debug toolbar

app.jinja_env.undefined = StrictUndefined # Raises error for undefined vars

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

## Routes here #############################################################

# use a lot of RESTful API stuff here (mostly single-page app, will use AJAX/React)
# /api/ is for React

@app.route("/")
def index():
    """Show homepage.""" 
    user_id = session['user']
    if user_id:
        user = User.query.get(user_id)

        if user:
            username = user.username
    else:
        username = "friend"   # Welcome person even if they are not logged in 

    return render_template("homepage.html", username=username)


@app.route("/register", methods=["GET"])
def display_registration_form():
    """Display registration form for a new user."""

    return render_template("registration_form.html")


@app.route("/register", methods=["POST"])
def execute_user_registration():
    """Add new user to database using info provided in registration form."""
    # this is a dictionary . get request, does not return error if nothing there
    # will return None. ** Find out how to make 2 of these fields mandatory

    username = request.form.get("username")
    password = request.form.get("password")
    # control through JS/HTML
    default_home_address = request.form.get("default_home_address")
    default_destination_address = request.form.get("default_destination_address")

    user = User(username=username, password=password, 
                default_home_address=default_home_address, 
                default_destination_address=default_destination_address)

    db.session.add(user)
    db.session.commit()

    return redirect('/')

####### Flask-login callbacks ################################################
# ** From flask-login documentation---> need to decide which one to use***
# Tell Flask-login how to load a user from a Flask request and from session

@login_manager.user_loader
def user_loader():

    username = request.form.get("username") # get username from form
    password = request.form.get("password") # get password from form
    users = User.query.all() # gets all user objects in a list

    if username not in users:
        return
        
    user = User.query.filter_by(username=username).one() # queries the db for the user object
    return user


@login_manager.request_loader
def request_loader(request):

    username = request.form.get("username") # get username from form
    password = request.form.get("password") # get password from form
    users = User.query.all() # gets all user objects in a list

    if username not in users: # returns none if user does not exist
        return

    user = User.query.filter_by(username=username).one() # queries the db for the user object
    user.is_authenticated = password == user.password

    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


############# Views, etc. ######################################################


@app.route("/login", methods=["POST"])
def check_login_credentials():
    """Check user email and password against the database, add user to session."""

    username = request.form.get("username") # get username from form
    password = request.form.get("password") # get password from form
    user = User.query.filter_by(username=username).one() # queries the db for the user object

    if user:  # if the user exists (if that username exists)
        if user.password == password:  # check if the password is the same
            session['user'] = user.user_id # adds user to the session
            flask_login.login_user(user) # flask-login specific method call
            flash("You are now logged in.")
            return redirect("/")
        else:
            flash("Incorrect login information. Please try again.")
            return redirect("/")

    elif not user:
        flash("Your username does not exist. Please try again or register as a new user.")
        return redirect("/")

    return render_template("homepage.html", username=username, password=password,
                            user=user)


@app.route("/logout")
def log_out_user():
    """Log user out."""

    session['user'] = None  # clears the user's data from the session
    flask_login.logout_user() # Flask-login specific method call
    flash("You are now logged out.")

    return redirect("/")


@app.route("/api/tasks", methods=["GET"])
@flask_login.login_required  # flask-login specific method call
def task_list():
    """Show list of tasks.""" # All task objects for this user

    user_id = session['user']  # get the user_id from the session dictionary
    tasks = Task.query.filter_by(user_id=user_id).all()  # get list of user's task objects

    # may need to figure out what to get out of the task objects to display

    return render_template("dashboard.html", tasks=tasks)


@app.route("/api/task", methods=["POST"])
@flask_login.login_required  # flask-login specific method call
def add_new_task():
    """Add a new task to user's task list."""

    user_id = session['user']  # get the user_id from the session dictionary
    task_name = request.form.get(task_name=task_name)  # get from the form user fills out
    duration_estimate = request.form.get(duration_estimate=duration_estimate)  # get from form
    new_task = Task(user_id=user_id, task_name=task_name, 
                    duration_estimate=duration_estimate)  # instantiate a Task object

    db.session.add(new_task)  # add new task object to user's list of tasks (tasks table)
    db.session.commit()

    return redirect ("/dashboard")  # go back to dashboard


@app.route("/api/task/<task_id>", methods=["DELETE"])
@flask_login.login_required  # flask-login specific method call
def delete_task_from_task_list():
    """Delete a task from user's task list."""

    task_id = request.form.get(task_id=task_id)  # get task_id from form
    task_to_delete = Task.query.get(task_id)  # get the task object to delete
    db.session.delete(task_to_delete)  # delete from database/task table
    db.session.commit() 

    return redirect ("/dashboard")  # go back to dashboard


@app.route("/settings")
@flask_login.login_required  # flask-login specific method call
def show_user_settings():
    """Show user's settings."""

    user_id = session['user'] # get the user_id from the session dictionary
    user = User.query.get(user_id) # use the user_id to get the user object
    username = user.username # get the username from the user object
    user_settings = UserSetting.query.filter_by(user_id=user_id).all() # list of setting objects

    return render_template("user_settings.html", username=username, 
                            user_settings=user_settings)

@app.route("/api/setting/<name>", methods=['PUT'])
@flask_login.login_required  # flask-login specific method call
def update_user_setting():
    """Update a setting for a user."""

    user_id = session['user'] # get the user_id from the session dictionary
    username = user.username # get the username from the user object
    new_value_user_setting = request.form.get(value=value)  # get from form
    user_setting = UserSetting.query.filter_by(user_setting_id=user_setting_id).one() # get the user setting object
    user_setting.value = new_value_user_setting  # update setting with new value

    db.session.commit()

    return redirect("/dashboard")

@app.route("/gameplan", methods=["GET"])
@flask_login.login_required  # flask-login specific method call
def show_user_gameplan():
    """Show user's morning gameplan."""

    user_id = session['user'] # get the user_id from the session dictionary
    user = User.query.get(user_id) # use the user_id to get the user object
    username = user.username # get the username from the user object
    gameplan_tasks = GameplanTask.query.filter_by(username=username).all()

    return render_template("dashboard.html", username=username,
                            gameplan_tasks=gameplan_tasks)


@app.route("/gameplan", methods=["DELETE","POST"])
@flask_login.login_required  # flask-login specific method call
def update_gameplan():
    """Update user's gameplan."""
    # First clears out the current gameplan tasks for that user.
    # Then commits all information in gameplan into the gameplan table 
    # so user can access it next time logs in.

    user_id = session['user']  # get the user_id from the session
    user = User.query.get(user_id)  # get the user object
    gameplan_tasks = user.gameplan # get the list of gameplan tasks for user
    for item in gameplan_tasks:  # loop through each task in the list
        db.session.delete(item)  # delete that task
    db.session.commit()  # commit changes
    
    #** Somehow get all the gameplan task objects that are in gameplan area
    # and add them to a list, call it new_gameplan

    for item in new_gameplan:  # loop through each item in the list
        db.session.add(item)  # add that item
    db.session.commit() # commit changes

    return redirect("/dashboard")


@app.route("/about")
def display_about_page():
    """Display about page."""

    return render_template("about.html")


if __name__ == "__main__":
    # set debug to true since it has to be true at the point
    # where we invoke the DebugToolbarExtension
    app.debug = True 
                   
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the debug toolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

## Some of these routes will need to be changed to JSON using jsonify









