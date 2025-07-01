#this is a file for the misc functions and views that it doesn't make sense to dedicate file structure to
import flask

bp = flask.Blueprint('other', __name__)

@bp.route('/other/contact')
def contact() :
    return flask.render_template('other/contact.html')

@bp.route('/') #the home page
def index() :  #get every design and every type and send those through to the index page
    return flask.render_template('base.html')