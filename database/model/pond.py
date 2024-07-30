from datetime import datetime
from database.mysql import db

class Pond(db.Model):
    __tablename__ = 'ponds'
    
    pond_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pond_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    water_qualities = db.relationship("WaterQuality", backref="pond", lazy=True)
    fish_data = db.relationship("FishData", backref="pond", lazy=True)
    metrics = db.relationship("FishPondMetrics", backref="pond", lazy=True)

    def __init__(self, pond_name, location=None):
        self.pond_name = pond_name
        self.location = location

    def to_dict(self):
        return {
            "pond_id": self.pond_id,
            "pond_name": self.pond_name,
            "location": self.location,
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        }

class WaterQuality(db.Model):
    __tablename__ = 'water_qualities'
    
    water_quality_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pond_id = db.Column(db.Integer, db.ForeignKey('ponds.pond_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pH = db.Column(db.Float, nullable=False)
    turbidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    nitrate = db.Column(db.Float, nullable=False)

    def __init__(self, pond_id, pH, turbidity, temperature, nitrate, date=None):
        self.pond_id = pond_id
        self.pH = pH
        self.turbidity = turbidity
        self.temperature = temperature
        self.nitrate = nitrate
        if date:
            self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "water_quality_id": self.water_quality_id,
            "pond_id": self.pond_id,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "pH": self.pH,
            "turbidity": self.turbidity,
            "temperature": self.temperature,
            "nitrate": self.nitrate
        }

class FishData(db.Model):
    __tablename__ = 'fish_data'
    
    fish_data_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pond_id = db.Column(db.Integer, db.ForeignKey('ponds.pond_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fish_weight = db.Column(db.Float, nullable=False)
    fish_height = db.Column(db.Float, nullable=False)
    fish_population = db.Column(db.Integer, nullable=False)

    def __init__(self, pond_id, fish_weight, fish_height, fish_population, date=None):
        self.pond_id = pond_id
        self.fish_weight = fish_weight
        self.fish_height = fish_height
        self.fish_population = fish_population
        if date:
            self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "fish_data_id": self.fish_data_id,
            "pond_id": self.pond_id,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "fish_weight": self.fish_weight,
            "fish_height": self.fish_height,
            "fish_population": self.fish_population
        }

class FishPondMetrics(db.Model):
    __tablename__ = 'fish_pond_metrics'
    
    metric_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pond_id = db.Column(db.Integer, db.ForeignKey('ponds.pond_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_fish_weight = db.Column(db.Float, nullable=False)
    average_fish_weight = db.Column(db.Float, nullable=False)
    average_fish_height = db.Column(db.Float, nullable=False)
    total_population = db.Column(db.Integer, nullable=False)

    def __init__(self, pond_id, total_fish_weight, average_fish_weight, average_fish_height, total_population, date=None):
        self.pond_id = pond_id
        self.total_fish_weight = total_fish_weight
        self.average_fish_weight = average_fish_weight
        self.average_fish_height = average_fish_height
        self.total_population = total_population
        if date:
            self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "metric_id": self.metric_id,
            "pond_id": self.pond_id,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "total_fish_weight": self.total_fish_weight,
            "average_fish_weight": self.average_fish_weight,
            "average_fish_height": self.average_fish_height,
            "total_population": self.total_population
        }
