from flask import Flask


class App(Flask):
    def __init__(self, instance_path: str):
        super(App, self).__init__(
            import_name=__name__,
            instance_path=instance_path,
            instance_relative_config=True
        )

        # assigning the base templates & static folder
        self.template_folder = './base/templates'
        self.static_folder = './base/static'

        # loading environment variables
        self.load_environment_variables()

        # registering essential partials for the app
        self.register_blueprints()
        self.register_login_manager()


    def register_blueprints(self):
        """
        Registering the app's blueprints.
        """
        from .modules.index import index_module
        from src.main.modules.auth import auth_module
        from src.main.modules.project import project_module
        from src.main.modules.task import task_module
        from src.main.modules.task_checklist_item import task_checklist_item_module
        from src.main.modules.client import client_module
        from src.main.modules.contact import contact_module
        from src.main.modules.currency import currency_module
        from src.main.modules.country import country_module
        from src.main.modules.product import product_module

        self.register_blueprint(index_module, url_prefix="/")
        self.register_blueprint(auth_module, url_prefix="/auth")
        self.register_blueprint(project_module, url_prefix="/project")
        self.register_blueprint(task_module, url_prefix="/task")
        self.register_blueprint(task_checklist_item_module, url_prefix="/task-checklist-item")
        self.register_blueprint(client_module, url_prefix="/client")
        self.register_blueprint(contact_module, url_prefix="/contact")
        self.register_blueprint(currency_module, url_prefix="/currency")
        self.register_blueprint(country_module, url_prefix="/country")
        self.register_blueprint(product_module, url_prefix="/product")



    def register_login_manager(self):
        # adding login manager
        from flask_login import LoginManager

        login_manager = LoginManager()
        login_manager.login_view = "auth.login"
        login_manager.init_app(self)

        @login_manager.user_loader
        def load_user(email):
            # registering user_loader
            from src.main.modules.user import User
            return User.query.get(email)


    def load_environment_variables(self):
        """
        Loading the configured environment variables.
        """
        # Load the default configuration (../config/default.py)
        self.config.from_object('config.default')

        # Load the file specified by the APP_CONFIG_FILE environment variable
        # Variables defined here will override those in the default configuration
        self.config.from_envvar('APP_CONFIG_FILE')

