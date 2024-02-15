from flask import Flask, render_template
from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from users import users_bp
from dashboard import dashboard_bp
from challenges import challenges_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(challenges_bp, url_prefix='/challenges')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
