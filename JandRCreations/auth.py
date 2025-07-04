#use this file for any validation we need to do
#ie if we need to make sure an entry in our db exists, just use something here
#off the top of my head, we will need to get designs, types, and products

import sqlite3
from JandRCreations.db import get_db
from flask import flash

####NEED TO UPDATE THESE TO PROTECT INPUTS IN THE FUTURE JUST TO BE SAFE########

def get_all_designs() : #I want to get design id and name for all designs
    db = get_db() #connect

    #get the data, leaving it in the dict (row) so its more readable in the future
    designs = db.execute('SELECT prod_design_id, prod_design FROM prod_design').fetchall()

    return designs

def get_design_by_designid(designid) : #get design the design by the id, simply returns the design name
    db = get_db() #connect

    #get the design name where design id matches input
    design = db.execute('SELECT prod_design FROM prod_design WHERE prod_design_id = ?', (designid,)).fetchone()['prod_design']

    return design

def get_types_by_designid(designid) : #get the types that fall under a certain design
    db = get_db() #connect

    #get the ids of the types then get it in a list of ids rather than a list of sql dict rows
    typeIDs = db.execute('SELECT prod_type_id, prod_type  FROM prod_type where prod_design_id = ?', (designid,)).fetchall()
    typeIDs = [row['prod_type_id'] for row in typeIDs]

    return typeIDs

def get_type_by_typeid(typeid) : #get type info from the id
    db = get_db() #connect

    #get the type and description from the db. leave it in a dict to make future access more logical
    types = db.execute('SELECT prod_type_id, prod_type, prod_type_description FROM prod_type WHERE prod_type_id = ?', (typeid,)).fetchone()

    return types

def get_prods_by_typeid(typeid) : #get the products that full under a certain type

    db = get_db() #connect

    #get the prod info where the type id matches the input. get it a list of ids rather than a list of sql rows
    prods = db.execute('SELECT prod_id FROM prod WHERE prod_type_id = ?', (typeid,)).fetchall()
    prods = [row['prod_id'] for row in prods]

    return prods

def get_prod_by_prodid(prodid) : #get the prod by id
    db = get_db() #connect

    #get the prod info where the prod id matched the input. leave it in dict to make future access more logical 
    prod = db.execute('SELECT prod_id, prod_name, prod_description, prod_price, prod_cost, prod_sold FROM prod WHERE prod_id = ?', (prodid,)).fetchone()

    return prod