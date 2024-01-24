from flask import Flask
import json
from neo4j import GraphDatabase

app = Flask(__name__)

#neo4j
NEO4J_URI = 'neo4j+s://8bc886ed.databases.neo4j.io'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '4Ka5DqTW0WC9-ZbxMV0x9ZdCiagHCRxHDkYvZc6GSFw'

# Driver instantiation
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
    cypher_query = "MATCH (p:Person) RETURN p LIMIT 4"

    try:
        result = run_query(cypher_query)
        return json.dumps(result), 200  # Use json.dumps() to convert to JSON
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
