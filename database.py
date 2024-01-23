from config import *

"""Model for Users."""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    company = db.Column(db.String)
    job = db.Column(db.String)
    country = db.Column(db.String)
    phone = db.Column(db.String)


"""Model for Vehicles."""
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(50))
    color = db.Column(db.String(50))    
    vehicle_states = db.relationship('VehicleState', backref='vehicle', lazy=True)
    ##edits
    location=db.Column(db.String(100))
    alerts = db.relationship('Alerts', backref='vehicle', lazy=True)
    parking_status = db.relationship('Parkingstatus', backref='vehicle', lazy=True)
    


"""Model for VehicleStates."""
class VehicleState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(50), db.ForeignKey('vehicle.plate_number'))
    timestamp = db.Column(db.TIMESTAMP)
    Vehicle_image = db.Column(db.String(100))  
    speed = db.Column(db.Float)
    orientation = db.Column(db.Enum('Up', 'Down', 'Right' ,'Left', name='orientation'), default='Up')
    idle_time = db.Column(db.Float)
    status = db.Column(db.Enum('Entering', 'Exiting', 'Moving Inside' ,'Parking', 'Violating', 'Other', name='vehicle_status'), default='Entering')
    violation = db.Column(db.Enum('Speed', 'Direction', 'Parking' ,'Other', 'None', name='violation'), default='None')
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.camera_id'))
    camera_info = db.relationship('Camera', backref='VehicleState', lazy=True)
    



"""Model for Cameras."""
class Camera(db.Model):
    camera_id = db.Column(db.Integer, primary_key=True)
    camera_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    vendor = db.Column(db.String(100))
    resolution = db.Column(db.Enum('360p', '480p', '720p' ,'1080p', '1440p', '2160p', name='resolution'), default='1080p')
    fps = db.Column(db.Integer)
    camera_states = db.relationship('CameraState', backref='camera', lazy=True)
    #edits
    alerts = db.relationship('Alerts', backref='camera', lazy=True)

"""Model for CameraStates."""
class CameraState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.camera_id'))
    camera_path = db.Column(db.String(100))  
    active_time = db.Column(db.TIMESTAMP)
    stop_time = db.Column(db.TIMESTAMP)
    status = db.Column(db.Enum('Online', 'Offline', name='camera_status'), default='Online')
    malfunction = db.Column(db.Enum('Blurred', 'Background Change', 'Stop working' ,'Other', 'None', name='malfunction'), default='None')



class Alerts(db.Model):
    violation_id=db.Column(db.Integer, primary_key=True)
    car_id=db.Column(db.String(50), db.ForeignKey('vehicle.plate_number'))
    camera_id=db.Column(db.Integer, db.ForeignKey('camera.camera_id'))
    type=db.Column(db.String(100))
    alert_time = db.Column(db.TIMESTAMP)
    opened=db.Column(db.Boolean)

##edits can be changed
"""Model for Praking"""
class Parkingareas(db.Model):
    area_id = db.Column(db.Integer, primary_key=True)
    free=db.Column(db.Integer)
    occupied=db.Column(db.Integer)
    location=db.Column(db.String(100))
    parking_spots = db.relationship('Parkingspots', backref='parkingareas', lazy=True)

class Parkingspots(db.Model):
    spot_id=db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    area_id=db.Column(db.Integer, db.ForeignKey('parkingareas.area_id'))
    parking_status = db.relationship('Parkingstatus', backref='parkingspots', lazy=True)

class Parkingstatus(db.Model):
    status_id=db.Column(db.Integer, primary_key=True)
    spot_id=db.Column(db.Integer, db.ForeignKey('parkingspots.spot_id'))
    car_id=db.Column(db.String(50), db.ForeignKey('vehicle.plate_number'))
    status=db.Column(db.String(100))
    status_time = db.Column(db.TIMESTAMP)



with app.app_context():
    # Create "team" user and add it to session
    team = User(full_name = "Ibrahim Hamada", email = "admin@zewailcity.edu.eg", password = "123", company ="ZC", job="Admin", country="Egypt", phone="01155319781")
    db.session.add(team)
    db.create_all()
    # Commit changes in the session
    try:
        db.session.commit()
    except Exception as e: 
        db.session.rollback()
    finally:
        db.session.close()
        
def pushdata(Pnum,Mod,Ty,Co,Vi=1):
    Vehicle=Vehicle(plate_number=Pnum,model=Mod,type=Ty,color=Co,visits=Vi)
    db.session.add(Vehicle) 
    try:
        db.session.commit()
    except Exception as e: 
        db.session.rollback()
    finally:
        db.session.close()