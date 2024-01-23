from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, abort,Response,stream_with_context
from forms import LoginForm, EditCameraForm,EditCarForm, RegisterForm, EditUserForm, AddCamera, AddVehicle, EditVehicleForm,filtercameras,filtervechiles
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from camera import streaming,thumbnail,Parking,parkingthumbnail
from flask_migrate import Migrate
from flask import session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys
from sqlalchemy import create_engine, Column, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:787898@localhost/gradproject'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'max_overflow': 5
}
db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app)
migrate = Migrate(app, db)

