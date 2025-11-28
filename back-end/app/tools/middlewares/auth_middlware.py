# app/middlewares/auth_middleware.py

from functools import wraps
from typing import Callable, Any

from flask import request, jsonify
from app.tools.jwt_utils import verify_access_token


def _extract_token_from_header() -> tuple[str | None, dict | None]:
    """
    On récupère le JWT envoyé dans l’en-tête Authorization.
    Format attendu :
        Authorization: Bearer <token>
    C’est vraiment juste l’extraction ici, aucune vérification.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, {"error": "En-tête Authorization manquant ou invalide."}

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return None, {"error": "Token JWT manquant."}

    return token, None


def require_auth(f: Callable) -> Callable:
    """
    Middleware placé devant une route pour vérifier qu’il y a bien un utilisateur connecté.
    
    Petit rappel utile :
    ---------------------
    Le but d’un middleware ici, c’est d’éviter de répéter
    dans chaque contrôleur tout le code qui vérifie le token.
    On “filtre” la requête avant qu’elle n’arrive réellement à la route.

    En clair :
      - si le token est présent et valide → on laisse passer
      - sinon → on arrête tout de suite (401) et la route ne s’exécute même pas
    """

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any):
        # On tente de récupérer le token envoyé par le client
        token, err = _extract_token_from_header()
        if err:
            return jsonify(err), 401

        # Vérification du JWT (signature + expiration)
        payload, verif_err = verify_access_token(token)
        if verif_err:
            return jsonify(verif_err), 401

        # Ici, on pourrait garder le payload dans request
        # (pratique pour savoir qui est connecté dans le contrôleur)
        # request.user = payload

        # L’utilisateur a passé le contrôle → la vraie route peut tourner
        return f(*args, **kwargs)

    return wrapper


def require_role(required_role: str) -> Callable:
    """
    Variante du middleware au-dessus, mais avec une vérification de rôle.
    
    Idée simple :
    ---------------------
    On ne demande pas seulement "est-ce que tu es connecté ?"
    mais "est-ce que tu as le droit de faire ça ?".
    
    Exemple classique :
        @require_role("admin")
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any):
            # Même logique d’auth que require_auth
            token, err = _extract_token_from_header()
            if err:
                return jsonify(err), 401

            payload, verif_err = verify_access_token(token)
            if verif_err:
                return jsonify(verif_err), 401

            # On regarde le rôle indiqué dans le JWT
            role = payload.get("role")

            # Si le rôle ne correspond pas, l’accès est refusé
            if role != required_role:
                return jsonify({
                    "error": "Accès refusé.",
                    "detail": f"Rôle requis : {required_role}, rôle actuel : {role!r}",
                }), 403

            # Si tout est bon, la route peut s’exécuter normalement
            return f(*args, **kwargs)

        return wrapper

    return decorator
