import os
from flask import Flask
from init import db, ma
from controllers.cli_controller import db_commands
from controllers.addresses_controller import addresses_bp

def create_app():
    app= Flask(__name__)
    print("server begins")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(db_commands)
    app.register_blueprint(addresses_bp)
    return app