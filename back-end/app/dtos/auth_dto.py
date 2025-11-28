from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any


@dataclass
class LoginDTO:
    """
    Représente les données nécessaires pour un login.
    Un DTO sert ici à :
      - centraliser la validation,
      - garantir que le contrôleur reçoit des données propres,
      - éviter la logique de vérification dans les routes Flask.
    """
    email: str
    password: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Tuple[Optional["LoginDTO"], Optional[dict]]:
        """
        Transforme un JSON brut reçu depuis le front en un LoginDTO valide.
        Retourne un tuple :
          (dto, erreur)
          - dto : l’objet construit si tout est bon
          - erreur : un dict décrivant les problèmes détectés
        """
        errors: dict[str, str] = {}

        # On récupère les champs du JSON.
        email = data.get("email")
        password = data.get("password")

        # Vérifications minimales : les deux champs doivent exister.
        if not email:
            errors["email"] = "L'email est requis."
        if not password:
            errors["password"] = "Le mot de passe est requis."

        # S'il y a des erreurs, on les renvoie dans un format lisible par le contrôleur.
        if errors:
            return None, {"errors": errors}

        # Tout est correct → création du DTO prêt à être utilisé.
        return cls(email=email, password=password), None


@dataclass
class RegisterDTO:
    """
    Représente les données attendues pour l'inscription d'un utilisateur.
    On y valide :
      - la présence des champs,
      - la cohérence password / confirmPassword.
    """
    email: str
    password: str
    confirm_password: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Tuple[Optional["RegisterDTO"], Optional[dict]]:
        """
        Même principe que LoginDTO, mais avec plus de règles :
        - vérification des 3 champs
        - correspondance entre password et confirmPassword
        """
        errors: dict[str, str] = {}

        email = data.get("email")
        password = data.get("password")

        # Le champ de confirmation peut venir en camelCase (Angular) ou snake_case
        confirm_password = data.get("confirmPassword") or data.get("confirm_password")

        # Présence obligatoire des trois champs
        if not email:
            errors["email"] = "L'email est requis."
        if not password:
            errors["password"] = "Le mot de passe est requis."
        if not confirm_password:
            errors["confirmPassword"] = "La confirmation du mot de passe est requise."

        # Vérification de la correspondance
        if password and confirm_password and password != confirm_password:
            errors["passwordMatch"] = "Les mots de passe ne correspondent pas."

        # S'il y a des erreurs → retour immédiat
        if errors:
            return None, {"errors": errors}

        # Sinon, on construit un DTO validé.
        return cls(email=email, password=password, confirm_password=confirm_password), None
