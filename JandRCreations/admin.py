from JandRCreations.db import (get_db)
from JandRCreations.auth import (get_user_by_username)
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from JandRCreations.forms import *
import functools

bp = Blueprint('admin', __name__, url_prefix='/admin')

#we dont want a way to register new admins here
#this will need to be done manually to ensure safety

#similar to the base website we have 4 pages
#home page to go to each form you want to update
#   a page with a form to input new items in to database for each page
#       design, type, and product. Need a page fore each to add a new one of any of those to the db

def require_login(view) :
    @functools.wraps(view)
    def wrapped_view(**kwargs) :
        if g.admin is None :

            return redirect(url_for('admin.login'))
        
        else :
            print(g.admin)
        
        return view(**kwargs)
    
    return wrapped_view

@bp.route('/home') #this will be a simple page. button to go to the other three pages
@require_login
def admin_home() :
    return render_template('admin/home.html')

@bp.route('/design') #form to add a design into our database. relatively simple
@require_login
def admin_design() :
    return render_template('admin/design.html')

@bp.route('/type') #form to add a type into our database. will need to reference a design
@require_login
def admin_type() :
    return render_template('admin/type.html')

@bp.route('/product') #form to add a product into our database. will need to reference type, and include adding customization options
@require_login
def admin_product() :
    return render_template('admin/product.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate() :

        return redirect(url_for('admin.admin_home'))

    return render_template('admin/login.html', form=form)

@bp.before_app_request
def load_admin_user() :
    user_id = session.get('user_id')

    if user_id is None :
        g.admin = None
    else :
        g.admin = get_db().execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchone()['username']


    