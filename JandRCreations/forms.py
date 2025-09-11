from wtforms import Form, RadioField, DecimalField, FileField, SubmitField, StringField, PasswordField, validators, SelectField
from flask import session
import sqlite3

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
        
       

        #validation successful
        return True
    
class DesignForm(Form) :
    design = StringField("Design Name", [validators.DataRequired()])
    submit = SubmitField("Submit")

class TypeForm(Form) :
    type_name = StringField("Type Name", [validators.DataRequired()])
    type_description = StringField("Type Description", [validators.DataRequired()])
    prod_design_id = SelectField("Corresponding Design", [validators.DataRequired()], choices=[])
    type_image = FileField("Upload an image")
    submit = SubmitField("Submit")

class ProductForm(Form) :
    type_id = SelectField("Corresponding Type", [validators.DataRequired()], choices=[])
    prod_name = StringField("Product Name", [validators.DataRequired()])
    prod_desc = StringField("Product Description", [validators.DataRequired()])
    prod_price = DecimalField("Product Price", places=2, validators=[validators.DataRequired()])
    prod_cost = DecimalField("Product Cost (how much it cost you)", places=2, validators=[validators.DataRequired()])
    prod_sold = RadioField("Has this been sold?", choices=[(True, "Yes"), (False,  "No")], default="no")
    prod_image = FileField("Upload an image")
    submit = SubmitField("Submit")

'''class CustomForm(ProductForm) :
    prod_id = SelectField("Corresponding product", [validators.DataRequired()], choices=[])
    custom_text = StringField("What are we customizing (ie color or size)", [validators.DataRequired()])
    custom_desc = StringField("Text for customization (customize your color)", [validators.DataRequired()])
    required = RadioField("Is this a required customization", choices=[("yes", True), ("no",  False)], default="no")
    cost_change = DecimalField("Price increase from customization", places=2, validators=[validators.DataRequired()])'''
