from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "Ce2U9zj5NVu9Cl4H"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://aigituwazdqqyl:aab922da356a629e3a5136068d92647c631d8208dad1beda0bdbde9640651ef9@ec2-54-225-118-55.compute-1.amazonaws.com:5432/d20mmqmdnnd8j5"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"
db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
