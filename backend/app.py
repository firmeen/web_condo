from flask import Flask, jsonify
from flask_cors import CORS

from config import config
from routes.inquiries import inquiries_bp


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    if config.CORS_ORIGINS == "*":
        CORS(app)
    else:
        CORS(app, resources={r"/api/*": {"origins": [origin.strip() for origin in config.CORS_ORIGINS.split(",")]}})

    app.register_blueprint(inquiries_bp, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"message": "ไม่พบ endpoint ที่ร้องขอ"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"message": "Method ไม่ถูกต้องสำหรับ endpoint นี้"}), 405

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
