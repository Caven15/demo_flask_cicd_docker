# tests/conftest.py

import os
import sys
import pytest

# --- Réglage du chemin racine du projet ---
# On récupère le dossier parent (la racine du back)
# afin que les imports "from app import create_app" fonctionnent
# aussi bien dans le projet que pendant l'exécution des tests.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from app.tools.jwt_utils import create_access_token


@pytest.fixture
def client():
    """
    Fournit un client de test Flask.
    Chaque test obtient sa propre instance isolée.
    - Pas besoin de lancer le serveur.
    - On peut appeler les routes directement en interne.
    """
    app = create_app()
    app.testing = True  # Active le mode test (logs moins verbeux, erreurs gérées différemment)
    return app.test_client()


@pytest.fixture
def auth_headers():
    """
    Génère un header Authorization complet pour les tests.

    L'idée :
    - Créer un JWT valide via notre utilitaire interne.
    - Injecter un rôle "admin" pour pouvoir tester les routes protégées :
        * @require_auth
        * @require_role("admin")  (ex: DELETE)
    - Retourner un dictionnaire utilisable directement dans :
        client.get(..., headers=auth_headers)
    """
    token = create_access_token(
        user_id=1,                 # Identité “factice” suffisante pour les tests
        email="test@example.com",  # Pas important, mais crédible
        role="admin",              # 👈 On force le rôle admin ici pour couvrir les routes sensibles
    )
    return {"Authorization": f"Bearer {token}"}
