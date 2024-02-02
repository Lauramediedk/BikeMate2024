from neo4j.time import DateTime
from db import db
import uuid

class Post:
    """Post model"""
    def __init__(self, content, author, image_path=None, is_private=False, **kwargs):
        self.post_id = None
        self.content = content
        self.author = author
        self.image_path = image_path
        self.is_private = is_private

        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_post(self):
        self.post_id = str(uuid.uuid4())
        self.created = DateTime.now()

        query = (
            """
            CREATE (post:Post {post_id: $post_id, created: $created, content: $content, author: $author_id, image_path: $image_path, is_private: $is_private })
            """
            )
        parameters = {
            "post_id": self.post_id,
            "created": self.created,
            "content": self.content,
            "author_id": self.author,
            "image_path": self.image_path,
            "is_private": self.is_private,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error creating post: {str(e)}") from e

    @classmethod
    def get_posts(cls):
        try:
            query = "MATCH (n:Post) RETURN n"

            result = db.run_query(query)

            posts = [cls(**record['n']) for record in result]

            return posts

        except Exception as e:
            print(f"Could not get posts: {str(e)}")
            return None