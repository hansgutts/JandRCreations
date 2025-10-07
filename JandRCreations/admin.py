from JandRCreations.db import (get_db)
from JandRCreations.auth import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, current_app, jsonify
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

            return redirect(url_for('admin.login')) #they go to the log in page
        
        return view(**kwargs)
    
    return wrapped_view #if they are loggged in continue as expected

@bp.route('/home') #this will be a simple page. button to go to the other three pages
@require_login #require them to be logged in
def admin_home() :
    return render_template('admin/home.html') #render the home page

@bp.route('/design', methods=('GET', 'POST')) #form to add a design into our database. relatively simple
@require_login #require them to be logged in
def admin_design() : 

    addForm = DesignForm(request.form) #get the form for adding a new design
    addDeleteForm = AddDeleteForm(request.form) 
    deleteForm = DeleteDesign(request.form)

    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 

    return render_template('admin/design.html', addForm=addForm, deleteForm=deleteForm, addDeleteForm=addDeleteForm) #if no errors go to the home page

@bp.route('/add/design', methods=('POST',))
@require_login
def add_design() :
    addForm = DesignForm(request.form) #get the form for adding a new design

    if request.method == 'POST' and addForm.validate() : #if posted and the form validates

        if create_design(addForm) < 0 : #create the form and make sure it succeeded
            flash("Error adding design") #if failed flash the errors
        else :
            flash("Successfully added design")
    
    return redirect(url_for('admin.admin_home')) #if no errors go to the home page


@bp.route('/delete/design', methods=('POST',))
@require_login
def remove_design() :
    addForm = DesignForm(request.form) #get the form for adding a new design
    addDeleteForm = AddDeleteForm(request.form) 
    deleteForm = DeleteDesign(request.form)

    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 

    if request.method == 'POST' and deleteForm.validate() :
        if delete_design(deleteForm) < 0 :
            flash("Error deleting design")
        else :
            flash("Succesfully deleted design")
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 
    return redirect(url_for('admin.admin_home')) #if no errors go to the home page

@bp.route('/type', methods=('GET', 'POST')) #form to add a type into our database. will need to reference a design
@require_login #log in
def admin_type() :

    #initialize forms
    addDeleteForm = AddDeleteForm(request.form) 
    addForm = TypeForm(request.form) #get the form
    deleteForm = DeleteType(request.form)

    #fill in the choices for the form
    addForm.prod_design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    
    #if didn't succeed just go back to the form page
    return render_template('admin/type.html', addForm=addForm, deleteForm=deleteForm, addDeleteForm=addDeleteForm)

@bp.route('/add/type', methods=('GET', 'POST'))
@require_login
def add_type() :
    addForm = TypeForm(request.form)
    addForm.prod_design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 

     #some extra validation for image uploads are required
    if request.method == "POST" and addForm.validate() and request.files[addForm.type_image.name] and request.files[addForm.type_image.name].filename:

        if create_type(addForm, current_app) < 0 : #try and create the new type
            flash("Error adding type") #if it fails flash the errors
        else : #if it succeeds
            flash("Successfully added type") #success message
            
    return redirect(url_for('admin.admin_home')) #if succeeded go to the home page

@bp.route('delete/type', methods=("GET", "POST")) 
@require_login
def remove_type() :
    deleteForm = DeleteType(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]

    if request.method == "POST" and deleteForm.validate() :
        if delete_type(deleteForm) < 0 :
            flash("Error deleting type")
        else :
            flash("Successfully deleted type")

    return redirect(url_for('admin.admin_home'))

@bp.route('/product', methods=('GET', 'POST')) #form to add a product into our database. will need to reference type, and include adding customization options
@require_login #admin needs to be logged in to upload
def admin_product() : #page to add a product

    #initialize forms
    addDeleteForm = AddDeleteForm(request.form) 
    addForm = ProductForm(request.form) #get the form
    deleteForm = DeleteProduct(request.form)

    #generate the choices dynamically, (typeid, typename)
    addForm.type_id.choices = [(types["prod_type_id"], types['prod_type']) for types in get_all_types()]
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]


    return render_template('admin/type.html', addForm=addForm, deleteForm=deleteForm, addDeleteForm=addDeleteForm)

@bp.route('/add/prod', methods=('GET', 'POST'))
@require_login
def add_prod() :
    addForm = ProductForm(request.form) #get the form
    addForm.type_id.choices = [(types["prod_type_id"], types['prod_type']) for types in get_all_types()]

    if request.method == "POST" and addForm.validate() : #if the form is submited
        if create_product(addForm, current_app) < 0 : #try and create the new type
            flash("Error adding product") #if it fails flash the errors
        else : #if it succeeds
            flash("Successfully added product") #success message
    return redirect(url_for("admin.admin_home"))

@bp.route('/delete/prod', methods=("GET", "POST"))
@require_login
def remove_prod() :
    deleteForm = DeleteProduct(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    
    if request.method == "POST" and deleteForm.validate() :
        if delete_prod(deleteForm) < 0 :
            flash("Error deleting prod")
        else :
            flash("Successfully deleted prod")

    return redirect(url_for('admin.admin_home'))

@bp.route('/custom', methods=('GET', 'POST')) #form to add a product into our database. will need to reference type, and include adding customization options
@require_login #admin needs to be logged in to upload
def admin_custom() : #page to add customization to a product
    
    addForm = CustomForm(request.form)
    addDeleteForm = AddDeleteForm()
    deleteForm = DeleteCustom(request.form)

    addForm.prod_id.choices = [(prod['prod_id'], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]
        
    return render_template('admin/custom.html', addForm=addForm, deleteForm=deleteForm, addDeleteForm=addDeleteForm)

@bp.route('/add/custom', methods=("GET", "POST"))
@require_login
def add_custom() :
    addForm = CustomForm(request.form)

    addForm.prod_id.choices = [(prod['prod_id'], prod['prod_name']) for prod in get_all_prods()]

    if request.method == 'POST' and addForm.validate() :
        if create_custom(addForm) < 0 :
            flash("Error adding customization")
        else :
            flash("Succesfully added customization (you still need to add options)")
    
    return redirect(url_for('admin.admin_home'))


@bp.route('/delete/custom', methods=("GET", "POST"))
@require_login
def remove_custom() :
    deleteForm = DeleteCustom(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]

    if request.method == "POST" and deleteForm.validate() :
        if delete_cust(deleteForm) < 0 :
            flash("Error deleting customization")
        else :
            flash("Successfully deleted customization")

    return redirect(url_for('admin.admin_home'))

@bp.route('/option', methods=('GET', 'POST')) 
@require_login
def admin_option() :

    addForm = OptionForm(request.form)
    addDeleteForm = AddDeleteForm()
    deleteForm = DeleteOption()

    addForm.custom_id.choices = [(option['custom_id'], option['custom'] + ' of ' + get_prod_by_prodid(get_prodid_by_customid(option['custom_id']))['prod_name']) for option in get_all_custom()]
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]
    deleteForm.option_id.choices = [(option["options_id"], option["option_name"]) for option in get_all_options()]
        
    return render_template('admin/option.html', addForm=addForm, addDeleteForm=addDeleteForm, deleteForm=deleteForm)

@bp.route('/add/option', methods=("GET", "POST"))
@require_login
def add_option() :
    addForm = OptionForm(request.form)

    addForm.custom_id.choices = [(option['custom_id'], option['custom'] + ' of ' + get_prod_by_prodid(get_prodid_by_customid(option['custom_id']))['prod_name']) for option in get_all_custom()]
    

    if request.method == "POST" and addForm.validate() :
        if create_option(addForm) >= 0 :
            flash("Successfully added option")

        else :
            flash("Error adding option")

    return redirect(url_for('admin.admin_home'))

        

@bp.route('/delete/option', methods=("GET", "POST"))
@require_login
def remove_option() :
    deleteForm = DeleteOption(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]
    deleteForm.option_id.choices = [(option["options_id"], option["option_name"]) for option in get_all_options()]

    if request.method == "POST" and deleteForm.validate() :
        if delete_option(deleteForm) < 0 :
            flash("Error deleting customization option")
        else :
            flash("Successfully deleted customization option")

    return redirect(url_for('admin.admin_home'))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate() :

         #open our admin db
        user = get_user_by_username(form.username.data)   

        #if there is no user matching the username input
        if user is None :
            return render_template('admin/login.html', login_form=form) #fail validation
        
        #otherwise check the password. hashed for security
        ###############NEED TO UNCOMMENT THIS AFTER TESTING#####################
        #elif not check_password_hash(user['user_password'], self.password) : 
        #    return False
        elif not user['userpassword'] == form.password.data :
            return render_template('admin/login.html', login_form=form)

        #if we get to the point we are logged in, store it in the session
        session['user_id'] = user['user_id']

        return redirect(url_for('admin.admin_home'))

    return render_template('admin/login.html', login_form=form)

@bp.before_app_request #load the admin user before the page is loaded
def load_admin_user() :
    user_id = session.get('user_id') #get the stored user id

    if user_id is None : #if the userid is none
        g.admin = None #we are not logged in
    else : #otherwise get user information
        g.admin = get_db().execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchone()['username']

@bp.route('/get_types')
def get_types() :

    design_id = request.args.get('design_id')
    if design_id :
        design_id = int(design_id)

    types = get_types_by_design_id(design_id)
    if types :
        types = [{"id": id, "type":prod_type} for (id, prod_type) in types]
    
    return jsonify(types)

@bp.route('/get_prods') 
def get_prods() :

    type_id = request.args.get('type_id')
    if type_id :
        type_id = int(type_id)
    
    prods = get_prods_by_typeid(type_id)
    if prods :
        prods = [{'id': id, "prod":prod} for (id, prod) in prods]

    return jsonify(prods)

@bp.route('/get_customs')
def get_customs() :

    prod_id = request.args.get('prod_id')
    if prod_id :
        prod_id = int(prod_id)

    customs = get_cust_by_prodid(prod_id)

    if customs :
        customs = [{'id': cust['custom_id'], 'custom':cust['custom']} for cust in customs]

    return jsonify(customs)

@bp.route('/get_options')
def get_options() :

    custom_id = request.args.get('custom_id')
    if custom_id :
        custom_id = int(custom_id)

    options = get_options_by_custid(custom_id)

    if options :
        options = [{'id': option['options_id'], 'option':option['option_name']} for option in options]

    return options