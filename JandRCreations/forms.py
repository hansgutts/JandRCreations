from wtforms import Form, RadioField, DecimalField, FileField, SubmitField, StringField, PasswordField, validators, SelectField
from flask import session
import sqlite3

#we need a log in form for our admin page

class AddDeleteForm(Form) :
    addDelete = RadioField("Are you adding or deleting", choices=[('Add', "Add"), ('Delete',  "Delete")], default="Add", id='add_delete')

class LoginForm(Form):
    #the fields of our form
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Log In')
    
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

class CustomForm(Form) :
    prod_id = SelectField("Corresponding product", [validators.DataRequired()], choices=[])
    custom_text = StringField("What are we customizing (ie color or size)", [validators.DataRequired()])
    custom_desc = StringField("Text for customization (customize your color)", [validators.DataRequired()])
    required = RadioField("Is this a required customization", choices=[(True, "Yes"), (False,  "No")], default="no")
    submit = SubmitField("Submit")

class OptionForm(Form) :
    custom_id = SelectField("Corresponding customization", [validators.DataRequired()], choices=[])
    option_name = StringField("Name of option (red, blue)", [validators.DataRequired()])
    cost_change = DecimalField("Price increase", places=2, validators=[validators.DataRequired()])
    submit = SubmitField("Submit")

class DeleteDesign(Form) :
    design_id = SelectField('Delete design', choices=[], validators=[validators.DataRequired()])
    submit = SubmitField('Delete')

class DeleteType(Form) :
    design_id = SelectField('Narrow down by design', choices=[])
    type_id = SelectField('Delete type', choices=[], validators=[validators.DataRequired()])
    submit = SubmitField('Delete')

class DeleteProduct(Form) :
    design_id = SelectField('Narrow down by design', choices=[])
    type_id = SelectField('Narrow by type', choices=[])
    product_id = SelectField('Delete product', choices=[], validators=[validators.DataRequired()])
    submit = SubmitField('Delete')

class DeleteCustom(Form) :
    design_id = SelectField('Narrow down by design', choices=[])
    type_id = SelectField('Narrow by type', choices=[])
    product_id = SelectField('Narrow by product', choices=[])
    custom_id = SelectField('Delete custom', choices=[], validators=[validators.DataRequired()])
    submit = SubmitField('Delete')

class DeleteOption(Form) :
    design_id = SelectField('Narrow down by design', choices=[])
    type_id = SelectField('Narrow down by type', choices=[])
    product_id = SelectField('Narrow down by product', choices=[])
    custom_id = SelectField('Narrow down by custom', choices=[])
    option_id = SelectField('Delete option', choices=[], validators=[validators.DataRequired()])
    submit = SubmitField('Delete')

class addDeleteForm(Form) :
    addDelete = RadioField('Add or Delete', choices=[('Add', 'Add'), ('Delete', 'Delete')], id='add_delete_field', default='Add')