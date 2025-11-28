# app/controllers/auth_controller.py

from flask import jsonify, request

from app.dtos.auth_dto import LoginDTO, RegisterDTO
from app.services.user_service import (
    create_user,
    verify_credentials,
    get_user_by_email,
)
from app.tools.jwt_utils import create_access_token


def register():
    """
    POST /api/auth/register
    Reçoit les infos d'inscription depuis le front Angular :
      - email
      - password
      - confirmPassword

    Le contrôleur ne fait pas de validation "à la main".
    On délègue tout au DTO (RegisterDTO), qui renvoie soit :
      - un objet valide,
      - soit une erreur prête à être renvoyée au front.
    """

    # On tente de récupérer le JSON envoyé par le front.
    # Si rien n'est envoyé, on utilise un dict vide (évite erreurs None).
    data = request.get_json() or {}

    # Le DTO vérifie le format, la cohérence (password == confirmPassword), etc.
    # Le couple (dto, err) indique si les données sont acceptables.
    dto, err = RegisterDTO.from_json(data)
    if err:
        # Erreur de validation : on renvoie un statut 400 et un message clair.
        return jsonify(err), 400

    # Avant de créer un utilisateur, on s'assure que l'email n'est pas déjà pris.
    existing = get_user_by_email(dto.email)
    if existing:
        return jsonify({"error": "Un utilisateur avec cet email existe déjà."}), 409

    # Tentative de création dans la couche service.
    # En cas de souci (ex : politique mot de passe), create_user peut lever ValueError.
    try:
        user = create_user(email=dto.email, password=dto.password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    # Succès : on renvoie un statut 201 et les infos du nouvel utilisateur.
    return jsonify(
        {
            "message": "Utilisateur créé avec succès.",
            "user": user.to_dict(),  # Format léger prêt à être consommé côté Angular
        }
    ), 201


def login():
    """
    POST /api/auth/login
    Reçoit email + password et tente une authentification simple.

    En cas de succès :
      - Génération d'un JWT (token)
      - Renvoi de l'utilisateur pour stocker les infos dans le front
        (ex : AuthStore Angular)
    """

    # Récupération des données envoyées par Angular (ou dict vide si pas de JSON).
    data = request.get_json() or {}

    # Validation via LoginDTO : structure, champs obligatoires, etc.
    dto, err = LoginDTO.from_json(data)
    if err:
        return jsonify(err), 400

    # Appel au service pour vérifier les identifiants.
    # verify_credentials retourne l'objet User si OK, sinon None.
    user = verify_credentials(dto.email, dto.password)
    if not user:
        # Pour des raisons de sécurité, on reste vague : pas de détail sur ce qui est faux.
        return jsonify({"error": "Identifiants invalides."}), 401

    # Génération d’un token JWT contenant :
    # - l'id
    # - l'email
    # - le role (admin / user)
    #
    # Ce token sera récupéré côté Angular et conservé via le TokenService.
    token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role
    )

    # Réponse standardisée pour faciliter la consommation côté front.
    return jsonify(
        {
            "access_token": token,
            "user": user.to_dict(),
        }
    ), 200
