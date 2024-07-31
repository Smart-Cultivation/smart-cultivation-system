import os
from flask import Flask
from config import CONFIG

from index import bp as index_bp
from errors import bp as error_bp
from smart_cultivation_system import bp as scs_bp
from receive_data import bp as rd_bp
from insert_pond import bp as db_bp
from predict import bp as predict_bp
from login import bp as login_bp
from register import bp as register_bp
from logout import bp as logout_bp

from cache import init_cache_app
from compress import init_compress_app
from rate_limiter import init_rate_limiter
from database.mysql import init_db, init_db_command, drop_db_command, populate_db_command

from flask_login import LoginManager
from database.model.user import User

app = Flask(__name__)
app.config.update(CONFIG)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Register Blueprints
app.register_blueprint(index_bp)
app.register_blueprint(error_bp)
app.register_blueprint(scs_bp)
app.register_blueprint(rd_bp)
app.register_blueprint(db_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(logout_bp)

# Initializing
init_cache_app(app)
init_compress_app(app)
init_rate_limiter(app)
init_db(app)

# CLI Commands
app.cli.add_command(init_db_command)
app.cli.add_command(drop_db_command)
app.cli.add_command(populate_db_command)

if __name__ == "__main__":
    app.run(
        debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
    )
