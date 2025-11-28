# app/controllers/book_controller.py

from flask import jsonify, request
from app.dtos.book_dto import (
    BookCreateDTO,
    BookUpdateDTO,
    BookPatchDTO,
)
from app.services.book_service import (
    get_all,
    get_book_by_id,
    add_book,
    update_book,
    patch_book,
    delete_book,
    search_book_by_author,
)
from app.tools.middlewares.auth_middlware import require_auth, require_role


def get_books():
    """
    GET /api/books
    Route ouverte : renvoie la liste complète des livres.
    L'objectif est pédagogique : montrer une route publique simple.
    """
    books = get_all()  # Récupération depuis la couche service
    payload = [book.to_dict() for book in books]  # Transformation en JSON prêt pour Angular
    return jsonify(payload), 200


def get_book(id: int):
    """
    GET /api/books/<id>
    On récupère un livre par son identifiant.
    Si l'id est inconnu → 404 et un message compréhensible pour le front.
    """
    book = get_book_by_id(id)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({"error": "Livre non trouvé"}), 404


@require_auth
def create_book():
    """
    POST /api/books
    Route protégée : nécessite un JWT valide (middleware require_auth).
    Le contrôleur délègue la validation du JSON au DTO.
    """
    data = request.get_json()
    dto, err = BookCreateDTO.from_json(data)
    if err:
        return jsonify(err), 400  # Erreur de validation du DTO

    # On envoie les données propres à la couche service pour créer l'objet.
    new_book = add_book(dto.title, dto.author)
    return jsonify(new_book.to_dict()), 201


@require_auth
def update_book_full(id: int):
    """
    PUT /api/books/<id>
    Mise à jour complète : on remplace le titre ET l'auteur.
    Concrètement, si un champ est manquant → erreur côté DTO.
    """
    dto, err = BookUpdateDTO.from_json(request.get_json())
    if err:
        return jsonify(err), 400

    # La couche service s’occupe de la logique métier et du retour.
    updated = update_book(id, dto.title, dto.author)
    if not updated:
        return jsonify({"error": f"Livre avec Id {id} introuvable"}), 404

    return jsonify(updated.to_dict()), 200


@require_auth
def update_book_partial(id: int):
    """
    PATCH /api/books/<id>
    Mise à jour partielle : on modifie uniquement les champs fournis.
    Le DTO permet d'accepter des champs optionnels.
    """
    dto, err = BookPatchDTO.from_json(request.get_json())
    if err:
        return jsonify(err), 400

    # On construit un dictionnaire dynamique contenant uniquement
    # les champs présents dans le JSON (None = non modifié).
    update_data = {k: v for k, v in dto.__dict__.items() if v is not None}

    updated = patch_book(id, update_data)
    if not updated:
        return jsonify({"error": f"Livre avec Id {id} introuvable"}), 404

    return jsonify(updated.to_dict()), 200


@require_role("admin")
def remove_book(id: int):
    """
    DELETE /api/books/<id>
    Route volontairement réservée au rôle "admin".
    Cela illustre la différence entre require_auth (token requis)
    et require_role (token + rôle).
    """
    deleted = delete_book(id)
    if deleted:
        # 204 = succès silencieux (pas de JSON renvoyé)
        return "", 204
    return jsonify({"error": "Livre non trouvé"}), 404


def search_book():
    """
    GET /api/books/search?author=Nom
    Petite route de recherche : on passe un paramètre dans l’URL.
    Si le paramètre est absent → erreur explicite pour guider le front.
    """
    author = request.args.get("author", "")
    if not author:
        return jsonify({"error": "Paramètre 'author' requis"}), 400

    books = search_book_by_author(author)
    return jsonify([b.to_dict() for b in books]), 200
