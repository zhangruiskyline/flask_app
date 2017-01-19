from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)