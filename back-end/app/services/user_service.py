# app/services/user_service.py

from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import User

# Stockage en mémoire pour la démonstration.
# Dans un vrai projet, ces opérations pointeraient vers une base de données.
USERS: List[User] = []


def get_all_users() -> List[User]:
    """
    Retourne la liste complète des utilisateurs.
    Cette fonction n'est utilisée que pour du debug ou un futur tableau admin.
    """
    return USERS


def get_user_by_email(email: str) -> Optional[User]:
    """
    Recherche d'un utilisateur par email.
    Insensible à la casse (lower()), ce qui évite des doublons absurdes.
    Retourne :
      - User → trouvé
      - None → non trouvé
    """
    return next((u for u in USERS if u.email.lower() == email.lower()), None)


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Recherche d'un utilisateur par identifiant.
    Même principe que get_user_by_email, mais basé sur l'id.
    """
    return next((u for u in USERS if u.id == user_id), None)


def create_user(email: str, password: str, role: str = "user") -> User:
    """
    Crée un nouvel utilisateur.
    Ce service gère :
      - le contrôle d'unicité de l'email,
      - le hash du mot de passe,
      - l'assignation d'un id auto-incrémenté,
      - l'ajout en mémoire.

    En cas d'email déjà utilisé :
      → on lève une exception ValueError, que le contrôleur transformera en 409.
    """
    # Vérification de l'unicité de l'email
    existing = get_user_by_email(email)
    if existing:
        raise ValueError("Un utilisateur avec cet email existe déjà.")

    # Attribution d'un nouvel id (logique simplifiée pour la démo)
    new_id = max((u.id for u in USERS), default=0) + 1

    # Hash du mot de passe (indispensable pour ne jamais stocker de plain-text)
    password_hash = generate_password_hash(password)

    # Création du User (model)
    user = User(
        id=new_id,
        email=email,
        password_hash=password_hash,
        role=role
    )

    # Enregistrement dans la "table" en mémoire
    USERS.append(user)
    return user


def verify_credentials(email: str, password: str) -> Optional[User]:
    """
    Vérifie les identifiants envoyés lors du login.
    Étapes :
      1. Récupération de l'utilisateur via l'email.
      2. Comparaison du mot de passe fourni avec le hash stocké.
    
    check_password_hash() s'occupe de :
      - reproduire le hash du mot de passe entré,
      - le comparer au hash enregistré,
      - gérer les attaques usuelles (timing, salts internes…).

    Retour :
      - User → si email correct + mot de passe valide
      - None → sinon
    """
    user = get_user_by_email(email)
    if not user:
        return None

    if not check_password_hash(user.password_hash, password):
        return None

    return user
