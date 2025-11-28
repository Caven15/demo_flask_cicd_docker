# app/routes/auth_routes.py

from flask import Blueprint
import app.controllers.auth_controllers as auth_controller

auth_bp = Blueprint("auth", __name__)

auth_bp.add_url_rule(
    "/api/auth/register",
    view_func=auth_controller.register,
    methods=["POST"],
)

auth_bp.add_url_rule(
    "/api/auth/login",
    view_func=auth_controller.login,
    methods=["POST"],
)
