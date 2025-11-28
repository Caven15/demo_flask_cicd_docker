from app import create_app

app = create_app()

if __name__ == "__main__":
    # Exposer l'app sur 0.0.0.0 pour que Docker puisse y accéder
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
