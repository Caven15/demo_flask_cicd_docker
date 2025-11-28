# app/models/user_model.py

from dataclasses import dataclass

@dataclass
class User:
    """
    Modèle simple représentant un utilisateur.
    Pour la démo, on stocke les données en mémoire (pas de DB).
    """
    id: int
    email: str
    password_hash: str
    role: str = "user"  # ex: "user", "admin"

    def to_dict(self) -> dict:
        """Conversion utilitaire vers dict (sans le password_hash)."""
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role
        }
