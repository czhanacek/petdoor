from models.shared import db

class SensorNode(db.Model):
    __tablename__ = "sensor_node"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, default=lambda: str(uuid.uuid4().int()), 
        nullable=False, unique=True)
    mac = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String)
    location = db.Column(db.String)