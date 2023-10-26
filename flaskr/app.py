import os
from flask import Flask

def create_app():
    
    app = Flask(__name__)

    # import blueprints
    from . import routes
    app.register_blueprint(routes.bp)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    #import database
    from . import db
    db.init_app(app)

    return app

