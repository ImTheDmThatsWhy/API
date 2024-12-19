import os
from flask import Flask
from init import db, ma
from controllers.cli_controller import db_commands
from controllers.addresses_controller import addresses_bp
from controllers.faculties_controller import faculties_bp
from controllers.students_controller import students_bp
from controllers.supervisors_controller import supervisors_bp
from controllers.status_controller import status_bp
from controllers.phd_thesis_controller import thesis_bp
from controllers.student_supervisors_controllers import student_supervisors_bp


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
    app.register_blueprint(supervisors_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(thesis_bp)
    app.register_blueprint(student_supervisors_bp)
    return app
