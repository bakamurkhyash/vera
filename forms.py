# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo



class LoginForm(FlaskForm):
    """
    Form for handling developer portal login via email and password.
    """
    
    email = EmailField('Email Address', 
        validators=[
            DataRequired("Email is required."),
            Email("Please enter a valid email address.")
        ],
        render_kw={"placeholder": "Email Address"} # Renders the HTML placeholder
    )
    
    
    password = PasswordField('Password', 
        validators=[
            DataRequired("Password is required.")
        ],
        render_kw={"placeholder": "Password"}
    )
    
    


class SignupForm(FlaskForm):
    """
    Form for creating a new developer account.
    """

    name = StringField('Full Name', 
        validators=[
            Optional(), # Allows the field to be empty
            Length(min=2, max=60)
        ],
        render_kw={"placeholder": "Full Name (Optional)"}
    )
    
   
    email = StringField('Email Address', 
        validators=[
            DataRequired("Email is required."),
            Email("Please enter a valid email address."),
        ],
        render_kw={"placeholder": "Email Address"}
    )
    
   
    password = PasswordField('Choose Password', 
        validators=[
            DataRequired("A password is required."),
            Length(min=8, message="Password must be at least 8 characters long.")
        ],
        render_kw={"placeholder": "Choose Password"}
    )
    
