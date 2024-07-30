from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InsertPondForm(FlaskForm):
    pond_name = StringField('Pond Name', validators=[DataRequired()])
    location = StringField('Location')
    submit = SubmitField('Submit')