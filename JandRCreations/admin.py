from JandRCreations.db import (get_db)
from JandRCreations.auth import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, current_app, jsonify
)
from JandRCreations.forms import *
import functools
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin')

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

    #initialize forms needed to render the page
    addForm = DesignForm(request.form) 
    addDeleteForm = AddDeleteForm(request.form)  
    deleteForm = DeleteDesign(request.form)

    #dynamically set our delete form design_id choices
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 

    #render the admin design 
    return render_template('admin/design.html', addForm=addForm, deleteForm=deleteForm, addDeleteForm=addDeleteForm) #if no errors go to the home page

@bp.route('/add/design', methods=('POST',))
@require_login
def add_design() :

    #initialize the form for adding a design
    addForm = DesignForm(request.form) #get the form for adding a new design

    if request.method == 'POST' and addForm.validate() : #if posted and the form validates

        if create_design(addForm) < 0 : #create the form and make sure it succeeded
            flash("Error adding design") #if failed flash the errors
        else :  #it failed
            flash("Successfully added design") #let the user know it failed
    
    return redirect(url_for('admin.admin_home')) #if no errors go to the home page


@bp.route('/delete/design', methods=('POST',))
@require_login
def remove_design() : 

    #initialize the forms needed to render the page
    deleteForm = DeleteDesign(request.form)

    #dynamically load the delete form choices
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()] 

    #when the form is posted
    if request.method == 'POST' and deleteForm.validate() :
        if delete_design(deleteForm) < 0 : #attempt to delete the design
            flash("Error deleting design") #let the user know it suceeded
        else : 
            flash("Succesfully deleted design") #let the user know it failed
    
    #return the home page
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
    
    #initialize the form to add a type
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

    #initialize the delete form and populate the choices
    deleteForm = DeleteType(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]

    #make sure the form is submitted
    if request.method == "POST" and deleteForm.validate() :
        #try and delete the form
        if delete_type(deleteForm) < 0 :
            #let them know it failed
            flash("Error deleting type")
        else : #otherwise it suceeded
            flash("Successfully deleted type") #let the user know it suceeded

    #return to the home page
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


    return render_template('admin/product.html', addForm=addForm, deleteForm=deleteForm, addDeleteForm=addDeleteForm)

@bp.route('/add/prod', methods=('GET', 'POST'))
@require_login
def add_prod() :

    #initialize the forms
    addForm = ProductForm(request.form) #get the form
    addForm.type_id.choices = [(types["prod_type_id"], types['prod_type']) for types in get_all_types()]

    print(addForm.errors)
    if request.method == "POST" and addForm.validate() : #if the form is submited
        if create_product(addForm, current_app) < 0 : #try and create the new type
            flash("Error adding product") #if it fails flash the errors
        else : #if it succeeds
            flash("Successfully added product") #success message

    #return to the home page
    return redirect(url_for("admin.admin_home"))

@bp.route('/delete/prod', methods=("GET", "POST"))
@require_login
def remove_prod() :
    #initialize the delete form and populate it dynamically
    deleteForm = DeleteProduct(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    
    #if the form was submitted
    if request.method == "POST" and deleteForm.validate() :
        if delete_prod(deleteForm) < 0 : #if there was an error 
            flash("Error deleting prod") #let the user know it failed
        else :
            flash("Successfully deleted prod") #let the user know it suceeded
    #go to the home page
    return redirect(url_for('admin.admin_home'))


@bp.route('/custom', methods=('GET', 'POST')) #form to add a product into our database. will need to reference type, and include adding customization options
@require_login #admin needs to be logged in to upload
def admin_custom() : #page to add customization to a product
    
    #forms needed to render the page
    addForm = CustomForm(request.form)
    addDeleteForm = AddDeleteForm()
    deleteForm = DeleteCustom(request.form)

    #the dynamic form choices
    addForm.prod_id.choices = [(prod['prod_id'], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]
        
    #render the template
    return render_template('admin/custom.html', addForm=addForm, deleteForm=deleteForm, addDeleteForm=addDeleteForm)

@bp.route('/add/custom', methods=("GET", "POST"))
@require_login
def add_custom() :
    #the forms needed to render the page
    addForm = CustomForm(request.form)

    #make the choices dynamic
    addForm.prod_id.choices = [(prod['prod_id'], prod['prod_name']) for prod in get_all_prods()]

    #if the form was submitted
    if request.method == 'POST' and addForm.validate() :
        if create_custom(addForm) < 0 : #try and create the customization option
            flash("Error adding customization") #let the user know it failed
        else : #let the user know it failed
            flash("Succesfully added customization (you still need to add options)")
    
    #go to the home page
    return redirect(url_for('admin.admin_home'))


@bp.route('/delete/custom', methods=("GET", "POST"))
@require_login
def remove_custom() :
    #initialize the deletion form and make the choices dynamic
    deleteForm = DeleteCustom(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]

    #if the form was submitted
    if request.method == "POST" and deleteForm.validate() :
        if delete_cust(deleteForm) < 0 : #try and delete the customization
            flash("Error deleting customization") #let the user know whether or not it failed
        else : 
            flash("Successfully deleted customization")
    #go to the home page
    return redirect(url_for('admin.admin_home'))

@bp.route('/option', methods=('GET', 'POST')) 
@require_login
def admin_option() :
    #forms needed to render the page
    addForm = OptionForm(request.form)
    addDeleteForm = AddDeleteForm()
    deleteForm = DeleteOption()

    #make the choices dynamic
    addForm.custom_id.choices = [(option['custom_id'], option['custom'] + ' of ' + get_prod_by_prodid(get_prodid_by_customid(option['custom_id']))['prod_name']) for option in get_all_custom()]
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]
    deleteForm.option_id.choices = [(option["options_id"], option["option_name"]) for option in get_all_options()]
        
    #render the page
    return render_template('admin/option.html', addForm=addForm, addDeleteForm=addDeleteForm, deleteForm=deleteForm)

@bp.route('/add/option', methods=("GET", "POST"))
@require_login
def add_option() :

    #the form needed and dynamic
    addForm = OptionForm(request.form)
    addForm.custom_id.choices = [(option['custom_id'], option['custom'] + ' of ' + get_prod_by_prodid(get_prodid_by_customid(option['custom_id']))['prod_name']) for option in get_all_custom()]
    
    #if the form was submitted
    print(addForm.errors)
    if request.method == "POST" and addForm.validate() :
        if create_option(addForm) >= 0 : #try and create the option
            flash("Successfully added option") #let the user know whether it failed

        else :
            flash("Error adding option")

    #go to the home page
    return redirect(url_for('admin.admin_home'))

        

@bp.route('/delete/option', methods=("GET", "POST"))
@require_login
def remove_option() :
    #initialize the forms needed
    deleteForm = DeleteOption(request.form)
    deleteForm.design_id.choices = [(design["prod_design_id"], design['prod_design']) for design in get_all_designs()]
    deleteForm.type_id.choices = [(ptype["prod_type_id"], ptype["prod_type"]) for ptype in get_all_types()]
    deleteForm.product_id.choices = [(prod["prod_id"], prod['prod_name']) for prod in get_all_prods()]
    deleteForm.custom_id.choices = [(cust["custom_id"], cust['custom']) for cust in get_all_custom()]
    deleteForm.option_id.choices = [(option["options_id"], option["option_name"]) for option in get_all_options()]

    #if the form was submitted
    if request.method == "POST" and deleteForm.validate() :
        if delete_option(deleteForm) < 0 : #try and delete the option
            flash("Error deleting customization option") #let the user know whether or not they failed
        else :
            flash("Successfully deleted customization option")

    #go to the home page
    return redirect(url_for('admin.admin_home'))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    #create the log in form
    form = LoginForm(request.form)

    #if the form was submitted
    if request.method == 'POST' and form.validate() :
        #get the user name from the submitted form
        user = get_user_by_username(form.username.data) 
        #if there is no user matching the username input
        if user is None :
            flash('Something was incorrect, try again')
            return render_template('admin/login.html', login_form=form) #fail validation
            
        elif not check_password_hash(user['userpassword'], form.password.data) :
            
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

#these are our JS functions
@bp.route('/get_types') #get our types by a design id
def get_types() :
    #get the design id from the request
    design_id = request.args.get('design_id')
    if design_id : #if it was successfuly sent
        design_id = int(design_id) #make it an int

    types = get_types_by_design_id(design_id) #get the related types
    if types : #if types had valid data
        types = [{"id": id, "type":prod_type} for (id, prod_type) in types] #turn it into a dict
    
    return jsonify(types) #send it back

@bp.route('/get_prods')  #get prods by type
def get_prods() :
    #get type id from ajax request
    type_id = request.args.get('type_id')
    if type_id : #if the type id exists
        type_id = int(type_id) #make it an int
    
    #get the prods
    prods = get_prods_by_typeid(type_id)
    if prods : #if there are associated products
        prods = [{'id': id, "prod":prod} for (id, prod) in prods] #make them a dict

    return jsonify(prods) #send products back

@bp.route('/get_customs') #get customs by prod id
def get_customs() :
    #get prod id from AJAX
    prod_id = request.args.get('prod_id')
    if prod_id : #it the prod id exists
        prod_id = int(prod_id) #make it an int
    #get associated customization
    customs = get_cust_by_prodid(prod_id)
    #if there were associated customization
    if customs :
        #make them a dict
        customs = [{'id': cust['custom_id'], 'custom':cust['custom']} for cust in customs]

    return jsonify(customs) #send it back

@bp.route('/get_options') #get options from customization id
def get_options() :
    #get custom ids
    custom_id = request.args.get('custom_id')
    if custom_id : #if the custom id exists
        custom_id = int(custom_id) #make it an int

    options = get_options_by_custid(custom_id) #get the associated options

    if options : #if there are associated options
        #make it a dict
        options = [{'id': option['options_id'], 'option':option['option_name']} for option in options]

    return options #send options back to ajax