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
    """Show homepage.""" 

    return render_template("homepage.html")


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
        else:
            flash("Incorrect login information. Please try again.")
            return redirect("/login")

    return render_template("login.html", username=username, password=password,
                            user=user)


@app.route("/logout")
def log_out_user():
    """Log user out."""

    session['user'] = None  # clears the user's data from the session
    flash("You are now logged out.")

    return redirect("/")


@app.route("api/tasks", methods=["GET"])
def task_list():
    """Show list of tasks.""" # this is going to be the task vault, all task objects

    user_id = session['user']  # get the user_id from the session dictionary
    tasks = Task.query.filter_by(user_id=user_id).all()  # get list of user's task objects

    # may need to figure out what to get out of the task objects to display

    return render_template("task_list.html", tasks=tasks)


@app.route("/api/task", methods=["POST"])
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
def delete_task_from_task_list():
    """Delete a task from user's task list."""

    user_id = session['user']  # get the user_id from the session dictionary
    ### finish this one


@app.route("/settings")
def show_user_settings():
    """Show user's settings."""

    user_id = session['user'] # get the user_id from the session dictionary
    user = User.query.get(user_id) # use the user_id to get the user object
    username = user.username # get the username from the user object
    user_settings = UserSetting.query.filter_by(user_id=user_id).all() # list of setting objects

    return render_template("user_settings.html", username=username, 
                            user_settings=user_settings)

@app.route("/api/setting/<name>", methods=['PUT'])
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
def show_user_gameplan():
    """Show user's morning gameplan."""

    user_id = session['user'] # get the user_id from the session dictionary
    user = User.query.get(user_id) # use the user_id to get the user object
    username = user.username # get the username from the user object
    gameplan_tasks = GameplanTask.query.filter_by(username=username).all()

    return render_template("user_gameplan.html", username=username,
                            gameplan_tasks=gameplan_tasks)


@app.route("/gameplan", methods=["POST"])
def update_gameplan():
    """Update user's gameplan."""
    # commits all information in gameplan into the gameplan table so user can 
    # access it next time logs in

    user_id = session['user']
    user = User.query.get(user_id)
    gameplan_tasks = user.gameplan  # list of gameplan task objects

    db.session.add_all(gameplan_tasks)
    db.session.commit()

    return redirect("/dashboard")


@app.route("/about")
def display_about_page():
    """Display about page."""

    return render_template("about.html")


## Some of these routes will need to be changed to JSON using jsonify









