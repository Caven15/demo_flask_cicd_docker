# app/middlewares/request_logging.py

import time
from flask import Flask, request, g


def register_request_logging(app: Flask) -> None:
    """
    Active deux hooks Flask qui tournent autour de chaque requête.
    L’idée générale : mesurer combien de temps une requête met
    et garder une petite trace dans les logs du serveur.
    """

    @app.before_request
    def start_timer():
        """
        Fonction exécutée AVANT que la route ne démarre réellement.
        On note juste l’heure actuelle pour pouvoir calculer la durée après.
        On utilise 'g' parce que c’est un espace de stockage propre à une seule requête.
        """
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        """
        Fonction exécutée APRÈS l’exécution de la route.
        On récupère l’heure de départ, on calcule la différence,
        et on envoie une ligne dans les logs.
        
        Ce n’est pas pour le front : c’est vraiment pour le dev,
        pour voir ce qui se passe en coulisses et combien de temps les endpoints prennent.
        """

        # Si jamais start_time n'a pas été mis (edge case rare), on évite un crash
        duration_ms = -1
        if hasattr(g, "start_time"):
            duration_ms = (time.time() - g.start_time) * 1000

        method = request.method
        path = request.path
        status_code = response.status_code

        # Petite ligne sympa dans les logs, du genre :
        # [REQUEST] GET /api/books -> 200 (5.32 ms)
        app.logger.info(
            f"[REQUEST] {method} {path} -> {status_code} ({duration_ms:.2f} ms)"
        )

        # after_request doit toujours renvoyer la réponse finale
        return response
