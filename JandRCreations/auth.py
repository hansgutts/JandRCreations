#use this file for any validation we need to do
#ie if we need to make sure an entry in our db exists, just use something here
#off the top of my head, we will need to get designs, types, and products

import sqlite3
from JandRCreations.db import get_db
from flask import flash

def get_design(prod_design) :
    db = get_db()

    try :
        design = db.execute(
        'SELECT prod_design_id, prod_design FROM prod_design WHERE prod_design = ?',
        (prod_design,)
        ).fetchone()
        return design
    except Exception as e :
        flash(e)
        return None

def get_type(prod_type) :
    db = get_db()
    try :
        prod_type = db.execute(
            'SELECT prod_type_id, prod_type FROM prod_type WHERE prod_type = ?',
            (prod_type,)
        ).fetchone()
        return prod_type
    except :
        flash(e)
        return None

def get_product(prod_name) :
    db = get_db()
    try :
        prod = db.execute(
            'SELECT prod_id, prod_name, prod_description, prod_price, prod_cost, prod_sold FROM prod WHERE prod_name = ?',
            (prod_name,)
        ).fetchone()
        return prod
    except Exception as e:
        flash(e)
        return None