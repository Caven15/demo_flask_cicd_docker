# -----------------------------
# STAGE 1 : Build Angular
# -----------------------------
# Image légère Node pour builder le front
FROM node:22-alpine AS build

# Dossier de travail dans le conteneur
WORKDIR /app

# 1) Copier uniquement les fichiers de dépendances
#    => permet de profiter du cache Docker si package.json ne change pas
COPY package*.json ./

RUN npm install

# 2) Copier le reste du projet front
COPY . .

# 3) Build Angular en mode prod
#    Vérifier le nom du projet dans angular.json si besoin.
#    Avec Angular récent, le build sort souvent dans :
#    dist/<nom-projet>/browser
RUN npm run build -- --configuration=production

# -----------------------------
# STAGE 2 : Nginx pour servir le front
# -----------------------------
FROM nginx:1.27-alpine

# On copie le build Angular dans le dossier servi par Nginx
COPY --from=build /app/dist/demoAngularCiCd/browser /usr/share/nginx/html



# Nginx écoute sur le port 80 dans le conteneur
EXPOSE 80

# Commande de démarrage Nginx en foreground
CMD ["nginx", "-g", "daemon off;"]
