from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict


@dataclass
class BookCreateDTO:
    """
    Représente les données nécessaires pour créer un livre.
    La dataclass permet d’obtenir automatiquement :
      - un constructeur
      - un repr lisible
      - une structuration claire des champs
    Pour cette opération, title et author sont obligatoires.
    """
    title: str
    author: str

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["BookCreateDTO"], Optional[Dict]]:
        """
        Convertit un JSON envoyé par le front en un BookCreateDTO valide.
        Retourne :
          (DTO, None) si tout est correct
          (None, {"error": "..."} ) en cas de données incorrectes

        Ce pattern simplifie beaucoup le contrôleur : il n’a plus qu’à tester err.
        """

        if not data:
            return None, {"error": "Aucune donnée fournie"}

        title = data.get("title")
        author = data.get("author")

        # Vérification du type pour éviter les erreurs (ex : un entier au lieu d'une string).
        if not isinstance(title, str) or not isinstance(author, str):
            return None, {"error": "Les champs title et author doivent être des chaînes de caractères"}

        # On nettoie pour éviter les titres avec uniquement des espaces.
        title = title.strip()
        author = author.strip()

        # Règles métier simples côté API.
        if not title:
            return None, {"error": "Le titre ne peut pas être vide."}
        if len(title) > 100:
            return None, {"error": "Le titre ne peut pas dépasser 100 caractères."}

        # Débogage ponctuel (à retirer en production).
        print("---------------------------------------")
        print(author)
        print("---------------------------------------")

        if not author:
            return None, {"error": "Le nom de l'auteur est obligatoire"}
        if len(author) < 3:
            return None, {"error": "Le nom de l'auteur doit contenir au moins 3 caractères"}

        # Toutes les validations sont OK → on construit le DTO.
        return BookCreateDTO(title=title, author=author), None


@dataclass
class BookUpdateDTO:
    """
    DTO utilisé pour un PUT (mise à jour complète).
    Même structure que BookCreateDTO, mais on peut lui ajouter
    des règles spécifiques si un jour PUT ≠ POST.
    """
    title: str
    author: str

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["BookUpdateDTO"], Optional[Dict]]:
        if not data:
            return None, {"error": "Données manquantes pour la mise à jour complète"}

        # On réutilise la logique de validation du CreateDTO,
        # ce qui évite la duplication de code.
        dto, err = BookCreateDTO.from_json(data)
        if err:
            return None, err

        # dto contient déjà les valeurs valides.
        return BookUpdateDTO(title=dto.title, author=dto.author), None


@dataclass
class BookPatchDTO:
    """
    DTO pour une mise à jour partielle (PATCH).
    Ici, aucun champ n’est obligatoire : on modifie uniquement ce qui est fourni.
    Les champs sont optionnels, d'où l'utilisation de Optional + field(default=None).
    """
    title: Optional[str] = field(default=None)
    author: Optional[str] = field(default=None)

    @staticmethod
    def from_json(data: dict) -> Tuple[Optional["BookPatchDTO"], Optional[Dict]]:
        if not data:
            return None, {"error": "Aucune donnée fournie pour la mise à jour partielle"}

        # On récupère uniquement les champs potentiels
        title = data.get("title")
        author = data.get("author")

        # Aucun champ valide → erreur logique.
        if title is None and author is None:
            return None, {"error": "Aucun champ valide à mettre à jour"}

        # Validation ciblée pour chaque champ présent :
        if title is not None:
            if not isinstance(title, str):
                return None, {"error": "Le titre doit être une chaîne de caractères"}
            title = title.strip()
            if len(title) > 100:
                return None, {"error": "Le titre ne peut pas dépasser 100 caractères"}

        if author is not None:
            if not isinstance(author, str):
                return None, {"error": "L'auteur doit être une chaîne de caractères"}
            author = author.strip()
            if len(author) < 3:
                return None, {"error": "L'auteur doit contenir au moins 3 caractères"}

        # On construit le DTO avec uniquement les valeurs réellement fournies.
        return BookPatchDTO(title=title, author=author), None
