from db import db


class User:
    def __init__(self, first_name, last_name, email, hashed_password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password

    def signup_user(self):
        query = (
            "CREATE (user:User {first_name: $first_name, last_name: $last_name, email: $email, hashed_password: $password})"
        )
        parameters = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.hashed_password,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error registrering user: {str(e)}")
