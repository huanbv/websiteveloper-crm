import sys
import os
from pathlib import Path


def add_sys_paths():
    print('\n[ADDING PATHS TO THE PYTHON ENVIRONMENT...]')

    # getting the current file's absolute path
    CURRENT_FILE_ABSOLUTE_PATH = Path(__file__).absolute()

    # WORKING_DIR: src
    WORKING_DIR = os.path.abspath(os.path.join(CURRENT_FILE_ABSOLUTE_PATH, '../'))

    # ROOT_DIR (includes the: src ; scripts ; venv ; ..
    ROOT_DIR = os.path.abspath(os.path.join(CURRENT_FILE_ABSOLUTE_PATH, '../../'))

    # appending the WORKING_DIR, ROOT_DIR to the python environment
    sys.path.append(WORKING_DIR)
    sys.path.append(ROOT_DIR)
    print('\n[PATHS IN THE PYTHON ENVIRONMENT...]:')
    print('\n'.join(sys.path), '\n')

    return WORKING_DIR, ROOT_DIR


def create_app():
    # initializing the app
    print("\n[INITIALIZING THE APP...]")
    from src.main import App
    app = App(instance_path=add_sys_paths()[0])

    print("\n[INITIALIZING THE DATABASE...]")
    db.init_app(app=app)


    # migrating Models to DB
    from flask_migrate import Migrate
    print("\n\n[MIGRATING THE DATABASE...]")
    migrate = Migrate()

    with app.app_context():
        # allow dropping column for sqlite
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    # importing models
    import src.main.modules.user.user_model
    # place your new model (want to be created in the app.sqlite) here


    print('\n\n[NEW APP RETURNED...]')
    return app


# defining the db instance
print("\n[DEFINING THE DATABASE INSTANCE...]")
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
