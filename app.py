from flask import Flask
import json
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Neo4j Driver instantiation
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()

@app.route("/")
def check_database():
    # Your Cypher query
    cypher_query = "MATCH (p:Person) RETURN p LIMIT 1"

    try:
        result = run_query(cypher_query)
        return json.dumps(result), 200  # Use json.dumps() to convert to JSON
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
