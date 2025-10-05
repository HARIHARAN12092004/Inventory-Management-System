from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from models import Location

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[Optional()])
    sku = StringField('SKU', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[Optional()])
    submit = SubmitField('Submit')
    
    def validate_name(self, field):
        location = Location.query.filter(Location.name == field.data).first()
        if location:
            # If we're editing a location, it's okay if the name is the same as the current location
            if not hasattr(self, '_obj') or (hasattr(self, '_obj') and self._obj.location_id != location.location_id):
                raise ValidationError('A location with this name already exists.')

class ProductMovementForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    from_location_id = SelectField('From Location', coerce=int, validators=[Optional()])
    to_location_id = SelectField('To Location', coerce=int, validators=[Optional()])
    qty = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def validate(self):
        if not super(ProductMovementForm, self).validate():
            return False
        
        # Either from_location or to_location must be specified
        if self.from_location_id.data == 0 and self.to_location_id.data == 0:
            self.from_location_id.errors.append('Either From Location or To Location must be specified')
            return False
            
        # Cannot have same from and to location
        if self.from_location_id.data != 0 and self.to_location_id.data != 0:
            if self.from_location_id.data == self.to_location_id.data:
                self.to_location_id.errors.append('From Location and To Location cannot be the same')
                return False
                
        return True