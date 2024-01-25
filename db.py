from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class Database:
    def __init__(self, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD):
        self._driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self._driver.close()

    def run_query(self, query):
        with self._driver.session() as session:
            result = session.run(query)
            return result.data()


# Instance of the database connection
db = Database(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
