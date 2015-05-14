from flask import Flask, render_template

from stocksplosion.settings import Config
from stocksplosion.assets import assets
from stocksplosion.extensions import (
  debug_toolbar
)
from stocksplosion import public


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    debug_toolbar.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
