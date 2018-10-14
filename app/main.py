
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import flask_sqlalchemy as sqlalchemy
from flask_cors import CORS
from models.shared import db
from models.sensor import Sensor, SensorType
from models.sensor_reading import SensorReading
from models.sensor_node import SensorNode

from models.user import aUser


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

@app.route(sensors + "register", methods=["POST"])
def register():
    mac_address = request.args.get('mac', None)
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
    multi_dict = request.args
    for key in multi_dict:
        print(multi_dict.get(key))
        print(multi_dict.getlist(key))
    response = {}
    submitted_passcode = request.args.get("passcode", None)
    if(submitted_passcode == None):
        errors = []
        status = "bad"
        response["status"] = status
        errors.append("no passcode submitted")
        response["errors"] = errors
        return jsonify(response), 500
    
    if(submitted_passcode != aUser.passcode):
        status = "bad_pass"
    else:
        status = "good_pass"
    response["status"] = status
    return jsonify(response)

@app.route(web + "update_passcode", methods=["POST"])
def update_passcode():
    response = {}
    current_passcode = request.args.get("current_passcode", None)
    new_passcode = request.args.get("new_passcode", None)
    errors = []
    status = ""
    if(current_passcode == None or new_passcode == None):
        status = "bad"
        errors.append("one or more passwords not submitted")
    
    if(submitted_passcode != aUser.passcode):
        status = "bad_pass"
    else:
        status = "good_pass"


    response["status"] = status
    if(len(errors) == 0):
        return jsonify(response)
    else:
        response["errors"] = errors
    
    

#@app.route(web + "register", methods=["POST"])

