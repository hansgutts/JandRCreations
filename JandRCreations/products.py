from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from werkzeug.security import check_password_hash, generate_password_hash
from JandRCreations.db import get_db
from JandRCreations.auth import get_types_by_designid
from JandRCreations.auth import get_type_by_typeid
from JandRCreations.auth import get_all_designs
from JandRCreations.auth import get_prods_by_typeid
from JandRCreations.auth import get_prod_by_prodid
from JandRCreations.auth import get_design_by_designid

import sqlite3

bp = Blueprint('products', __name__)

#there are three views I want to be able to distinguish
#the home page should default to viewing everything except individual products - I want a section for each design, and a subsection for each type



#the design view should show only types of products within that design - right now either custom made or premade
@bp.route('/<design>/view_design') #look at a specific design a
def view_design(design) : #we need to get the specific designs types, if it exists. ow send a 404 error
    design = get_design_by_designid(design)
    if design is not None :
        return render_template('products/design.html', design=design)
    else :
        abort(404)

#the type view should show only types of products within that type - so wreaths, bracelets, etc
@bp.route('/<type>/view_type') #look at a specific type of product
def view_type(type) : #we need to get each product in each type, if it exists. ow send a 404 error
    return get_type_by_typeid(type)['prod_type']

#the product view should show specific product information - pictures of this item, price, description, etc
@bp.route('/<product>/view_prod') #look at a specific product
def view_product(product): #get the information about the product, if it exists. ow send a 404 error
    return get_prod_by_prodid(product)['prod_name']