from flask import Blueprint, render_template
from cache import cache
from database.model.pond import Pond, WaterQuality, FishData, FishPondMetrics

bp = Blueprint("smart_cultivation_system", __name__,
               url_prefix="/smart_cultivation_system")

@bp.route("/")
def smart_cultivation_system():
    ponds = Pond.query.all()
    return render_template("pages/smart_cultivation_system/index.html", ponds=ponds)

@bp.route("/<int:pond_id>")
def smart_cultivation_system_pond(pond_id):
    pond = Pond.query.filter_by(pond_id=pond_id).first()

    waterQualities = WaterQuality.query.filter_by(pond_id=pond_id).all()
    fishData = FishData.query.filter_by(pond_id=pond_id).all()
    metrics = FishPondMetrics.query.filter_by(pond_id=pond_id).all()

    return render_template(
        "pages/smart_cultivation_system/ponds.html",
        pond=pond,
        waterQualities=waterQualities,
        fishData=fishData,
        metrics=metrics,
    )

def get_pond_by_id(pond_id):
    return Pond.query.filter_by(pond_id=pond_id).first()

def get_water_quality_by_pond_id(pond_id):
    return WaterQuality.query.filter_by(pond_id=pond_id).all()

def get_fish_data_by_pond_id(pond_id):
    return FishData.query.filter_by(pond_id=pond_id).all()

def get_metrics_by_pond_id(pond_id):
    return FishPondMetrics.query.filter_by(pond_id=pond_id).all()
