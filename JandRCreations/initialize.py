import os
from flask import Flask, url_for

def create_app(test_config=None) : #create the flask app

    app = Flask(__name__, instance_relative_config=True) #initialize the app

    app.config.from_mapping( #set the config information. this should be in its own config file
        SECRET_KEY = 'dev', #this is a key to be used for encryption and shouldn't be able to be accessed by anyone else. also shouldn't be 'dev' at launch
        DATABASE = os.path.join(app.instance_path, 'JandRCreations.sqlite'), #where the db is stored
        IMAGES = os.path.join(app.static_folder, 'images/')
        #ADMIN_DATABASE = os.path.join(app.instance_path, 'admin.sqlite')
    )

    if test_config is None: #if we aren't testing
        app.config.from_pyfile('config.py', silent=True) #use the development config file
    else : #if we are testing
        app.config.from_mapping(test_config) #use the test_config file

    try:
        os.makedirs(app.instance_path) #
    except OSError :
        pass

    from JandRCreations import db #import our db file
    db.init_app(app) #use the init_app function in db

    from JandRCreations import products #register our blueprints with the app
    app.register_blueprint(products.bp)

    from JandRCreations import other
    app.register_blueprint(other.bp)

    from JandRCreations import admin
    app.register_blueprint(admin.bp)

    app.add_url_rule('/', endpoint='index') #the base page with no added paths should go to our index page. easier than a decorator function

    return app