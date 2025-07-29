#use this file for any validation we need to do
#ie if we need to make sure an entry in our db exists, just use something here
#off the top of my head, we will need to get designs, types, and products

import sqlite3
from JandRCreations.db import get_db
from flask import flash
#from JandRCreations.db import get_admin_db
from flask import g
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import functools

from werkzeug.security import check_password_hash, generate_password_hash

####NEED TO UPDATE THESE TO PROTECT INPUTS IN THE FUTURE JUST TO BE SAFE########

def get_all_designs() : #I want to get design id and name for all designs
    db = get_db() #connect

    #get the data, leaving it in the dict (row) so its more readable in the future
    designs = db.execute('SELECT prod_design_id, prod_design FROM prod_design').fetchall()

    return designs

def get_design_by_designid(designid) : #get design the design by the id, simply returns the design name
    db = get_db() #connect

    if not (type(designid) is int) : #avoid SQL injection
        return None

    #get the design name where design id matches input
    design = db.execute('SELECT prod_design FROM prod_design WHERE prod_design_id = ?', (designid,)).fetchone()['prod_design']

    return design

def get_types_by_designid(designid) : #get the types that fall under a certain design
    db = get_db() #connect

    if not (type(designid) is int) : #avoid SQL injection
        return None

    #get the ids of the types then get it in a list of ids rather than a list of sql dict rows
    typeIDs = db.execute('SELECT prod_type_id, prod_type  FROM prod_type where prod_design_id = ?', (designid,)).fetchall()
    typeIDs = [row['prod_type_id'] for row in typeIDs]

    return typeIDs

def get_type_by_typeid(typeid) : #get type info from the id
    db = get_db() #connect

    if not (type(typeid) is int) : #avoid SQL injection
        return None

    #get the type and description from the db. leave it in a dict to make future access more logical
    types = db.execute('SELECT prod_type_id, prod_type, prod_type_description FROM prod_type WHERE prod_type_id = ?', (typeid,)).fetchone()

    return types

def get_prods_by_typeid(typeid) : #get the products that full under a certain type

    db = get_db() #connect

    if not (type(typeid) is int) : #avoid SQL injection
        return None

    #get the prod info where the type id matches the input. get it a list of ids rather than a list of sql rows
    prods = db.execute('SELECT prod_id FROM prod WHERE prod_type_id = ?', (typeid,)).fetchall()
    prods = [row['prod_id'] for row in prods]

    return prods

def get_prod_by_prodid(prodid) : #get the prod by id
    db = get_db() #connect

    if not (type(prodid) is int) : #avoid SQL injection
        return None

    #get the prod info where the prod id matched the input. leave it in dict to make future access more logical 
    prod = db.execute('SELECT prod_id, prod_name, prod_description, prod_price, prod_cost, prod_sold FROM prod WHERE prod_id = ?', (prodid,)).fetchone()

    return prod

def get_cust_by_prodid(prodid) : #get customization sections based on prodid
    db = get_db() #open the db

    if not (type(prodid) is int) : #make sure our prodid is an int (avoid sql injection)
        return None
    
    #get all fields from custom table, makes it easier later since this works the same as a dict
    cust = db.execute('SELECT * FROM custom WHERE custom.prod_id = ?', (prodid,)).fetchall()

    return cust

def get_options_by_custid(custid) : #need to get options for the customization
    db = get_db() #connect

    if not (type(custid) is int) :
        return None #avoid sql injection
    
    options = db.execute('SELECT * FROM options WHERE options.custom_id = ?', (custid,)).fetchall()

    return options

def get_user_by_username(username) :

    admin_db = get_db() #connect

    return admin_db.execute('SELECT * FROM user WHERE user.username = ?', (username,)).fetchone()
        