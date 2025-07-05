#this is a file for the misc functions and views that it doesn't make sense to dedicate file structure to
import flask

from JandRCreations.auth import get_types_by_designid
from JandRCreations.auth import get_all_designs
from JandRCreations.auth import get_type_by_typeid

bp = flask.Blueprint('other', __name__)

@bp.route('/other/contact')
def contact() :
    return flask.render_template('other/contact.html')

@bp.route('/') #the home page
def index() :  #get every design and every type and send those through to the index page
    
    designs = get_all_designs() #we need designs in our database to include it all in our home page
    designdict = {} #initialize our dictionary

    #this lets us go through designs and their respective types making it easier to populate home page
    #feels a little weird but stops me from making a million different functions to get info from db
    for design in designs : #go through all our designs and set the (key, value) pair as (design name, list of types with design name)
        designdict[design['prod_design']] = [get_type_by_typeid(id) for id in get_types_by_designid(design['prod_design_id'])]
    print(designdict)
    return flask.render_template('other/index.html', designdict=designdict) #render home page and send it the designs and types