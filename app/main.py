
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import flask_sqlalchemy as sqlalchemy
from flask_cors import CORS
import uuid
from models.shared import db
from models.sensor import Sensor, SensorType
from models.sensor_reading import SensorReading
from models.sensor_node import SensorNode

from models.systemstats import systemstats


sensors = "/sensors/"
web = "/web/"



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security_system.db'
    db.init_app(app)
    print("created app!")
    
    return app

app = create_app()
app.app_context().push()
db.create_all() # the order of this and the previous 2 lines is important

def validatePasscode(request):
    passcode = request.form.get("passcode", None)
    if(passcode != systemstats.passcode):
        return False
    else:
        return True


@app.route(sensors + "register", methods=["POST"])
def register():
    mac_address = request.form.get('mac', None)
    if(mac_address == None):
        return str(-1), 500 # return error
    
    # Now that we can be sure we got what we needed
    
    # Check to see if MAC address is already in database
    query = SensorNode.query.filter_by(mac=str(mac_address)).limit(1)

    if(query.count() == 1):
        # sensor node has already been registered 
        # (or we have a mac address collision!)
        print(str(query))
    else:
        newNode = SensorNode(
            mac=mac_address
        )
        db.session.add(newNode)
        db.session.commit()
    
    return str(1)

@app.route(web + "check_passcode", methods=["POST"])
def check_passcode():
    response = {}
    submitted_passcode = request.form.get("passcode", None)
    if(submitted_passcode == None):
        errors = []
        result = "bad"
        response["result"] = result
        errors.append("no passcode submitted")
        response["errors"] = errors
        return jsonify(response), 500
    
    if(submitted_passcode != systemstats.passcode):
        result = "bad_pass"
    else:
        result = "good_pass"
    response["result"] = result
    return jsonify(response)

@app.route(web + "get_sensors", methods=["POST"])
def get_sensors():
    response = {}
    if(not validatePasscode(request)):
        response["errors"] = ["bad_pass"]
        return jsonify(response), 200
    
    sensorlist = []
    for sensor in db.session.query(SensorNode).all():
        sensor.__dict__.pop("_sa_instance_state")
        sensorlist.append(sensor.__dict__)
    response["sensors"] = sensorlist
    return jsonify(response), 200

@app.route(web + "update_sensor", methods=["POST"])
def update_sensor():
    response = {}
    if(not validatePasscode(request)):
        response["errors"] = ["bad_pass"]
        return jsonify(response), 200
    query = SensorNode.query.filter_by(id=request.form.get("id")).first()
    if(query == None):
        response["errors"] = ["invalid_id"]
    else:
        query.name = request.form.get("name")
        query.location = request.form.get("location")
        if(query.sensors == []):
            newSensor = Sensor(
                type=request.form.get("type"),
                threshold=request.form.get("threshold")
            )
            db.session.add(newSensor)
            db.session.add(query)
            query.sensors.append(newSensor)
            db.session.commit()
        else:
            query.sensors[0].type = request.form.get("type")
            query.sensors[0].threshold = request.form.get("threshold")
            db.session.commit()
        query = SensorNode.query.filter_by(id=request.form.get("id")).first()
        sensor = db.session.query(SensorNode).filter_by(id=request.form.get("id")).first()
        sensorsdict = sensor.sensors[0].__dict__
        sensor.__dict__.pop("_sa_instance_state")
        
        sensorsdict = sensor.sensors[0].__dict__
        sensorsdict.pop("_sa_instance_state")
        
        sensor.__dict__.pop("sensors")
        
        print(str(sensor.__dict__))
        
        #sensor.sensor.__dict__.pop("_sa_instance_state")
        response["sensor"] = sensor.__dict__
        response["sensor"]["sensors"] = sensorsdict
        #response["sensor"] = sensor.sensors[0].__dict__
        
    return jsonify(response)
        
    
    
    

#@app.route(web + "register", methods=["POST"])

