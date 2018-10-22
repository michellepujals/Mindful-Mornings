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

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} username={self.username}>"



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

