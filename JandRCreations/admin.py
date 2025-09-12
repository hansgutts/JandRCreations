from JandRCreations.db import (get_db)
from JandRCreations.auth import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, current_app
)
from JandRCreations.forms import *
import functools
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

#we dont want a way to register new admins here
#this will need to be done manually to ensure safety

#similar to the base website we have 4 pages
#home page to go to each form you want to update
#   a page with a form to input new items in to database for each page
#       design, type, and product. Need a page fore each to add a new one of any of those to the db

def require_login(view) : #make it be required for the user to be logged in
    @functools.wraps(view) #basic function wrapping
    def wrapped_view(**kwargs) :
        if g.admin is None : #if the admin user is not logged in

            return redirect(url_for('products.home')) #they go to the log in page
        
        return view(**kwargs)
    
    return wrapped_view #if they are loggged in continue as expected

@bp.route('/home') #this will be a simple page. button to go to the other three pages
@require_login #require them to be logged in
def admin_home() :
    return render_template('admin/home.html') #render the home page

@bp.route('/design', methods=('GET', 'POST')) #form to add a design into our database. relatively simple
@require_login #require them to be logged in
def admin_design() : 

    form = DesignForm(request.form) #get the form for adding a new design

    if request.method == 'POST' and form.validate() : #if posted and the form validates

        if create_design(form) < 0 : #create the form and make sure it succeeded
            flash("Error adding design") #if failed flash the errors
        else :
            return redirect(url_for('admin.admin_home'))

    return render_template('admin/design.html', form=form) #if no errors go to the home page

@bp.route('/type', methods=('GET', 'POST')) #form to add a type into our database. will need to reference a design
@require_login #log in
def admin_type() : 
    form = TypeForm(request.form) #get the form
    #fill in the choices for the form
    form.prod_design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 

    #some extra validation for image uploads are required
    if request.method == "POST" and form.validate() and request.files[form.type_image.name] and request.files[form.type_image.name].filename:

        if create_type(form, current_app) < 0 : #try and create the new type
            flash("Error adding type") #if it fails flash the errors
        else : #if it succeeds
            flash("Successfully added type") #success message
            
        return redirect(url_for('admin.admin_home')) #if succeeded go to the home page
    
    #if didn't succeed just go back to the form page
    return render_template('admin/type.html', form=form)

@bp.route('/product', methods=('GET', 'POST')) #form to add a product into our database. will need to reference type, and include adding customization options
@require_login #admin needs to be logged in to upload
def admin_product() : #page to add a product

    form = ProductForm(request.form) #create our new product form

    #generate the choices dynamically, (typeid, typename)
    form.type_id.choices = [(types["prod_type_id"], types['prod_type']) for types in get_all_types()]

    if request.method == "POST" and form.validate() : #if the form is submited
        if create_product(form, current_app) < 0 : #try and create the new type
            flash("Error adding product") #if it fails flash the errors
        else : #if it succeeds
            flash("Successfully added product") #success message
            return redirect(url_for("admin.admin_home"))

    return render_template('admin/product.html', form=form) #redirect to the product page on failure

@bp.route('/custom', methods=('GET', 'POST')) #form to add a product into our database. will need to reference type, and include adding customization options
@require_login #admin needs to be logged in to upload
def admin_custom() : #page to add customization to a product
    
    form = CustomForm(request.form)

    form.prod_id.choices = [(prod['prod_id'], prod['prod_name']) for prod in get_all_prods()]

    if request.method == 'POST' and form.validate() :
        if create_custom(form) < 0 :
            flash("Error adding customization")
        else :
            flash("Succesfully added customization (you still need to add options)")
            return redirect(url_for('admin.admin_home'))
        
    return render_template('admin/custom.html', form=form)

@bp.route('/option', methods=('GET', 'POST')) 
def admin_option() :

    form = OptionForm(request.form)

    form.custom_id.choices = [(option['custom_id'], option['custom'] + ' of ' + get_prod_by_prodid(get_prodid_by_customid(option['custom_id']))['prod_name']) for option in get_all_custom()]

    if request.method == 'POST' and form.validate() :
        if create_option(form) < 0 :
            flash('Error adding customization')
        else :
            flash("Successfully added customization. Don't forget to add ALL options")
            return redirect(url_for('admin.admin_home'))
        
    return render_template('admin/option.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate() :

         #open our admin db
        user = get_user_by_username(form.username.data)       

        #if there is no user matching the username input
        if user is None :
            return False #fail validation
        
        #otherwise check the password. hashed for security
        ###############NEED TO UNCOMMENT THIS AFTER TESTING#####################
        #elif not check_password_hash(user['user_password'], self.password) : 
        #    return False
        elif not user['userpassword'] == form.password.data :
            return False

        #if we get to the point we are logged in, store it in the session
        session['user_id'] = user['user_id']

        return redirect(url_for('admin.admin_home'))

    return render_template('admin/login.html', form=form)

@bp.before_app_request #load the admin user before the page is loaded
def load_admin_user() :
    user_id = session.get('user_id') #get the stored user id

    if user_id is None : #if the userid is none
        g.admin = None #we are not logged in
    else : #otherwise get user information
        g.admin = get_db().execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchone()['username']


    