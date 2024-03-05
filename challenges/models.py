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
        self.participants = participants

        for key, value in kwargs.items():
            setattr(self, key, value)


    def create_event(self, user_id):
        self.event_id = str(uuid.uuid4())

        query = (
            """
            CREATE (event:Event {event_id: $event_id, title: $title, description: $description, date: $date, location: $location, admin: $admin, participants: $participants})
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
            "participants": self.participants,
            "user_id": user_id,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error creating event: {str(e)}") from e


    @classmethod
    def get_own_events(cls, user_id):
        query = (
            """
            MATCH (u:User {user_id: $user_id})-[:CREATED]->(e:Event)
            RETURN e
            """
        )

        parameters = {
            "user_id": user_id,
        }

        try:
            result = db.run_query(query, parameters)

            events = [cls(**record['e']) for record in result]

            return events
        except Exception as e:
            raise RuntimeError(f"Error finding events: {str(e)}") from e


    @classmethod
    def get_all_events(cls, user_id):
        query = (
            """
            MATCH (e:Event)
            WHERE NOT (:User {user_id: $user_id})-[:CREATED]->(e)
            RETURN e
            """
        )

        parameters = {
            "user_id": user_id,
        }

        try:
            result = db.run_query(query, parameters)

            events = [cls(**record['e']) for record in result]

            return events
        except Exception as e:
            raise RuntimeError(f"Error finding events: {str(e)}") from e


    @classmethod
    def get_event_by_id(cls, event_id):
        query = (
            """
            MATCH (e:Event {event_id: $event_id})
            RETURN e
            """
        )
        parameters = {"event_id": event_id}

        try:
            result = db.run_query(query, parameters)
            data_list = result

            if data_list:
                data = data_list[0].get("e")

                return cls(
                    event_id=data.get("event_id"),
                    title=data.get("title"),
                    description=data.get("description"),
                    date=data.get("date"),
                    location=data.get("location"),
                    admin=data.get("admin"),
                    participants=data.get("participants"),

                )
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Error getting event by ID: {str(e)}") from e


    @classmethod
    def is_user_joined(cls, user_id, event_id):
        query = (
            """
            MATCH (u:User {user_id: $user_id})-[:JOINED]->(event:Event {event_id: $event_id})
            RETURN COUNT(*) > 0 AS is_joined
            """
        )
        parameters = {"user_id": user_id, "event_id": event_id}
        result = db.run_query(query, parameters)
        if result:
            return result[0]['is_joined']
        else:
            return False


    @classmethod
    def join_event(cls, user_id, event_id):
        query = (
            """
            MATCH (u:User {user_id: $user_id})
            MATCH (e:Event {event_id: $event_id})
            MERGE (u)-[:JOINED]->(e)
            ON CREATE SET e.participants = COALESCE(e.participants, 0) + 1
            """
        )
        parameters = {
            "user_id": user_id,
            "event_id": event_id,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error joining event: {str(e)}") from e


    @classmethod
    def unjoin_event(cls, user_id, event_id):
        query = (
            """
            MATCH (u:User {user_id: $user_id})-[r:JOINED]->(e:Event {event_id: $event_id})
            DELETE r
            WITH e
            SET e.participants = CASE WHEN e.participants > 0 THEN e.participants - 1 ELSE 0 END
            """
        )
        parameters = {
            "user_id": user_id,
            "event_id": event_id,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error unjoining event: {str(e)}") from e
