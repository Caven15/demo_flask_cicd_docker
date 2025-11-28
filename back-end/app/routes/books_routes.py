# app/routes/books_routes.py

from flask import Blueprint
import app.controllers.book_controller as book_controller

books_bp = Blueprint("books", __name__)

# Routes publiques
books_bp.add_url_rule(
    "/api/books",
    view_func=book_controller.get_books,
    methods=["GET"],
)

books_bp.add_url_rule(
    "/api/books/<int:id>",
    view_func=book_controller.get_book,
    methods=["GET"],
)

books_bp.add_url_rule(
    "/api/books/search",
    view_func=book_controller.search_book,
    methods=["GET"],
)

# Routes protégées (JWT dans les contrôleurs)
books_bp.add_url_rule(
    "/api/books",
    view_func=book_controller.create_book,
    methods=["POST"],
)

books_bp.add_url_rule(
    "/api/books/<int:id>",
    view_func=book_controller.update_book_full,
    methods=["PUT"],
)

books_bp.add_url_rule(
    "/api/books/<int:id>",
    view_func=book_controller.update_book_partial,
    methods=["PATCH"],
)

books_bp.add_url_rule(
    "/api/books/<int:id>",
    view_func=book_controller.remove_book,
    methods=["DELETE"],
)
