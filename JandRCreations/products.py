from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from JandRCreations.db import get_db

import sqlite3

bp = Blueprint('products', __name__, url_prefix='/auth')

#there are three views I want to be able to distinguish
#the home page should default to viewing everything except individual products - I want a section for each design, and a subsection for each type

@bp.route('/') #the home page
def index() :  #get every design and every type and send those through to the index page
    pass

#the design view should show only types of products within that design - right now either custom made or premade
@bp.route('<design>/view_design') #look at a specific design a
def view_design() : #we need to get the specific designs types, if it exists. ow send a 404 error
    pass

#the type view should show only types of products within that type - so wreaths, bracelets, etc
@bp.route('<type>/view_type') #look at a specific type of product
def view_type() : #we need to get each product in each type, if it exists. ow send a 404 error
    pass

#the product view should show specific product information - pictures of this item, price, description, etc
@bp.route('<product>/view_product') #look at a specific product
def view_product(): #get the information about the product, if it exists. ow send a 404 error
    pass