from flask import Flask

def create_app():
    
    app = Flask(__name__)

    # import blueprints
    from . import routes
    app.register_blueprint(routes.bp)
    app.secret_key = 'your_secret_key'

    return app

app = create_app()

if __name__ == "__main__":
    app.run()