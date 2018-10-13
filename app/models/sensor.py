from models.shared import db
import enum
class SensorType(enum.Enum):
    binary = 0
    range = 1


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(SensorType))
    threshold = db.Column(db.Float, nullable=False)
    node = db.Column(db.Integer, db.ForeignKey("sensor_node.id"))
    last_reading = db.Column(db.Integer, db.ForeignKey("sensor_reading.id"))