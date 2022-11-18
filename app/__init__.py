from flask import Flask


def init_app():
    app = Flask(__name__)
    from .controller.controller import my_controller
    app.register_blueprint(my_controller, url_prefix='/')
    return app
