# app/routes/routes.py

from flask import Flask
from .books_routes import books_bp
from .auth_routes import auth_bp

def init_routes(app: Flask) -> None:
    """
    Enregistre tous les blueprints de l'application.
    Ici on se contente de brancher les groupes de routes
    (livres, auth, etc.) sur l'app Flask.
    """
    app.register_blueprint(books_bp)
    app.register_blueprint(auth_bp)
