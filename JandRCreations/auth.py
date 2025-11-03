#use this file for any validation we need to do
#ie if we need to make sure an entry in our db exists, just use something here
#off the top of my head, we will need to get designs, types, and products

import sqlite3
from sqlite3 import IntegrityError
import wtforms
import os
from JandRCreations.db import get_db
#from JandRCreations.db import get_admin_db
from flask import g
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
import functools
import flask

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

#our database has essentially a hierarchy from highest to lowest, design -> type -> product -> custom -> option
#a design has types, types have products, products have customization, customizations have options
#using the placeholder ? in our insertion actually prevents sql injection. not much data cleaning needed

def get_all_designs() : #get all design elements
    db = get_db() #connect

    #get the data, leaving it in the dict (row) so its more readable in the future
    designs = db.execute('SELECT prod_design_id, prod_design FROM prod_design').fetchall()

    return designs

def get_all_types() : #get all type elements
    db = get_db() #connect

    #get the value neededs
    types = db.execute('SELECT prod_type_id, prod_type FROM prod_type').fetchall()

    return types

def get_all_prods() : #get all prod elements
    db = get_db() #connect

    #get the prods
    prods = db.execute("SELECT prod_id, prod_name FROM prod").fetchall()
    return prods


def get_all_custom() :#get all custom elements
    db = get_db()

    options = db.execute("SELECT custom_id, custom FROM custom").fetchall()
    return options

def get_all_options() : #get all options
    db = get_db()

    options = db.execute("SELECT options_id, option_name FROM options").fetchall()
    return options


def get_design_by_designid(designid) : #get design the design by the id, simply returns the design name
    db = get_db() #connect

    if not (type(designid) is int) : #avoid SQL injection
        return []

    #get the design name where design id matches input
    design = db.execute('SELECT prod_design FROM prod_design WHERE prod_design_id = ?', (designid,)).fetchone()

    return design

def get_types_by_designid(designid) : #get the types that fall under a certain design
    db = get_db() #connect

    if not (type(designid) is int) : #avoid SQL injection
        return []

    #get the ids of the types then get it in a list of ids rather than a list of sql dict rows
    typeIDs = db.execute('SELECT prod_type_id, prod_type  FROM prod_type where prod_design_id = ?', (designid,)).fetchall()
    typeIDs = [row['prod_type_id'] for row in typeIDs]

    return typeIDs

def get_type_by_typeid(typeid) : #get type info from the id
    db = get_db() #connect

    if not (type(typeid) is int) : #avoid SQL injection
        return []

    #get the type and description from the db. leave it in a dict to make future access more logical
    types = db.execute('SELECT prod_type_id, prod_type, prod_type_description, prod_type_image FROM prod_type WHERE prod_type_id = ?', (typeid,)).fetchone()

    return types

def get_prods_by_typeid(typeid) : #get the products that full under a certain type

    db = get_db() #connect

    if not (type(typeid) is int) : #avoid SQL injection
        return []

    #get the prod info where the type id matches the input. get it a list of ids rather than a list of sql rows
    prods = db.execute('SELECT prod_id, prod_name FROM prod WHERE prod_type_id = ?', (typeid,)).fetchall()
    prods = [(row['prod_id'], row['prod_name']) for row in prods]
 

    return prods

def get_prod_by_prodid(prodid) : #get the prod by id
    db = get_db() #connect

    if not (type(prodid) is int) : #avoid SQL injection
        return []

    #get the prod info where the prod id matched the input. leave it in dict to make future access more logical 
    prod = db.execute('SELECT prod_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image FROM prod WHERE prod_id = ?', (prodid,)).fetchone()

    return prod

#get the prodid from the customization id
def get_prodid_by_customid(id) :
    db = get_db()

    try :
        prod = db.execute("SELECT prod_id FROM custom WHERE custom_id = ?", (id,)).fetchone()['prod_id']
        return prod
    except Exception as e :
        return -1

def get_cust_by_prodid(prodid) : #get customization sections based on prodid
    db = get_db() #open the db

    if not (type(prodid) is int) : #make sure our prodid is an int (avoid sql injection)
        return []
    
    #get all fields from custom table, makes it easier later since this works the same as a dict
    cust = db.execute('SELECT * FROM custom WHERE custom.prod_id = ?', (prodid,)).fetchall()
    return cust

def get_options_by_custid(custid) : #need to get options for the customization
    db = get_db() #connect

    if not (type(custid) is int) :
        return [] #avoid sql injection
    
    options = db.execute('SELECT * FROM options WHERE options.custom_id = ?', (custid,)).fetchall()

    return options

def get_user_by_username(username) : #get our user by the user name provided

    admin_db = get_db() #connect

    return admin_db.execute('SELECT * FROM user WHERE user.username = ?', (username,)).fetchone()
        
def create_design(form) : #create a design element from provided form

    design_values = tuple_form(form) #turn it into tuples for insertion

    db = get_db() #connect
 
    try : #protect failure
        db.execute("INSERT INTO prod_design (prod_design) VALUES (?)", design_values)
        db.commit()
        return 0
    except IntegrityError as e : #integrity error is not caught by exception. cusotm handling for that error
        flash("Error entry already exists") #let the user know they are trying to make a duplicate
        return -1 
    except Exception as e: #otherwise print generic error and return failure
        db.rollback()
        return -1
    
def create_type(form, my_app) : #create a type element from provided form
    db = get_db()
    try : #protect from sql failure
        

        #image handline
        image = request.files[form.type_image.name]
        image_name = form.type_name.data + image.filename[-4:]
        form.type_image.data = image_name

        #get values in tuple format
        type_values = tuple_form(form)
        #save the image
        image.save(my_app.config['IMAGES'] + image_name)
        #save it
        db.execute("INSERT INTO prod_type (prod_type, prod_type_description, prod_design_id, prod_type_image) VALUES (?, ?, ?, ?)", type_values)
        db.commit()
        return 0
    except IntegrityError as e : #error handling. print error and return failure (-1)
        flash("Error entry already exists")
        return -1 

    except Exception as e :
        db.rollback()
        return -1
    
def create_product(form, my_app) : #create product

    db = get_db()
    try : #protect against sql failure
        
        #image handling =
        image = request.files[form.prod_image.name]
        image_name = form.prod_name.data + image.filename[-4:]
        form.prod_image.data = image_name
        #get values in tuple format
        product_tuple = tuple_form(form)
        #save the image
        image.save(my_app.config['IMAGES'] + image_name)

        db.execute("INSERT INTO prod (prod_type_id, prod_name, prod_description, prod_price, prod_cost, prod_sold, prod_image) VALUES (?, ?, ?, ?, ?, ?, ?)", product_tuple)
        db.commit()

        return 0
    except IntegrityError as e : #error handling. print error and return failure (-1)
        flash("Error entry already exists")
        return -1 
    except Exception as e :
        
        db.rollback()
        return -1
    
def create_custom(form) : #create customization element
    db = get_db() 
    try : #protect against sql failure
        
        #get value in tuple format
        custom_tuple = tuple_form(form)

        db.execute("INSERT INTO custom (prod_id, custom, custom_desc, require) VALUES (?, ?, ?, ?)", custom_tuple)
        db.commit()
        return 0
    except IntegrityError as e : #error handling. print error and return failure (-1)
        flash("Error entry already exists")
        return -1 
    except Exception as e :
        
        db.rollback()
        return -1

def create_option(form) : #create an option form
    db = get_db()
    try : #protect against sql failure
        
        #get it in tuple format
        option_tuple = tuple_form(form)    

        db.execute('INSERT INTO options (custom_id, option_name, cost_change) VALUES (?, ?, ?)', option_tuple)
        db.commit()
        return 0        
    except IntegrityError as e : #error handling. print error and return failure (-1)
        flash("Error entry already exists")
        return -1 
    except Exception as e:
        
        db.rollback()
        return -1

def delete_design(form) : #delete design based on id
    db = get_db()
    try : # protect against sql failure

        #delete the design
        db.execute('DELETE FROM prod_design WHERE prod_design_id=?', (form.design_id.data,))
        db.commit()

        return 0
    except IntegrityError as e : #error handling. print the error and return failure (-1)
        flash("Error entry needed for database integrity")
        return -1 
    except Exception as e :
        
        db.rollback()
        return -1
    
def delete_type(form) : #delete the type based on type id
    
    db = get_db() 
    try : #protect against sql failure
        
        #delete the type
        db.execute('DELETE FROM prod_type WHERE prod_type_id=?', (form.type_id.data,))
        db.commit() 

        return 0
    except IntegrityError as e : #error handling. print error and return failure (-1)
        flash("Error entry needed for database integrity")
        return -1 
    except Exception as e :
        
        db.rollback()
        return -1
    
def delete_prod(form) :
    
    db = get_db()
    try : #protect against sql failure
        
        #delete the product from prod id
        db.execute('DELETE from prod WHERE prod_id=?', (form.product_id.data,))
        db.commit()

        return 0
    except IntegrityError as e : #error handling. print the error and return failure (-1)
        flash("Error entry needed for database integrity")
        return -1 
    except Exception as e :
        
        db.rollback()
        return -1
    
def delete_cust(form) : #delete customization based on id
    db = get_db()
    try : #protect against sql failure
        
        #delete the customization
        db.execute("DELETE from custom WHERE custom_id=?", (form.custom_id.data,))
        db.commit()

        return 0
    except IntegrityError as e : #error handling. print error and return failure (-1)
        flash("Error entry needed for database integrity")
        return -1 
    except Exception as e :
        
        db.rollback()
        return -1
    
def delete_option(form) : #delete option based on id
    db = get_db()
    try : #protect agianst sql failure

        #delete the option
        db.execute("DELETE from options WHERE options_id=?", (form.option_id.data,))
        db.commit()

        return 0
    except IntegrityError as e : #error handling. print error and return failure (-1)
        flash("Error entry needed for database integrity")
        return -1 
    except Exception as e :
        
        db.rollback()
        return -1

def tuple_form(form) : #tuple our form data
    #we don't need submit field data
    return tuple(field.data if not field.type == "DecimalField" else float(field.data) for field in form if not field.id == "submit")

def get_types_by_design_id(designid) : #get the type by design
    db = get_db()

    #join the two tables
    types = db.execute('SELECT prod_type.prod_type_id, prod_type.prod_type FROM prod_design JOIN prod_type ON prod_type.prod_design_id = prod_design.prod_design_id WHERE prod_type.prod_design_id = ?', (designid,)).fetchall()
    #get the type id and type description in a list
    ptypes = [(ptype['prod_type_id'], ptype['prod_type']) for ptype in types]
    
    return ptypes #return the list