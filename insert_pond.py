from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from auth import auth
from rate_limiter import limiter
from database.model.pond import Pond
from database.mysql import db, format_database_error
from form.form_insert import InsertPondForm

bp = Blueprint("mysql", __name__, url_prefix="/pond")

@bp.route("/insert/", methods=["POST", "GET"])
def insert_data():
    form = InsertPondForm()

    if form.validate_on_submit():
        pond_name = form.pond_name.data
        location = form.location.data

        pond = Pond(
            pond_name=pond_name,
            location=location
        )
        db.session.add(pond)
        db.session.commit()

        return redirect(url_for("smart_cultivation_system.smart_cultivation_system"))
    return render_template(
        "pages/smart_cultivation_system/insert_pond.html", form=form
    )

@bp.route("/api/insert/", methods=["POST", "GET"])
@limiter.limit("5 per minute")
@auth.login_required()
def insert_data_api():
    if request.method == "POST":
        pond_name = request.form.get("pond_name")
        location = request.form.get("location")

        if not pond_name:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            pond = Pond(
                pond_name=pond_name,
                location=location
            )
            db.session.add(pond)
            db.session.commit()
            return (
                jsonify(
                    {
                        "status": {
                            "code": 201,
                            "message": "Pond created successfully",
                        },
                        "pond": {
                            "pond_id": pond.pond_id,
                            "pond_name": pond_name,
                            "location": location,
                        },
                    }
                ),
                201,
            )
        except Exception as e:
            db.session.rollback()
            error_msg = format_database_error(e)
            return (
                jsonify(
                    {
                        "status": {"code": 500, "message": error_msg},
                        "data": None,
                    }
                ),
                500,
            )
    else:
        return (
            jsonify(
                {"status": {"code": 405, "message": "Method not allowed"}, "data": None}
            ),
            405,
        )
