from app.models.book_model import Book

# Jeu de données en mémoire pour la démo.
# Dans une vraie application, cette partie serait remplacée par une base SQL.
BOOKS = [
    Book(1, "Harry Potter", "JK Rowling"),
    Book(2, "ça", "Stephen King"),
    Book(3, "La Bible", "Dieu"),
]


def get_all() -> list[Book]:
    """
    Retourne l'ensemble des livres disponibles.
    Le service ne renvoie pas du JSON, mais des objets Book.
    Le contrôleur transformera ensuite en dict pour l'API.
    """
    return BOOKS


def get_book_by_id(book_id: int) -> Book | None:
    """
    Recherche un livre par son identifiant.
    Utilise next() avec une expression génératrice,
    ce qui permet de trouver le premier match puis arrêter immédiatement.
    Retourne None si rien n'est trouvé.
    """
    return next((b for b in BOOKS if b.id == book_id), None)


def add_book(title: str, author: str) -> Book:
    """
    Ajoute un nouveau livre dans la liste.
    L'id est généré simplement :
      - si la liste n'est pas vide → max(id) + 1
      - si vide → id = 1
    Cette logique serait gérée par l'auto-incrément de la DB dans un vrai projet.
    """
    new_id = max(b.id for b in BOOKS) + 1 if BOOKS else 1
    new_book = Book(new_id, title, author)
    BOOKS.append(new_book)
    return new_book


def update_book(book_id: int, title: str, author: str) -> Book | None:
    """
    Mise à jour complète (PUT).
    On remplace entièrement :
      - le titre
      - l'auteur
    Si le livre n'existe pas → None (le contrôleur renverra la 404).
    """
    book = get_book_by_id(book_id)
    if book:
        book.title = title
        book.author = author
        return book
    return None


def patch_book(book_id: int, data: dict) -> Book | None:
    """
    Mise à jour partielle (PATCH).
    Seuls les champs présents dans 'data' sont modifiés.
    Exemple :
        {"author": "Tolkien"} → seul l'auteur change.
    Cette approche respecte l'idée du PATCH côté API REST.
    """
    book = get_book_by_id(book_id)
    if not book:
        return None

    if "title" in data:
        book.title = data["title"]
    if "author" in data:
        book.author = data["author"]

    return book


def delete_book(book_id: int) -> bool:
    """
    Supprime un livre si l'id existe.
    Retourne :
      - True → suppression réussie
      - False → id introuvable
    Le contrôleur transforme ensuite ça en réponse HTTP (204 ou 404).
    """
    book = get_book_by_id(book_id)
    if not book:
        return False

    BOOKS.remove(book)
    return True


def search_book_by_author(author: str) -> list[Book]:
    """
    Recherche simple par auteur :
    - insensible à la casse,
    - recherche d'une sous-chaîne (ex : "king" match "Stephen King").
    Ce service renvoie des objets Book, que le contrôleur convertira ensuite en dict.
    """
    return [b for b in BOOKS if author.lower() in b.author.lower()]
