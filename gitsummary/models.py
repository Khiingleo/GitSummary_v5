from flask import current_app
from gitsummary import db, login_manager
from datetime import datetime, timezone, timedelta
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import jwt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """user class"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    saved_repositories = db.relationship('SavedRepository', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=600):
        s = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        print(f"token {s}")
        return s
    
    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms="HS256"
            )
        except Exception as e:
            print(f"error decoding the token{e}")
            return None
        user_id = data.get('user_id')
        print(f"decoded token {user_id}")
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class SavedRepository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repository_name = db.Column(db.String(100), nullable=False)
    repository_url = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"SavedRepository('{self.repository_name}', '{self.repository_url}')"