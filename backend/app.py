from flask import Flask
import os
from dotenv import load_dotenv
from routes import get_info_api, checkout_api, close_store_api
from flask_cors import CORS
from db import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(get_info_api.routes)
    app.register_blueprint(checkout_api.routes)
    app.register_blueprint(close_store_api.routes)

    with app.app_context():
        db.create_all()
    return app




if __name__ == "__main__":
    app = create_app()
    @app.route("/")
    def home():
        return "This is steve's api"
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)), threaded=True, debug=True)