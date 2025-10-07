import sqlite3
import click
from flask import current_app, g

def get_db():  #get the db connection for other functions
    if 'db' not in g: #if its not already in g
        g.db = sqlite3.connect( #connect to the database and put it in g
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")

    return g.db #get the database out of g, will be in there now if it wasn't before

'''def get_admin_db() :
    if 'admin_db' not in g :
        g.admin_db = sqlite3.connect(
            current_app.config['ADMIN_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.admin_db.row_factory=sqlite3.PARSE_DECLTYPES

    return g.admin_db'''
    
def close_db(e=None) : #close the connection to the database

    #admindb = g.pop('admin_db', None) #we need to close the administrator db
    db = g.pop('db', None) #get the db out of g, pop it to delete

    if db is not None : #if the db was in g
        db.close() #close the db

    '''if admindb is not None :
        admindb.close()'''

def init_db() : #function to initialize the db
    db = get_db() #open the db

    with current_app.open_resource('schema.sql') as f: #open the sql file
        db.executescript(f.read().decode('utf8')) #run the sql file

'''def init_admin_db() : #function to initialize the db
    admin_db = get_admin_db() #open the db

    with current_app.open_resource('admin_schema.sql') as f: #open the sql file
        admin_db.executescript(f.read().decode('utf8')) #run the sql file'''

def init_app(app) : #function ot initialize the app
    app.teardown_appcontext(close_db) #add close_db to the functions to run when closing the app
    app.cli.add_command(init_db_command) #add a command line function to initialize the db. dont want to do it on website running as we don't want to reset the database every time
    #app.cli.add_command(init_admin_db_command)

@click.command('init-db') #create a command line interface command. this is the decorator for 'init-db'
def init_db_command(): #this is the actual function called
    init_db() #run the init_db function in this file
    click.echo('Initialized the database') #output for verification it completed

'''@click.command("init-admin-db")
def init_admin_db_command():
    init_admin_db()
    click.echo("Initialized the administrator database")'''