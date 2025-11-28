# Utilise une image Python légère basée sur Debian.
# "slim" permet de réduire la taille du conteneur, tout en gardant l'essentiel.
FROM python:3.12-slim

# On définit le répertoire de travail à l’intérieur du conteneur.
# Toutes les commandes suivantes seront exécutées depuis /app.
WORKDIR /app

# On copie uniquement requirements.txt dans un premier temps.
# Ce pattern permet de mettre en cache l'installation des dépendances
# tant que requirements.txt ne change pas.
COPY requirements.txt .

# Installation des dépendances du projet.
# --no-cache-dir évite que pip garde des fichiers inutiles → image plus légère.
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du projet (ton code Flask, modules, config…)
COPY . .

# Le conteneur expose le port 5000.
# C’est le port utilisé par le serveur Flask dans app.py.
EXPOSE 5000

# Commande exécutée au démarrage du conteneur.
# On lance simplement le back Flask via app.py.
CMD ["python", "app.py"]
