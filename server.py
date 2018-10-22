"""File that deals with server."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, 
                    session, Markup)

from flask_debugtoolbar import DebugToolbarExtension

from model import * 


app = Flask(__name__) # this is the instance of the flask application

app.secret_key = "ABC" # Required to use Flask sessions and debug toolbar

app.jinja_env.undefined = StrictUndefined # Raises error for undefined vars


## create all the routes here #########################################
## @app.route('/')
    #def index():
    #"""Homepage.""" 