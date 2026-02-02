# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import func

# Initialize SQLAlchemy object (it will be linked to the Flask app later)
db = SQLAlchemy()

class Developer(db.Model, UserMixin):
    """
    Represents a Developer user in the application, linked to an Auth0 identity.
    """
    __tablename__ = 'developers'

    # Primary Key
    developer_id = db.Column(db.Integer, primary_key=True)
    
    # Auth0 Link (REQUIRED for lookup after Auth0 authentication)
    auth0_user_id = db.Column(db.String(255), unique=True, nullable=False)
    
    # User Details
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    tier = db.Column(db.String(50), default='Starter', nullable=False)

    # Relationships: Define back references
    keys = db.relationship('APIKey', backref='developer', lazy=True)
    logs = db.relationship('UsageLog', backref='developer', lazy=True)

    def __repr__(self):
        return f"<Developer {self.email} (Auth0 ID: {self.auth0_user_id})>"
    #for overriding get_id() that usermixin calls and throws an error if the column name isnt id
    def get_id(self):
        return str(self.developer_id)


class APIKey(db.Model, UserMixin):
    """
    Stores API keys assigned to developers. We store the hash, not the plain key.
    """
    __tablename__ = 'api_keys'

    # Primary Key
    key_id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key relationship to Developer
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.developer_id'), nullable=False)
    
    # Key details
    api_key_hash = db.Column(db.String(255), unique=True, nullable=False) # Store SHA-256 hash
    key_prefix = db.Column(db.String(50), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return f"<APIKey {self.key_prefix} active:{self.is_active}>"
    
    def get_id(self):
        return str(self.key_id)


class UsageLog(db.Model, UserMixin):
    """
    Records every API request for analytics and billing purposes.
    """
    __tablename__ = 'usage_logs'

    # Primary Key
    log_id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key relationship to Developer
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.developer_id'), nullable=False)
    
    # Log Details
    endpoint = db.Column(db.String(100), nullable=False)
    latency_ms = db.Column(db.Integer)
    status_code = db.Column(db.Integer, nullable=False)
    
    # Metadata
    requested_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return f"<UsageLog {self.endpoint} @ {self.requested_at}>"
    
    def get_id(self):
        return str(self.log_id)
    

#Table for Requests recieved on FAPI
class RequestLog(db.Model, UserMixin):
    """
    Records every API request  and stores the source to return the result to the accurate user.
    """
    __tablename__ = 'request_logs'

    # Primary Key
    req_id = db.Column(db.Integer, primary_key=True)
    
    # Log Details
    endpoint = db.Column(db.String(100), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    req_source = db.Column(db.String(100), nullable=False)
    task_id = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.String(100), nullable=False)
    # Metadata
    requested_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return f"<UsageLog {self.endpoint} @ {self.requested_at}>"
    
    def get_id(self):
        return str(self.log_id)