import uuid
from db import db


class Events:
    """Events model"""
    def __init__(self, title, description, date, location, admin, participants=None, **kwargs):
        self.event_id = None
        self.title = title
        self.description = description
        self.date = date
        self.location = location
        self.admin = admin
        self.participants = participants or []

        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_event(self, user_id):
        self.event_id = str(uuid.uuid4())

        query = (
            """
            CREATE (event:Event {title: $title, description: $description, date: $date, location: $location, admin: $admin})
            WITH event
            MATCH (u:User {user_id: $user_id})
            MERGE (u)-[:CREATED]->(event)
            """
        )
        parameters = {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "location": self.location,
            "admin": user_id,
            "user_id": user_id,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error creating event: {str(e)}") from e
