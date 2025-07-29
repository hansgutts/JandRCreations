from wtforms import Form, SubmitField, StringField, PasswordField, validators
from flask import session
import sqlite3
from JandRCreations.auth import (get_user_by_username)

#we need a log in form for our admin page
class LoginForm(Form):
    #the fields of our form
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Log In')

    #we need a little more validation since we are logging in
    def validate(self):

        #make sure base level validation is clear
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        
        #open our admin db
        user = get_user_by_username(self.username.data)       

        #if there is no user matching the username input
        if user is None :
            return False #fail validation
        
        #otherwise check the password. hashed for security
        ###############NEED TO UNCOMMENT THIS AFTER TESTING#####################
        #elif not check_password_hash(user['user_password'], self.password) : 
        #    return False
        elif not user['userpassword'] == self.password.data :
            return False

        #if we get to the point we are logged in, store it in the session
        session['user_id'] = user['user_id']

        #validation successful
        return True



