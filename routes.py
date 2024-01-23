from database import *
from flask import render_template, url_for, redirect,flash, get_flashed_messages, request
from datetime import datetime
from asyncio import sleep
import threading
import time
import os
from sqlalchemy import and_, column, select
from sqlalchemy.orm import aliased
from collections import Counter



##camera stream import
from camera import streaming, thumbnail


def background_task():
    with app.app_context():
        while True:
            latest_record = Alerts.query.order_by(Alerts.alert_time.desc()).first()
            if latest_record and latest_record.opened==False:
                latest_record.opened=True
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                db.session.close()
                socketio.emit("update alerts", True)
                print("Alert!!!")
            time.sleep(10)

@app.route("/alertsupdate",methods=["POST"])
async def alertsupdate():
    t = threading.Thread(target=background_task)  # create new thread
    t.setDaemon(True)
    t.start()  # start thread
    return Response(status=204)

@app.route("/alerts")
def alertstable():
    """Table contain all the Alerts in the data base"""
    if session.get('user') is not None:
        user = User.query.get(session['user'])
        if user.job!='Admin':
            return render_template("credential_error.html",user=user)
        alerts = Alerts.query.all()
        return render_template("alerts.html",user=user,alerts=alerts)
    else:
        return redirect(url_for('pages_login'))



@app.route("/pages_login", methods=["POST", "GET"])
def pages_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            flash("Wrong Credentials. Please Try Again.", "danger")
            return redirect(url_for('pages_login'))
        else:
            session['user'] = user.id
            return redirect(url_for('index'))
        
    return render_template("pages-login.html", form = form)



@app.route("/pages_register", methods=["POST", "GET"])
def pages_register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() is None:
            entry = User(full_name=form.name.data, email=form.email.data, password=form.password.data, company=form.company.data, job=form.job.data, country=form.country.data, phone=form.phone.data)
            db.session.add(entry)
            db.session.commit()
            #db.session.close()
            flash("Account was Successfully Registered", "success")
            return redirect(url_for('pages_login'))
            
        else:
            flash("Email already exists", "danger")
        
    return render_template('pages-register.html', form=form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('pages_login', _scheme='http', _external=True))
    

@app.route("/users_profile")
def users_profile():
    if session.get('user') is not None:
        user = User.query.get(session['user'])
        return render_template('users-profile.html', user=user)
    else:
        return redirect(url_for('pages_login'))



@app.route("/users_edit/<int:id>", methods=["POST", "GET"])
def users_edit(id):
    if session.get('user') is not None:
        user = User.query.get_or_404(id)
        form = EditUserForm()
        if user is None: 
            abort(404, description="No User was Found with the given ID")
        
        if form.validate_on_submit():
            if User.query.filter(User.id != user.id, User.email == form.email.data).first() is not None:
                flash("Email already exists", "danger")
                return redirect(url_for('users_edit', id = user.id, _scheme='http', _external=True))

            user.full_name = form.name.data
            user.email = form.email.data
            user.company = form.company.data
            user.job = form.job.data
            user.country = form.country.data
            user.phone = form.phone.data
            try:
                db.session.commit()
                #db.session.close()
                flash("Account was successfully updated", "success")
            except:
                flash("No Users was Found with the given ID", "danger")
                db.session.rollback()
            return redirect(url_for('users_profile', _scheme='http', _external=True))

        return render_template("users-edit.html", form=form, user=user)

    else:
        return redirect(url_for('pages_login'))
    

@app.route("/pages_faq")
def pages_faq():
    if session.get('user') is not None:
        user = User.query.get(session['user'])
        return render_template("pages-faq.html", user=user)
    else:
        return redirect(url_for('pages_login'))
     

@app.route("/add_camera", methods=["POST", "GET"])
def add_camera():
    if session.get('user') is not None:
        user = User.query.get(session['user'])
        if user.job!='Admin':
            return render_template("credential_error.html",user=user)
        form = AddCamera()
        if form.validate_on_submit():
            atime_dt = datetime.combine(form.active_date.data, form.active_time.data)
            stime_dt = datetime.combine(form.stop_date.data, form.stop_time.data)
            entry_camera = Camera(camera_name=form.camera_name.data, location=form.location.data, vendor=form.vendor.data, resolution=form.resolution.data, fps=form.fps.data)
            app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
            camera_path = form.camera_path.data
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], camera_path)
    
            db.session.add(entry_camera)    
            try:
                db.session.commit()
                
            except:
                flash("Camera was not Added", "danger")
            
            camID = entry_camera.camera_id
            entry_cameraState = CameraState(camera_id = camID, camera_path=full_path, active_time=atime_dt, stop_time=stime_dt, status=form.status.data, malfunction=form.malfunction.data)
            db.session.add(entry_cameraState)
            try:
                db.session.commit()
                #db.session.close()
                flash("Camera was Successfully Added", "success")
            except:
                flash("Camera was not Added", "danger")
            return redirect(url_for('add_camera', _scheme='http', _external=True))
        
        return render_template('add-camera.html', form=form, user=user)
    else:
        return redirect(url_for('pages_login'))
    

@app.route("/add_vehicle", methods=["POST", "GET"])
def add_vehicle():
    if session.get('user') is not None:
        user = User.query.get(session['user'])
        if user.job!='Admin':
            return render_template("credential_error.html",user=user)
        form = AddVehicle()

        camera_locations = [(c.location, c.location) for c in Camera.query.distinct(Camera.location)]
        form.location.choices = camera_locations

        camera = Camera.query.all()[1]
       
        if form.validate_on_submit():
            entry_vehicle = Vehicle(plate_number=form.plate_number.data, type=form.type.data, color=form.color.data, location=form.location.data)
            db.session.add(entry_vehicle)    
            try:
                db.session.commit()
            except:
                flash("Vehicle was not Added", "danger")
            
            atime_dt = datetime.combine(form.date.data, form.time.data)

            app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'vehicles')
            vehicle_path = form.Vehicle_image.data
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], vehicle_path)
    
            plate_num = entry_vehicle.plate_number
            #camera_id = form.location.data

            entry_vehicelState = VehicleState(plate_number = plate_num, timestamp=atime_dt, Vehicle_image=full_path, speed=form.speed.data, orientation=form.orientation.data, 
                                              idle_time = form.idle_time.data, status = form.status.data, violation = form.violation.data, camera_id=camera.camera_id)  
            db.session.add(entry_vehicelState)
            try:
                db.session.commit()
                #db.session.close()
                flash("Vehicle was Successfully Added", "success")
            except:
                flash(form.errors)
                flash("Vehicle was not Added", "danger")
            return redirect(url_for('add_vehicle', _scheme='http', _external=True))

        return render_template('add-vehicle.html', form=form, user=user)
    else:
        return redirect(url_for('pages_login'))

@app.route("/table_cameras", methods=["POST", "GET"])
def table_cameras():
    if 'user' in session:
        form = filtercameras()
        user = User.query.get(session['user'])
        if user.job!='Admin':
            return render_template("credential_error.html",user=user)
        if any(bool(field.data) for field in form) and request.method == 'POST':
            camera = aliased(Camera, name='c')
            # Build the filter conditions dynamically based on the form data
            filters = []
            if form.camera_name.data:
                filters.append(Camera.camera_name.ilike(f'%{form.camera_name.data}%'))
            if form.location.data:
                filters.append(Camera.location.ilike(f'%{form.location.data}%'))
            if form.status.data:
                filters.append(CameraState.status == form.status.data)
            if form.start_active_date.data and form.start_active_time.data:
                start_active_datetime = datetime.combine(form.start_active_date.data, form.start_active_time.data)
                filters.append(CameraState.active_time <= start_active_datetime)
            if form.malfunction.data:
                filters.append(CameraState.malfunction == form.malfunction.data)
            # Apply the filters to the query
            query = db.session.query(
            Camera.camera_id.label('id'),
            Camera.camera_name.label('camera_name'),
            Camera.location.label('location'),
            Camera.vendor.label('vendor'),
            Camera.resolution.label('resolution'),
            Camera.fps.label('fps'),
            CameraState.id.label('camera_state_id'),
            CameraState.camera_id.label('camera_id'),
            CameraState.camera_path.label('camera_path'),
            CameraState.active_time.label('active_time'),
            CameraState.stop_time.label('stop_time'),
            CameraState.status.label('status'),
            CameraState.malfunction.label('malfunction')
        ).join(
            CameraState, Camera.camera_id == CameraState.camera_id
        ).filter(
            and_(*filters)
        )

        # Execute the query and retrieve the results
            cameras = db.session.execute(query).fetchall()
            camera_info = []
            for camera in cameras:
                active_time = camera.active_time.strftime('%Y-%m-%d %H:%M:%S') if camera.active_time else ''
                stop_time = camera.stop_time.strftime('%Y-%m-%d %H:%M:%S') if camera.stop_time else ''
                camera_info.append({
                    'camera_id': camera.camera_id,
                    'camera_name': camera.camera_name,
                    'location': camera.location,
                    'vendor': camera.vendor,
                    'resolution': camera.resolution,
                    'fps': camera.fps,
                    'status': camera.status,
                    'malfunction': camera.malfunction,
                    'active_time': active_time,
                    'stop_time': stop_time,
                })
            # Process and display the filtered cameras as needed
            return render_template('cameras-table.html',form=form ,user=user, camera_info=camera_info)
        else:
            cameras = Camera.query.all()
            camera_states = CameraState.query.all()
            # Create a dictionary to map camera IDs to camera states
            camera_state_map = {}
            for state in camera_states:
                camera_state_map[state.camera_id] = state
            # Create a list of dictionaries with camera information
            camera_info = []
            for camera in cameras:
                state = camera_state_map.get(camera.camera_id)
                if state is None:
                    state = CameraState(status='Offline', malfunction='None')
                active_time = state.active_time.strftime('%Y-%m-%d %H:%M:%S') if state.active_time else ''
                stop_time = state.stop_time.strftime('%Y-%m-%d %H:%M:%S') if state.stop_time else ''
                camera_info.append({
                    'camera_id': camera.camera_id,
                    'camera_name': camera.camera_name,
                    'location': camera.location,
                    'vendor': camera.vendor,
                    'resolution': camera.resolution,
                    'fps': camera.fps,
                    'status': state.status,
                    'malfunction': state.malfunction,
                    'active_time': active_time,
                    'stop_time': stop_time,
                })
            
            return render_template("cameras-table.html",form=form ,user=user, camera_info=camera_info)
    else:
        return redirect(url_for('pages_login'))

@app.route("/delete_camera/<int:camera_id>", methods=["POST"])
def delete_camera(camera_id):
    camera = Camera.query.get(camera_id)
    camerastate = CameraState.query.filter(CameraState.camera_id == camera.camera_id).first()  
    if camera is None: 
        abort(404, description="No Camera was Found with the given ID")
    db.session.delete(camerastate)
    db.session.delete(camera)
    try:
        db.session.commit()
        #db.session.close()
        flash("Camera deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('table_cameras', _scheme='http', _external=True))

@app.route("/edit_camera/<int:camera_id>", methods=["POST", "GET"])
def edit_camera(camera_id):
    if 'user' in session:
        user = User.query.get(session['user'])
        if user.job!='Admin':
            return render_template("credential_error.html",user=user)
        camera = Camera.query.get_or_404(camera_id)
        if camera is None: 
            abort(404, description="No Camera was Found with the given ID")
        camerastate = CameraState.query.filter(CameraState.camera_id == camera.camera_id).first()        
        form = EditCameraForm()
        if form.validate_on_submit():
            camera.camera_name = form.camera_name.data
            camera.location = form.location.data
            camera.vendor = form.vendor.data
            camera.resolution = form.resolution.data
            camera.fps = form.fps.data
            if camerastate is None:
                camerastate = CameraState(camera_id = camera.camera_id, camera_path=form.camera_path.data, active_time=form.active_time.data, stop_time=form.stop_time.data, status=form.status.data, malfunction=form.malfunction.data)
                db.session.add(camerastate)    
                try:
                    db.session.commit()
                    #db.session.close()
                    flash("Camera was successfully updated", "success")
                except:
                    flash("No Camera was Found with the given ID", "danger")
                return redirect(url_for('table_cameras', _scheme='http', _external=True))
            else: 
                camerastate.camera_path = form.camera_path.data
                camerastate.status = form.status.data
                camerastate.active_time = form.active_time.data
                camerastate.stop_time = form.stop_time.data
                camerastate.malfunction = form.malfunction.data
                try:
                    db.session.commit()
                    #db.session.close()
                    flash("Camera was successfully updated", "success")
                except:
                    flash("No Camera was Found with the given ID", "danger")
                    db.session.rollback()
                return redirect(url_for('table_cameras', _scheme='http', _external=True))
        return render_template("camera-edit.html", user=user, form=form, camera=camera, camerastate=camerastate)
    else:
        return redirect(url_for('pages_login'))

###
@app.route("/table_vehicles", methods=["POST", "GET"])
def table_vehicles():
    if 'user' in session:
        form = filtervechiles(date=datetime.now().date(),time=datetime.now().time())
        user = User.query.get(session['user'])
        if user.job!='Admin':
            return render_template("credential_error.html",user=user)
        camera_locations = [(c.location) for c in Camera.query.distinct(Camera.location)]
        if any(bool(field.data) for field in form) and request.method == 'POST':
            vehicle = aliased(Vehicle, name='v')
            # Build the filter conditions dynamically based on the form data
            filters = []
            if form.plate_number.data:
                filters.append(Vehicle.plate_number.ilike(f'%{form.plate_number.data}%'))
            if form.type.data:
                filters.append(Vehicle.type.ilike(f'%{form.type.data}%'))
            if form.color.data:
                filters.append(Vehicle.color.ilike(f'%{form.color.data}%'))
            if form.date.data and form.time.data:
                timestamp = datetime.combine(form.date.data, form.time.data)
                filters.append(VehicleState.timestamp <= timestamp)
            if form.speed.data:
                filters.append(VehicleState.speed <= form.speed.data)
            if form.orientation.data:
                filters.append(VehicleState.orientation == form.orientation.data)
            if form.idle_time.data:
                filters.append(VehicleState.idle_time >= form.idle_time.data)
            if form.status.data:
                filters.append(VehicleState.status == form.status.data)
            if form.violation.data:
                filters.append(VehicleState.violation == form.violation.data)
            if form.location.data:
                filters.append(Vehicle.location == form.location.data)

            # Apply the filters to the query
            query = db.session.query(
            Vehicle.plate_number.label('plate_number'),
            Vehicle.type.label('type'),
            Vehicle.color.label('color'),
            Vehicle.location.label('location'),
            VehicleState.id.label('vehicle_state_id'),
            VehicleState.plate_number.label('vehicle_plate_number'),
            VehicleState.timestamp.label('timestamp'),
            VehicleState.Vehicle_image.label('Vehicle_image'),
            VehicleState.speed.label('speed'),
            VehicleState.orientation.label('orientation'),
            VehicleState.idle_time.label('idle_time'),
            VehicleState.status.label('status'),
            VehicleState.violation.label('violation')
        ).join(
            VehicleState, Vehicle.plate_number == VehicleState.plate_number
        ).filter(
            and_(*filters),
        )

        # Execute the query and retrieve the results
            vechiles =db.session.execute(query).fetchall()
            print(query)
            print(vechiles)
            vehicle_info = []
            for vechile in vechiles:
                vehicle_info.append({
                    'plate_number': vechile.plate_number,
                    'type': vechile.type,
                    'color': vechile.color,
                    'timestamp': vechile.timestamp,
                    'speed': vechile.speed,
                    'orientation': vechile.orientation,
                    'idle_time': vechile.idle_time,
                    'status': vechile.status,
                    'violation': vechile.violation
                })
            # Process and display the filtered cameras as needed
            return render_template("vehicles-table.html", user=user,form=form ,vehicle_info=vehicle_info,camera_locations=camera_locations)
        else:
            
            vehicles = Vehicle.query.all()
            vehicle_states = VehicleState.query.all()
            # Create a dictionary to map camera IDs to camera states
            vehicel_state_map = {}
            for state in vehicle_states:
                vehicel_state_map[state.plate_number] = state
            # Create a list of dictionaries with camera information
            vehicle_info = []
            for vehicle in vehicles:
                state = vehicel_state_map.get(vehicle.plate_number)
                if state is None:
                    state = VehicleState(speed=0, orientation='Up', idle_time=0, status='Entering', violation='None')
                timestamp = state.timestamp.strftime('%Y-%m-%d %H:%M:%S') if state.timestamp else ''
                vehicle_info.append({
                    'plate_number': vehicle.plate_number,
                    'type': vehicle.type,
                    'color': vehicle.color,
                    'timestamp': timestamp,

                    'speed': state.speed,
                    'orientation': state.orientation,
                    'idle_time': state.idle_time,
                    'status': state.status,
                    'violation': state.violation,
                })
            
            return render_template("vehicles-table.html", user=user,form=form ,vehicle_info=vehicle_info,camera_locations=camera_locations)
    else:
        return redirect(url_for('pages_login'))
    
@app.route("/delete_vehicle/<string:vehicle_id>", methods=["POST"])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(plate_number = vehicle_id).first()
    vehiclestate = VehicleState.query.filter(VehicleState.plate_number == vehicle.plate_number).first()  
    if vehicle is None: 
        abort(404, description="No Vehicle was Found with the given ID")
    db.session.delete(vehiclestate)
    db.session.delete(vehicle)
    try:
        db.session.commit()
        #db.session.close()
        flash("Vehicle deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('table_vehicles', _scheme='http', _external=True))

###
@app.route("/edit_vehicle/<string:vehicle_id>", methods=["POST", "GET"])
def edit_vehicle(vehicle_id):
    if 'user' in session:
        user = User.query.get(session['user'])
        if user.job!='Admin':
            return render_template("credential_error.html",user=user)
        vehicle = Vehicle.query.filter_by(plate_number = vehicle_id).first()
        if vehicle is None: 
            abort(404, description="No Vehicle was Found with the given ID")
        vehiclestate = VehicleState.query.filter(VehicleState.plate_number == vehicle.plate_number).first()        
        form = EditVehicleForm()
        camera_locations = [(c.location, c.location) for c in Camera.query.distinct(Camera.location)]
        form.location.choices = camera_locations
        if form.validate_on_submit():
            vehicle.plate_number = form.plate_number.data
            vehicle.type = form.type.data
            vehicle.color = form.color.data 
            if vehiclestate is None:
                vehiclestate = VehicleState(plate_number = vehicle.plate_number, timestamp=form.time.data, Vehicle_image=form.Vehicle_image.data, speed=form.speed.data, 
                                            orientation=form.orientation.data, idle_time=form.idle_time.data, status=form.status.data, violation=form.violation.data )
                db.session.add(vehiclestate)    
                try:
                    db.session.commit()
                    #db.session.close()
                    flash("Vehicle was successfully updated", "success")
                except:
                    flash("No Vehicle was Found with the given ID", "danger")
                return redirect(url_for('table_vehicles', _scheme='http', _external=True))
            else: 
                vehiclestate.plate_number = form.plate_number.data
                vehiclestate.timestamp = form.time.data
                vehiclestate.Vehicle_image = form.Vehicle_image.data
                vehiclestate.speed = form.speed.data
                vehiclestate.orientation = form.orientation.data

                vehiclestate.idle_time = form.idle_time.data
                vehiclestate.status = form.status.data
                vehiclestate.violation = form.violation.data
               
                try:
                    db.session.commit()
                    #db.session.close()
                    flash("Vehicle was successfully updated", "success")
                except:
                    flash("No Vehicle was Found with the given ID", "danger")
                    db.session.rollback()
                return redirect(url_for('table_vehicles', _scheme='http', _external=True))
        return render_template("vehicle-edit.html", user=user, form=form, vehicle=vehicle, vehiclestate=vehiclestate)
    else:
        return redirect(url_for('pages_login'))

##Cameras stream needed routes

######
@app.route("/camerapage")
def camerapage():
    if 'user' in session:
        user = User.query.get(session['user'])
        cameras = Camera.query.order_by(Camera.camera_id.asc()).all()
        camera_states = CameraState.query.all()
        # Create a dictionary to map camera IDs to camera states
        camera_state_map = {}
        cameras_info=[]
        for state in camera_states:
            camera_state_map[state.camera_id] = state
        for camera in cameras:
            state = camera_state_map.get(camera.camera_id)
            if state is not None:
                cameras_info.append({
                'camera_id': camera.camera_id,
                'camera_name': camera.camera_name,
                'location': camera.location,
                'camera_path': state.camera_path})
        return render_template("stream.html",user=user,cameras_info=cameras_info)
    else:
        return redirect(url_for('pages_login'))


@app.route("/camera_feed/<int:camera_id>")
def video(camera_id):
    """Camera streaming route."""
    return Response(stream_with_context(streaming(camera_id)),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/thumbnail_feed/<int:camera_id>")
def video_thumbnail(camera_id):
    """Camera Thumbnail route."""
    return Response(stream_with_context(thumbnail(camera_id)),mimetype='multipart/x-mixed-replace; boundary=frame')
######



@app.route("/")
def index():
    if session.get('user') is not None:
        user = User.query.get(session['user'])
        # Query the database to retrieve camera and camera state information
        cameras = Camera.query.all()
        camera_states = CameraState.query.all()
        parkings = Parkingareas.query.all()

        parking_states = {}
        for parking in parkings:
            parking_states['free'] = parking.free
            parking_states['occupied'] = parking.occupied
            parking_states['location'] = parking.location
        
        camera_state_map = {}
        camera_malfunction_map = {}
        for camera in cameras:
            camera_malfunction_map[camera.location] = {'Blurred': 0, 'Background Change': 0, 'None': 0}
            
        camera_malfunction = {}
        for state in camera_states:
            camera_state_map[state.camera.camera_name] = state.status
            if state.malfunction != 'None':
                camera_malfunction[state.camera_id] = state.malfunction
            if state.malfunction:
                camera_malfunction_map[state.camera.location][state.malfunction] += 1

        status_counts = dict(Counter(camera_state_map.values()))
        malfunction_counts = dict(Counter(camera_malfunction.values()))

        vehicles = Vehicle.query.all()
        vehicles_states = VehicleState.query.all()
        vehicle_map = {}
        vehicles_types = {'Car': 0, 'Bus': 0, 'Van': 0}
        vehicle_status = {}
        #camera_state_map = {}
        #camera_malfunction_map = {}
        
        for vehicle in vehicles:
            vehicles_types[vehicle.type] +=1

            if vehicle.type not in vehicle_status:
                vehicle_status[vehicle.type] = {'Entering': 0, 'Exiting': 0, 'Moving Inside': 0}
        
            if vehicle.location not in vehicle_map:
                vehicle_map[vehicle.location] = {'Car': 0, 'Bus': 0, 'Van': 0}
            
            vehicle_map[vehicle.location][vehicle.type] += 1
            
            
        for state in vehicles_states:
            if state.status:
                vehicle_status[state.vehicle.type][state.status] += 1
            

        # Render the template with the context object to generate the HTML response
        return render_template('dashboard.html', user=user, status_counts=status_counts, 
                            malfunction_counts=malfunction_counts, camera_malfunction_map=camera_malfunction_map,
                            parking_states=parking_states, vehicle_map=vehicle_map, vehicles_types=vehicles_types, vehicle_status=vehicle_status)
    

    else:
        return redirect(url_for('pages_login'))

 









