from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash
from cache import cache
from database.model.pond import Pond, WaterQuality, FishData, FishPondMetrics
from database.model.user import User
from database.model.employee import Employee
from werkzeug.security import generate_password_hash, check_password_hash
from database.mysql import db, format_database_error
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from form.form_login import LoginForm
import json

bp = Blueprint(
    "smart_cultivation_system", __name__, url_prefix="/smart_cultivation_system"
)

@bp.route("/")
@login_required
def get_all_ponds():
    # Fetch ponds owned by the current logged-in user
    user_id = current_user.user_id
    ponds = Pond.query.filter_by(owner_id=user_id).all()
    
    return render_template("pages/smart_cultivation_system/index.html", ponds=ponds)

@login_required
@bp.route("/<int:pond_id>")
def smart_cultivation_system_pond(pond_id):
    pond = get_pond_by_id(pond_id)

    if pond is None:
        return "Pond not found", 404

    if pond.owner_id != current_user.user_id:
        return "You do not have permission to access this pond", 403

    waterQualities = get_water_quality_by_pond_id(pond_id)
    fishData = get_fish_data_by_pond_id(pond_id)
    metrics = get_metrics_by_pond_id(pond_id)
    owner = User.query.get(pond.owner_id)  # Fetch owner details
    employees = (
        Employee.query.join(Employee.ponds).filter_by(pond_id=pond_id).all()
    )  # Fetch employees

    # Convert WaterQuality instances to dictionaries
    def water_quality_to_dict(waterQuality):
        return {
            "date": waterQuality.date.strftime("%Y-%m-%d"),
            "pH": waterQuality.pH,
            "turbidity": waterQuality.turbidity,
            "temperature": waterQuality.temperature,
            "nitrate": waterQuality.nitrate,
        }

    # Extract latest water quality metrics
    latestWaterQualities = (
        water_quality_to_dict(waterQualities[-1])
        if waterQualities
        else {"pH": None, "turbidity": None, "temperature": None}
    )

    print(latestWaterQualities)

    # Extract historical data
    historicalWaterQualities = {
        "dates": [w.date.strftime("%Y-%m-%d") for w in waterQualities],
        "ph": [w.pH for w in waterQualities],
        "turbidity": [w.turbidity for w in waterQualities],
        "temperature": [w.temperature for w in waterQualities],
    }
    print(historicalWaterQualities)

    return render_template(
        "pages/smart_cultivation_system/ponds.html",
        pond=pond,
        waterQualities=waterQualities,
        fishData=fishData,
        metrics=metrics,
        owner=owner,
        employees=employees,
        latestWaterQualities=json.dumps(latestWaterQualities),
        historicalWaterQualities=json.dumps(historicalWaterQualities),
    )

def get_pond_by_id(pond_id):
    return Pond.query.filter_by(pond_id=pond_id).first()

def get_water_quality_by_pond_id(pond_id):
    return WaterQuality.query.filter_by(pond_id=pond_id).all()

def get_fish_data_by_pond_id(pond_id):
    return FishData.query.filter_by(pond_id=pond_id).all()

def get_metrics_by_pond_id(pond_id):
    return FishPondMetrics.query.filter_by(pond_id=pond_id).all()
