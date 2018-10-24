"""Models and database functions for for Mindful Mornings project."""

from flask_sqlalchemy import SQLAlchemy # connection to PostgreSql database
# getting this from the Flask-SQLAlchemy helper library
# On this, session object, where most interactions occur (committing, etc.)

db = SQLAlchemy() # instance of SQLAlchemy, everything comes off of this object

#############################################################################
# Model Definitions

class User(db.Model):
    """User of Mindful Mornings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    home_address = db.Column(db.String(100), nullable=True)
    destination_address = db.Column(db.String(100), nullable=True)

    tasks = db.relationship('Task', backref='user')

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

    __tablename__ = "settings"

    setting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    setting_name = db.Column(db.String(100), unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Setting setting_id={self.setting_id} setting_name={self.setting_name}>"


class UserSetting(db.Model):
    """Settings regarding user."""
    # This is a Middle Table (meaningful)
    # Like Comments that users can make about a book.
    # A user has many settings. Settings can pertain to many users. 
    # Each row's value is what a particular user has set for a particular setting.

    __tablename__ = "users_settings"

    setting_id = db.Column(db.Integer, primary_key=True, 
                           db.ForeignKey("settings.setting_id"), 
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                        nullable=False)
    value = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<UserSetting setting_id={self.setting_id} user_id={self.user_id} value={self.value}>"

    
class Task(db.Model):
    """Task belonging to a user of Mindful Mornings website."""
    # A user has many tasks. A task can be a gameplan task (special type of task).
    # These tasks exist as ideas/blueprints. They come into play and aquire more 
    # attributes once moved into the gameplan.

    __tablename__ = "tasks"

    def __init__(self, user_id, task_name, duration_estimate):
        """Create a task, given user_id and task name."""

        self.user_id = user_id
        self.task_name = task_name
        self.duration_estimate = duration_estimate

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                        nullable=False)
    task_name = db.Column(db.String(50), nullable=False)
    task_description = db.Column(db.String(100), nullable=True) # optional
    duration_estimate = db.Column(db.Integer, nullable=False) # in minutes
    duration_actual = db.Column(db.Integer, nullable=True) # in minutes

    gameplan_task = db.relationship("GameplanTask", uselist=False) # don't want a list, just one item

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Task task_id={self.task_id} task_name={self.task_name} user_id={self.user_id}>"


class GameplanTask(db.Model): #Twitter Employee (a special type of twitter user)
    """Task that is part of the gameplan for the morning."""
    # Like Twitter employer/user example. Gameplan tasks are a subset of Tasks. 
    # Can refer to current morning or the next day's morning. 

    __tablename__ = "gameplan"

    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), 
                        primary_key=True, 
                        nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    order = db.Column(db.Integer, unique=True)
    start_time = db.Columm(db.Datetime, unique=True)
    end_time = db.Column(db.Datetime, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<GameplanTask task_id={self.task_id} user_id={self.user_id}>"


class Category(db.Model):
    """Categories that tasks will belong to."""
    # This has a many to many relationship with tasks (tasks can have many 
    # categories and categories can have many tasks)
    # This is to help user add 'tags' to their tasks
    # will build more logic into this if time permits.
    # Category ideas: must-do, optional, one-off, repeating, default, mondays

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Category id={self.category_id} name={self.category_name}>"


class TaskCategory(db.Model):
    """Place to store tasks and what categories they belong to."""
    # Just an association table. Not a meaningful middle table. 
    # Like BookGenre table

    __tablename__ = "tasks_categories"

    tasks_categories_id = db.Column(db.Integer, autoincrement=true, primary_key=true)
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
    # Running this file interactively allows direct interaction w/ database."""

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

