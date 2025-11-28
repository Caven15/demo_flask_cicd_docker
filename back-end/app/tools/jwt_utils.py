# app/tools/jwt_utils.py

import datetime
from typing import Tuple, Optional, Dict, Any

import jwt

# !!! Clé définie en dur pour la démonstration !!!
# Dans un vrai projet :
#   - la clé doit être stockée dans une variable d'environnement
#   - jamais commitée dans un dépôt Git
JWT_SECRET = "CHANGE_ME_SUPER_SECRET"
JWT_ALGO = "HS256"


def create_access_token(user_id: int, email: str, role: str, expires_in: int = 3600) -> str:
    """
    Génère un token JWT signé.
    Le JWT contient :
      - sub : identifiant de l’utilisateur
      - email : utile côté front pour l'affichage / stores
      - role : pour les autorisations (admin, user, etc.)
      - iat : date de création du token (issued at)
      - exp : date d'expiration (gestion de session)

    Le front Angular recevra ce token et le stockera via un TokenService.
    """
    now = datetime.datetime.utcnow()

    payload = {
        # Identifiant principal (subject)
        "sub": user_id,
        "email": email,                                # Info de profil utile côté front
        "role": role,                                  # Utilisé pour vérifier les droits
        "iat": now,                                    # Moment où le token a été créé
        # Expiration (1h par défaut)
        "exp": now + datetime.timedelta(seconds=expires_in),
    }

    # jwt.encode signe le token avec l'algorithme choisi.
    # Le résultat est déjà une chaîne utilisable dans les headers Authorization.
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return token


def verify_access_token(token: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, str]]]:
    """
    Vérifie et décode un token JWT reçu dans un header Authorization.
    Retourne :
      - (payload, None) → token valide
      - (None, {error: ...}) → token expiré ou invalide

    Cette fonction est utilisée par les middlewares require_auth et require_role.
    """

    try:
        # Vérifie la signature + l'expiration.
        # Si tout est bon, on récupère le payload original (sub, email, role…).
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload, None

    except jwt.ExpiredSignatureError:
        # L'expiration est gérée automatiquement par PyJWT.
        return None, {"error": "Token expiré."}

    except jwt.InvalidTokenError:
        # Mauvaise signature, token modifié, format incorrect, etc.
        return None, {"error": "Token invalide."}
