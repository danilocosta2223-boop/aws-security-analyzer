from app import app

# Necessário caso o Render procure por application ou app
application = app

if __name__ == "__main__":
    app.run()