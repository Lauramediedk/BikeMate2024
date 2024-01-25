from flask import Flask
from config import SECRET_KEY
from db import db

app = Flask(__name__)
app.secret_key = SECRET_KEY

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
