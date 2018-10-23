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

    
class Task(db.Model):
    """Tasks owned by users of Mindful Mornings website."""

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

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Task task_id={self.task_id} task_name={self.task_name} user_id={self.user_id}>"



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

