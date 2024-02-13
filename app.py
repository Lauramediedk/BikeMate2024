from flask import Flask, render_template
from config import SECRET_KEY
from users import users_bp
from dashboard import dashboard_bp
from challenges import challenges_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(challenges_bp, url_prefix='/challenges')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
