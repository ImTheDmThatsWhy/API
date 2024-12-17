import os
from flask import Flask
from init import db, ma
from controllers.cli_controller import db_commands
from controllers.addresses_controller import addresses_bp
from controllers.faculties_controller import faculties_bp
from controllers.students_controller import students_bp
from controllers.professors_controller import professors_bp
from controllers.degree_level_controller import degree_levels_bp
from controllers.thesis_controller import thesis_bp


def create_app():
    app = Flask(__name__)
    print("server begins")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(db_commands)
    app.register_blueprint(addresses_bp)
    app.register_blueprint(faculties_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(professors_bp)
    app.register_blueprint(degree_levels_bp)
    app.register_blueprint(thesis_bp)
    return app
