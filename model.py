"""Models and database functions for for Mindful Mornings project."""

import flask_login
from flask_sqlalchemy import SQLAlchemy # connection to PostgreSql database
# getting this from the Flask-SQLAlchemy helper library
# On this, session object, where most interactions occur (committing, etc.)

db = SQLAlchemy() # instance of SQLAlchemy, everything comes off of this object

#############################################################################
# Model Definitions

class User(db.Model):
    """A user of Mindful Mornings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    tasks = db.relationship("Task", backref='user')
    # user.tasks returns list of tasks 
    # this way, can do tasks.user to get the user object

    gameplan = db.relationship("GameplanTask", backref='user')
    # user.gameplan returns list of gameplan tasks
    # this way, can do gameplan_task.user to get the user object

    settings = db.relationship("UserSetting") # go to UserSetting to see other one
    # user.settings returns list of users's settings


    def __init__(self, username, password):
        """Create a user, given username and password."""

        self.username = username
        self.password = password


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} username={self.username}>"


    @classmethod
    def get_user_by_username(cls, username):
        """Get a user, given their username."""

        return cls.query.filter_by(username=username).one()


class Setting(db.Model):
    """List of all settings."""
    # Place to store just the names of all of the settings, not their actual values.
    # Linked to users through the users_settings table. 
    # A user has many settings, and settings have many users --> middle table

    __tablename__ = "settings"

    setting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    setting_name = db.Column(db.String(100), unique=True)
    setting_default_value = db.Column(db.String(100))

    users_settings = db.relationship("UserSetting")
    # setting.users_settings returns a list of the users' settings for that setting

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Setting setting_id={self.setting_id} setting_name={self.setting_name}>"


class UserSetting(db.Model):
    """A setting that has been set by a user."""
    # This is a Middle Table (meaningful)
    # Like Comments that users can make about a book.
    # A user has many settings. Settings can pertain to many users. 
    # Each row's value is what a particular user has set for a particular setting.

    __tablename__ = "users_settings"

    user_setting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                        nullable=False)
    setting_id = db.Column(db.Integer, db.ForeignKey("settings.setting_id"),
                           nullable=False)
    value = db.Column(db.String(100), nullable=False)

    user = db.relationship("User") # usersetting.user returns the user object
    setting = db.relationship("Setting") # usersetting.setting returns the setting object

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserSetting setting_id={self.setting_id} user_id={self.user_id} value={self.value}>"

    
class Task(db.Model):
    """A task that belongs to a user (a theoretical 'to-do' blueprint)."""
    # A user has many tasks. A task can be a gameplan task (special type of task).
    # These tasks exist as things to do but don't have a set time to be done. 
    # They get a time to be done/more attributes once moved into the gameplan.

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                        nullable=False)
    task_name = db.Column(db.String(50), nullable=False)
    task_description = db.Column(db.String(100), nullable=True) # optional
    duration_estimate = db.Column(db.Integer, nullable=False) # in minutes
    duration_actual = db.Column(db.Integer, nullable=True) # in minutes

    gameplan_task = db.relationship("GameplanTask", uselist=False, # don't want a list, just one item
                                    backref="task") 
    # this is how to get the Gameplan Task object (which has more attributes)

    def __init__(self, task_name, duration_estimate):
        """Create a task, given task name and duration estimate in minutes."""

        self.task_name = task_name
        self.duration_estimate = duration_estimate

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Task task_id={self.task_id} task_name={self.task_name} user_id={self.user_id}>"

    @property
    def order(self):
        return self.gameplan_task.order or None  # get the order of the task easily
    


class GameplanTask(db.Model): #Twitter Employee (a special type of twitter user)
    """Task that is part of the gameplan for the morning."""
    # A gameplan task is a special type of task. One to one relationship
    # Can refer to current morning or the next day's morning (depending on what time it is currently). 

    __tablename__ = "gameplan_tasks"

    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), 
                        primary_key=True, 
                        nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    order = db.Column(db.Integer, unique=True)
    start_time = db.Column(db.DateTime, unique=True)
    end_time = db.Column(db.DateTime, unique=True)
    
    # can access with user.gameplan (due to the backref)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<GameplanTask task_id={self.task_id} user_id={self.user_id}>"


class Category(db.Model):
    """Categories that tasks belong to."""
    # This has a many to many relationship with tasks (tasks can have many 
    # categories and categories can have many tasks).
    # This is to help user add 'tags' to their tasks.
    # Will build more logic into this if time permits. (class methods)
    # Category ideas: must-do, optional, one-off, repeating, default, mondays, etc.

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True,
                            primary_key=True, nullable=False)
    category_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Category id={self.category_id} name={self.category_name}>"


class TaskCategory(db.Model): # Like BookGenre table
    """Place to store tasks and what categories they belong to."""
    # Just an association table. Not a meaningful middle table. 
    # A task belongs to a category. It can belong to multiple categories. 
    # A category can have many tasks. 
    # Each row is just a combo of a task (task_id) and a category (category_id).

    __tablename__ = "tasks_categories"

    tasks_categories_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))

    def __repr__(self):
        """Provide helpful information when printed."""

        return f"<TaskCategory id= {self.tasks_categories_id} task_id={self.task_id} category_id={self.category_id}>"


#############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use PostgresSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mindfulmornings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # Running this file interactively allows direct interaction w/ database.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

