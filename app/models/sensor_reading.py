from models.shared import db


class SensorReading(db.Model):
    __tablename__ = "sensor_reading"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Float, nullable=False)
    value = db.Column(db.Float, nullable=False)
    sensor = db.Column(db.Integer, db.ForeignKey("sensor.id"))