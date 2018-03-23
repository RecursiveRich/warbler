from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
import os

app = Flask(__name__)

if os.environ.get('ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/warbler-db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "it's a secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.users.models import User
from project.messages.models import Message

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(
    messages_blueprint, url_prefix='/users/<int:id>/messages')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def root():
    # messages = Message.query.order_by("timestamp asc").limit(100).all()
    following_ids = [u.id for u in current_user.following.all()]
    condition1 = Message.user_id.in_(following_ids)
    # condition2 = Message.user_id == current_user.id  #or_ gives an error with from flask_sqlalchemy import or_
    messages = Message.query.filter(condition1).order_by(
        "timestamp asc").limit(100).all()
    # messages = current_user.messages.all()
    # for u in current_user.following.all():
    #     messages += u.messages.all()
    # if len(messages) > 100:
    #     messages = messages[0:100]
    return render_template('home.html', messages=messages)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
