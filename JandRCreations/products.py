from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from werkzeug.security import check_password_hash, generate_password_hash
from JandRCreations.db import get_db
from JandRCreations.auth import get_type_by_typeid
from JandRCreations.auth import get_prods_by_typeid
from JandRCreations.auth import get_prod_by_prodid
from JandRCreations.auth import get_design_by_designid
from JandRCreations.auth import get_cust_by_prodid
from JandRCreations.auth import get_options_by_custid

import sqlite3

bp = Blueprint('products', __name__,)

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
@bp.route('/<int:type>/view_type') #look at a specific type of product
def view_type(type) : #we need to get each product in each type, if it exists. ow send a 404 error
    type = get_type_by_typeid(type)

    prods = get_prods_by_typeid(type['prod_type_id'])
    
    prods = [get_prod_by_prodid(prodid[0]) for prodid in prods]

    if type is not None :    
        return render_template('products/type.html', type=type, prods=prods)#get_type_by_typeid(type)['prod_type']
    else :
        abort(404)

#the product view should show specific product information - pictures of this item, price, description, etc
@bp.route('/<int:product>/view_prod') #look at a specific product
def view_product(product): #get the information about the product, if it exists. ow send a 404 error
    prod = get_prod_by_prodid(product)

    #also need information regarding whether our product is customizable
    cust = get_cust_by_prodid(product)

    #and the options on the customizations
    #[{key:cust = value:[options]}] a bit weird but makes iteration a lot easier and logical later
    cust = {tempcust:get_options_by_custid(tempcust['custom_id']) for tempcust in cust}


    if prod is not None :
        return render_template('products/product.html', prod=prod, cust=cust)
    else :
        abort(404)