# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

## NOTE: For a real app, you would also define custom validators (e.g., CheckIfEmailExists)
## and use a more secure Length for passwords (e.g., min=12).

class LoginForm(FlaskForm):
    """
    Form for handling developer portal login via email and password.
    """
    # Corresponds to: <input type="email" name="email" ...>
    email = EmailField('Email Address', 
        validators=[
            DataRequired("Email is required."),
            Email("Please enter a valid email address.")
        ],
        render_kw={"placeholder": "Email Address"} # Renders the HTML placeholder
    )
    
    # Corresponds to: <input type="password" name="password" ...>
    password = PasswordField('Password', 
        validators=[
            DataRequired("Password is required.")
        ],
        render_kw={"placeholder": "Password"}
    )
    
    # NOTE: The HTML button is custom styled, so we won't use a standard SubmitField
    # submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    """
    Form for creating a new developer account.
    """
    # Corresponds to: <input type="text" name="name" ...>
    # Made optional as per your HTML (Optional)
    name = StringField('Full Name', 
        validators=[
            Optional(), # Allows the field to be empty
            Length(min=2, max=60)
        ],
        render_kw={"placeholder": "Full Name (Optional)"}
    )
    
    # Corresponds to: <input type="email" name="email" ...>
    email = StringField('Email Address', 
        validators=[
            DataRequired("Email is required."),
            Email("Please enter a valid email address."),
        ],
        render_kw={"placeholder": "Email Address"}
    )
    
    # Corresponds to: <input type="password" name="password" ...>
    password = PasswordField('Choose Password', 
        validators=[
            DataRequired("A password is required."),
            Length(min=8, message="Password must be at least 8 characters long.")
        ],
        render_kw={"placeholder": "Choose Password"}
    )
    
    # NOTE: You might also add a 'confirm_password' field with EqualTo validator 
    # for production use, but it's omitted here to match the current HTML structure.