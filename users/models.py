from werkzeug.security import check_password_hash
import uuid
from db import db


class User:
    """User model"""
    def __init__(self, first_name, last_name, email, hashed_password, image_path=None, bio=None, **kwargs):
        self.user_id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password
        self.image_path = image_path
        self.bio = bio

        for key, value in kwargs.items():
            setattr(self, key, value)

    def signup_user(self):
        self.user_id = str(uuid.uuid4())

        query = (
            "CREATE (user:User {user_id: $user_id, first_name: $first_name, last_name: $last_name, email: $email, hashed_password: $password})"
        )
        parameters = {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.hashed_password,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error registrering user: {str(e)}") from e

    @classmethod
    def find_user_email(cls, email):
        query = "MATCH (user:User {email: $email}) RETURN user"
        parameters = {"email": email}

        result = db.run_query(query, parameters)

        if result:
            return cls(**result[0]['user'])
        else:
            print("No user found with the email", email)
            return None

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
