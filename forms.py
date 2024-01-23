from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, SelectField, DateTimeField, DateField, TimeField, FileField, FloatField
from wtforms.validators import InputRequired, Email, EqualTo, Regexp, ValidationError
import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators = [InputRequired(), Regexp(r'^[A-Za-z ]+$', message='Name must only contain letters and spaces')])
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    company = StringField('Company', validators = [InputRequired()])
    job = StringField('Job', validators = [InputRequired()])
    country = StringField('Country', validators = [InputRequired()])
    phone = StringField('Phone', validators = [InputRequired()])
    submit = SubmitField('Create Account')

class EditUserForm(FlaskForm):
    name = StringField('Name', validators = [InputRequired(), Regexp(r'^[A-Za-z ]+$', message='Name must only contain letters and spaces')])
    company = StringField('Company', validators = [InputRequired()])
    job = StringField('Job', validators = [InputRequired()])
    country = StringField('Country', validators = [InputRequired()])
    phone = StringField('Phone', validators = [InputRequired()])
    email = StringField('Email', validators = [InputRequired(), Email()])
    submit = SubmitField('Save Changes')

class EditCameraForm(FlaskForm):
    camera_name = StringField('Camera Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    vendor = StringField('Vendor', validators=[InputRequired()])
    resolution = SelectField('Resolution', choices=[('360p', '360p'), ('480p', '480p'), ('720p', '720p'), ('1080p', '1080p'), ('1440p', '1440p'), ('2160p', '2160p')], default='1080p')
    fps = IntegerField('FPS', validators=[InputRequired()])
    camera_path = StringField('Camera Path', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Online', 'Online'), ('Offline', 'Offline')], default='Online')
    active_time = DateTimeField("Timestamp", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    stop_time = DateTimeField("Timestamp", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    malfunction = SelectField('Malfunction', choices=[('Blurred', 'Blurred'), ('Background Change', 'Background Change'), ('Stop working', 'Stop working'), ('Other', 'Other'), ('None', 'None')], default='None')    
    submit = SubmitField('Save Changes')

class EditVehicleForm(FlaskForm):
    plate_number = StringField('Plate Number', validators=[InputRequired()])
    type = StringField('Type', validators=[InputRequired()])
    color = StringField('Color', validators=[InputRequired()])
    time = DateTimeField("Timestamp", format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    Vehicle_image = StringField('Camera Path', validators=[InputRequired()])
    speed = FloatField('Speed', validators=[InputRequired()])
    orientation = SelectField('Orientation', choices=[('Up', 'Up'), ('Down', 'Down'), ('Right', 'Right'), ('Left', 'Left')], default='Up')    
    idle_time = FloatField('Idle Time', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Entering', 'Entering'), ('Exiting', 'Exiting'), ('Moving Inside', 'Moving Inside'), ('Parking', 'Parking'), ('Violating', 'Violating'), ('Other', 'Other')], default='Entering')    
    violation = SelectField('Violation', choices=[('Speed', 'Speed'), ('Direction', 'Direction'), ('Parking', 'Parking'), ('Other', 'Other'), ('None', 'None')], default='None')    
    location = SelectField('Location', choices=[], validators=[InputRequired()])
    submit = SubmitField('Save Changes')
    

class AddCamera(FlaskForm):
    camera_name = StringField('Camera Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    vendor = StringField('Vendor', validators=[InputRequired()])
    resolution = SelectField('Resolution', choices=[('360p', '360p'), ('480p', '480p'), ('720p', '720p'), ('1080p', '1080p'), ('1440p', '1440p'), ('2160p', '2160p')], default='1080p')
    fps = IntegerField('FPS', validators=[InputRequired()])
    camera_path = FileField('Camera Path', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Online', 'Online'), ('Offline', 'Offline')], default='Online')
    active_date = DateField('Active Date', format='%Y-%m-%d', validators=[InputRequired()])
    active_time = TimeField('Active Time', format='%H:%M', validators=[InputRequired()])
    stop_date = DateField('Stop Date', format='%Y-%m-%d')
    stop_time = TimeField('Stop Time', format='%H:%M')
    malfunction = SelectField('Malfunction', choices=[('Blurred', 'Blurred'), ('Background Change', 'Background Change'), ('Stop working', 'Stop working'), ('Other', 'Other'), ('None', 'None')], default='None')    
    submit = SubmitField('Add Camera')

class AddVehicle(FlaskForm):
    plate_number = StringField('Plate Number', validators=[InputRequired()])
    type = StringField('Type', validators=[InputRequired()])
    color = StringField('Color', validators=[InputRequired()])
    time = TimeField('Time', format='%H:%M')
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    Vehicle_image = FileField('Vehicle Image', validators=[InputRequired()])
    speed = FloatField('Speed', validators=[InputRequired()])
    orientation = SelectField('Orientation', choices=[('Up', 'Up'), ('Down', 'Down'), ('Right', 'Right'), ('Left', 'Left')], default='Up')    
    idle_time = FloatField('Idle Time', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Entering', 'Entering'), ('Exiting', 'Exiting'), ('Moving Inside', 'Moving Inside'), ('Parking', 'Parking'), ('Violating', 'Violating'), ('Other', 'Other')], default='Entering')    
    violation = SelectField('Violation', choices=[('Speed', 'Speed'), ('Direction', 'Direction'), ('Parking', 'Parking'), ('Other', 'Other'), ('None', 'None')], default='None')    
    location = SelectField('Location', choices=[], validators=[InputRequired()])
    submit = SubmitField('Add Vehicle')

class filtercameras(FlaskForm):
    camera_name = StringField('Camera Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Online', 'Online'), ('Offline', 'Offline')], default='Online')
    start_active_date = DateField('Start Active Date', format='%Y-%m-%d', validators=[InputRequired()])
    start_active_time = TimeField('Start Active Time', format='%H:%M', validators=[InputRequired()])
    malfunction = SelectField('Malfunction', choices=[('Blurred', 'Blurred'), ('Background Change', 'Background Change'), ('Stop working', 'Stop working'), ('Other', 'Other'), ('None', 'None')], default='None')    
    submit = SubmitField('Filter Cameras')

class filtervechiles(FlaskForm):
    plate_number = StringField('Plate Number', validators=[InputRequired()])
    type = StringField('Type', validators=[InputRequired()])
    color = StringField('Color', validators=[InputRequired()])
    time = TimeField('Time', format='%H:%M')
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    speed = FloatField('Max Speed', validators=[InputRequired()])
    orientation = SelectField('Orientation', choices=[('Up', 'Up'), ('Down', 'Down'), ('Right', 'Right'), ('Left', 'Left')], default='Up')    
    idle_time = FloatField('Idle Time', validators=[InputRequired()])
    status = SelectField('Status', choices=[('Entering', 'Entering'), ('Exiting', 'Exiting'), ('Moving Inside', 'Moving Inside'), ('Parking', 'Parking'), ('Violating', 'Violating'), ('Other', 'Other')], default='Entering')    
    violation = SelectField('Violation', choices=[('Speed', 'Speed'), ('Direction', 'Direction'), ('Parking', 'Parking'), ('Other', 'Other'), ('None', 'None')], default='None')    
    location = SelectField('Location', choices=[], validators=[InputRequired()])
    submit = SubmitField('Filter Vehicles')



class EditCarForm(FlaskForm):
    plate_number = StringField("Plate Number", validators = [InputRequired()])
    model = StringField("Model", validators = [InputRequired()])
    type = StringField("Type", validators = [InputRequired()])
    color = StringField("Color", validators = [InputRequired()])
    visits = IntegerField("Number of Visits", validators = [InputRequired()])
    submit = SubmitField("Edit Car")