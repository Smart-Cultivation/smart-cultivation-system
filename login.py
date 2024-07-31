from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash
from database.model.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
from form.form_login import LoginForm
import json

bp = Blueprint("login", __name__, url_prefix="/login")


@bp.route("/", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("smart_cultivation_system.get_all_ponds"))

    form = LoginForm()

    if form.validate_on_submit():
        requested_user = User.query.filter_by(email=form.email.data).first()
        if not requested_user:
            flash("The email does not exist, please try again.")
            return redirect(url_for("login.login"))

        elif not check_password_hash(requested_user.password_hash, form.password.data):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login.login"))

        else:
            login_user(requested_user)
            return redirect(url_for("smart_cultivation_system.get_all_ponds"))

    return render_template("pages/smart_cultivation_system/login.html", form=form)
