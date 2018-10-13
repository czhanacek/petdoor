
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


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
#@app.route(web + "register", methods=["POST"])

