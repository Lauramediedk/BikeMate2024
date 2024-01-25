from flask import Flask, jsonify
from config import SECRET_KEY
from db import db

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def check_database():
    query = "MATCH (p:person) RETURN p LIMIT 4"

    try:
        result = db.run_query(query)
        return jsonify(result), 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
