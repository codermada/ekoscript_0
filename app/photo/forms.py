from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired



class PhotoForm(FlaskForm):
    description = StringField('description', validators=[DataRequired()])
    file = FileField('', render_kw={'accept':'.png, .jpg'})
    upload = SubmitField('upload')