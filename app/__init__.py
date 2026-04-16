import os
import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from app.routes.ledger_routes import ledger_bp
    from app.routes.tx_routes import tx_bp

    app.register_blueprint(ledger_bp)
    app.register_blueprint(tx_bp)

    return app

def init_db():
    from app import create_app
    app = create_app()
    with app.app_context():
        db = sqlite3.connect(app.config['DATABASE'])
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            db.executescript(f.read())
        db.commit()
    print("Database Initialized Successfully.")
