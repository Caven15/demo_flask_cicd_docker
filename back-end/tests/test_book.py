# tests/test_book.py
# Ce fichier regroupe tous les tests de l'API /api/books.
# L'idée est de couvrir le cycle complet :
# - Lecture (GET, recherche)
# - Création (POST)
# - Mise à jour complète (PUT)
# - Mise à jour partielle (PATCH)
# - Suppression (DELETE)
#
# Chaque test simule un appel HTTP sur le back Flask à l'aide du client de test
# (fixture `client` définie dans conftest.py) sans lancer de vrai serveur.

#region GET
def test_get_all_books(client):
    """
    Vérifie que la route GET /api/books renvoie :
    - un statut HTTP 200
    - une liste de livres
    - exactement 3 livres au démarrage (jeu de données fake)
    - un schéma JSON cohérent (id, title, author)
    """

    # Quand / When : on appelle la route sans paramètres
    response = client.get("/api/books")

    # Alors / Then : on s'attend à une réponse OK et à une liste de livres
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3  # Correspond aux fake data de départ

    # Vérification basique de notre schéma : on contrôle les clés du premier élément
    assert set(data[0].keys()) == {"id", "title", "author"}


def test_get_book_not_found(client):
    """
    GET /api/books/999
    Cas où l'on demande un livre qui n'existe pas.
    L'API doit renvoyer une 404 avec un message d'erreur explicite.
    """
    response = client.get("/api/books/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Livre non trouvé"


def test_get_single_book(client):
    """
    GET /api/books/1
    Cas nominal : on récupère un livre existant.
    On vérifie que le titre et l'auteur correspondent à nos données de test.
    """
    response = client.get("/api/books/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Harry Potter"
    assert data["author"] == "JK Rowling"


def test_search_books(client):
    """
    GET /api/books/search?author=Dieu
    Test de la route de recherche.
    On vérifie que :
    - la route répond 200
    - le JSON renvoyé est une liste
    - tous les livres retournés contiennent 'Dieu' dans l'auteur
    """
    response = client.get("/api/books/search?author=Dieu")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # all(...) permet de vérifier que la condition est vraie pour chaque élément de la liste
    assert all("Dieu" in b["author"] for b in data)

# endregion

#region POST
def test_post_book(client, auth_headers):
    """
    POST /api/books
    On vérifie :
    - que l'on peut créer un nouveau livre via un JSON minimal (title, author)
    - que la route renvoie 201 (création)
    - que le nombre total de livres a bien augmenté de 1.
    """

    # 1) On récupère d'abord la longueur avant l'ajout
    response_before = client.get("/api/books")
    count_before = len(response_before.get_json())

    # 2) On prépare le livre à ajouter
    new_book = {
        "title": "DevWeb",
        "author": "Bstorm",
    }

    # 3) Appel de la route protégée → on ajoute les headers d'authentification
    response = client.post("/api/books", json=new_book, headers=auth_headers)

    # 4) Contrôle du statut et du contenu renvoyé
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "DevWeb"
    assert data["author"] == "Bstorm"

    # 5) Vérification que la taille de la liste a bien augmenté
    response_after = client.get("/api/books")
    count_after = len(response_after.get_json())
    assert count_after == count_before + 1

# endregion

#region PUT
def test_put_book(client, auth_headers):
    """
    PUT /api/books/1
    Test d'une mise à jour complète (remplacement des champs).
    Ici, on écrase entièrement le titre et l'auteur du livre 1.
    """
    # Données complètes pour le replace
    updated_data = {
        "title": "test_update_title",
        "author": "test_update_author",
    }

    # Appel PUT avec JSON + headers d'authentification
    response = client.put("/api/books/1", json=updated_data, headers=auth_headers)

    # La route doit répondre 200 et renvoyer les nouvelles valeurs
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "test_update_title"
    assert data["author"] == "test_update_author"


def test_put_book_not_found(client, auth_headers):
    """
    PUT /api/books/999
    Même logique que pour le GET not found :
    si le livre n'existe pas, on attend une 404.
    """
    response = client.put(
        "/api/books/999",
        json={"title": "titi", "author": "toto"},
        headers=auth_headers,
    )
    assert response.status_code == 404

# endregion

#region PATCH
def test_patch_book(client, auth_headers):
    """
    PATCH /api/books/2
    Mise à jour partielle : on ne modifie ici que l'auteur du livre 2.
    L'objectif est de montrer la différence avec PUT (qui remplace tout).
    """
    response = client.patch(
        "/api/books/2",
        json={"author": "Laboon"},  # On ne touche pas au titre
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.get_json()
    # On vérifie que l'auteur a bien été modifié
    assert data["author"] == "Laboon"
    # Et qu'on reçoit toujours un titre (il n'a pas été écrasé)
    assert "title" in data


def test_patch_book_not_found(client, auth_headers):
    """
    PATCH /api/books/999
    Cas d'erreur : tentative de mise à jour partielle sur un livre inexistant.
    On attend logiquement une 404.
    """
    response = client.patch(
        "/api/books/999",
        json={"title": "Inconnu"},
        headers=auth_headers,
    )
    assert response.status_code == 404

# endregion

#region DELETE
def test_delete_book(client, auth_headers):
    """
    DELETE /api/books/<id>
    Scénario complet :
    1) on crée un nouveau livre via POST
    2) on vérifie la taille actuelle de la liste
    3) on supprime ce livre
    4) on confirme que la taille a diminué d'une unité.
    """

    # 1) Création d'un livre à supprimer (on évite de jouer avec les données initiales)
    new_book = {
        "title": "DevWeb",
        "author": "Bstorm",
    }
    create_response = client.post(
        "/api/books",
        json=new_book,
        headers=auth_headers,
    )
    assert create_response.status_code == 201
    created = create_response.get_json()
    created_id = created["id"]  # On récupère l'id du livre fraichement créé

    # 2) Taille avant suppression
    before = len(client.get("/api/books").get_json())

    # 3) On supprime le livre ajouté
    response = client.delete(f"/api/books/{created_id}", headers=auth_headers)
    # 204 = "No Content" → la suppression s'est bien passée, rien à renvoyer dans le body
    assert response.status_code == 204

    # 4) Vérifie que la taille a diminué
    after = len(client.get("/api/books").get_json())
    assert after == before - 1


def test_delete_book_not_found(client, auth_headers):
    """
    DELETE /api/books/999
    Suppression d'un livre inexistant.
    On vérifie que l'API signale correctement l'erreur (404).
    """
    response = client.delete("/api/books/999", headers=auth_headers)
    assert response.status_code == 404

# endregion