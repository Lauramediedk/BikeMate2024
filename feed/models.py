from neo4j.time import DateTime
from db import db
import uuid

class Post:
    """Post model"""
    def __init__(self, content, author_id=None, author_name=None, image_path=None, is_private=False, **kwargs):
        self.post_id = None
        self.content = content
        self.author_id = author_id
        self.author_name = author_name
        self.image_path = image_path
        self.is_private = is_private

        for key, value in kwargs.items():
            setattr(self, key, value)


    def create_post(self):
        self.post_id = str(uuid.uuid4())
        self.created = DateTime.now()

        query = (
            """
            MATCH (user:User {user_id: $author_id})
            CREATE (post:Post {post_id: $post_id, created: $created, content: $content, author_id: $author_id, author_name: $author_name, image_path: $image_path, is_private: $is_private })
            CREATE (post)-[:CREATED_BY]->(user)
            """
            )
        parameters = {
            "post_id": self.post_id,
            "created": self.created,
            "content": self.content,
            "author_id": self.author_id,
            "author_name": self.author_name,
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
            query = "MATCH (n:Post) WHERE n.is_private = false RETURN n"

            result = db.run_query(query)

            posts = [record['n'] for record in result]

            return posts

        except Exception as e:
            print(f"Could not get posts: {str(e)}")
            return None


    @staticmethod
    def edit_post(post_id, author_id, new_content):
        query = (
            """
            MATCH (post:Post {post_id: $post_id})-[:CREATED_BY]->(user:User {user_id: $author_id})
            SET post.content = $new_content
            """
        )
        parameters = {
            "post_id": post_id,
            "author_id": author_id,
            "new_content": new_content
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error editing post: {str(e)}") from e

    @staticmethod
    def delete_post(post_id, author_id):
        query = (
            """
            MATCH (post:Post {post_id: $post_id})-[:CREATED_BY]->(user:User {user_id: $author_id})
            DETACH DELETE post
            """
        )
        parameters = {
            "post_id": post_id,
            "author_id": author_id,
        }

        try:
            db.run_query(query, parameters)
        except Exception as e:
            raise RuntimeError(f"Error deleting post: {str(e)}") from e


    @staticmethod
    def search_post(search_content):
        query = (
            """
            MATCH (post:Post)
            WHERE post.content CONTAINS $search_content
            RETURN post
            """
        )

        parameters = {
            "search_content": search_content,
        }

        try:
            result = db.run_query(query, parameters)
            posts = [record['post'] for record in result]
            return posts
        except Exception as e:
            raise RuntimeError(f"Kunne ikke finde nogle opslag: {str(e)}") from e