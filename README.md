# Demo Full-Stack – Angular + Flask  
Application pédagogique destinée à illustrer un flux front/back moderne avec :
- un back-end Python (Flask)
- un front-end Angular
- une API REST structurée
- un système d’authentification JWT
- tests automatisés côté back
- séparation contrôleurs / services / DTO / middlewares
- Blueprints pour organiser les routes


---

## 📂 Structure générale du projet

```
project/
│
├── back-end/
│   ├── app.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── controllers/
│   │   ├── dtos/
│   │   ├── services/
│   │   ├── models/
│   │   ├── tools/
│   │   ├── middlewares/
│   │   └── routes/
│   └── tests/
│
└── front-end/
    ├── package.json
    ├── angular.json
    └── src/app/
```

---

# 1. Front-end Angular

Le front consomme l’API Flask et gère l’authentification via JWT.  
Local : **http://localhost:4200**

### ✨ Points clés

### **Services**
- `AuthService` → login, register, stockage du token, mise à jour du store
- `TokenService` → gestion du JWT (localStorage)
- `BooksService` → appels CRUD sur `/api/books`

### **Intercepteur HTTP**
Injecte automatiquement :
```
Authorization: Bearer <token>
```

### **Store / State**
Un `AuthStore` maintient l’état de l’utilisateur :
- connecté / non connecté
- infos du profil
- rôle (admin/user)

### **Composants principaux**
- Login
- Register
- BooksList
- BookAdd
- BookEdit

---

# 2. Back-end Flask

Local : **http://localhost:5000**

### Architecture du back

- **controllers** → logique HTTP
- **services** → logique métier
- **dtos** → validation des données
- **middlewares** → auth + logs
- **routes (Blueprints)** → organisation du routing
- **models** → objets métier (stockés en mémoire pour la démo)
- **tools** → utilitaires (JWT, etc.)

---

# 3. 📦 Endpoints API

###  Auth
| Méthode |        Route 		 | 			Description 			|
|---------|----------------------|----------------------------------|
|  POST   | `/api/auth/register` | Inscription 						|
|  POST   | `/api/auth/login`    | Connexion (renvoie token + user) |

---

### Books
| Méthode | Route                         | Sécurité          | Description            |
|---------|-------------------------------|-------------------|------------------------|
| GET     | `/api/books`                  | Public            | Liste complète         |
| GET     | `/api/books/<id>`             | Public            | Détail                 |
| GET     | `/api/books/search?author=X`  | Public            | Recherche              |
| POST    | `/api/books`                  | JWT               | Création               |
| PUT     | `/api/books/<id>`             | JWT               | Mise à jour totale     |
| PATCH   | `/api/books/<id>`             | JWT               | Mise à jour partielle  |
| DELETE  | `/api/books/<id>`             | JWT + rôle admin  | Suppression            |


---

# 4. Blueprints (organisation des routes)

Le routing est séparé en deux fichiers :

```
app/routes/books_routes.py
app/routes/auth_routes.py
```

Puis importés dans :

```
app/routes/routes.py
```

Et le `create_app()` charge :

```python
def create_app():
    app = Flask(__name__)
    CORS(app, ...)
    register_request_logging(app)
    init_routes(app)
    return app
```

---

# 5. Lancer l’app (sans Docker)

## Back-end

```
cd back-end
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Back disponible sur :  
➡️ http://localhost:5000

---

## Front-end

```
cd front-end
npm install
ng serve --open
```

Front disponible sur :  
➡️ http://localhost:4200

---

# 6. Lancer l’app (avec Docker)

Depuis la racine du projet :

```
docker-compose up --build
```

- Back → http://localhost:5000  
- Front → http://localhost:4200  

---

# 7. Tests automatisés

Le back utilise **pytest** avec des fixtures :

```
pytest -v
```

Les tests couvrent :
- GET / POST / PUT / PATCH / DELETE
- protection JWT
- rôle admin pour suppression
- validation via DTO
- recherche par auteur

---

# 8. 🎯 Résumé

Ce projet montre comment :
- structurer une API Flask propre et lisible
- utiliser DTO + services + middlewares
- ajouter un JWT sur un flux de login/register
- sécuriser des routes avec rôles
- connecter Angular avec un back Python
- organiser les routes avec Blueprints
- écrire des tests autour d’une API REST

Il sert de base pédagogique pour pratiquer :
- les différentes couches d’une architecture backend
- la communication front/back moderne
- une authentification simple mais réaliste
