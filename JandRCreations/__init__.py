import os
from flask import Flask, url_for

def create_app(test_config=None) :

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'JandRCreations.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else :
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError :
        pass

    from . import db
    db.init_app(app)

    from . import products
    app.register_blueprint(products.bp)

    from . import other
    app.register_blueprint(other.bp)

    app.add_url_rule('/', endpoint='index')
    
    
    #@app.route("/")
    #def route_to_index() :
    #    app.redirect(url_for('index')) #if I have a index function defined somewhwere this will make it so 'app/' url will take us to 'app/index' url

    return app

