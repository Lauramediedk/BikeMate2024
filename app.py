from flask import Flask
from config import SECRET_KEY
from users import users_bp
from dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
