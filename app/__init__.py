import os
import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
            
        cur = db.execute("SELECT count(*) FROM categories")
        if cur.fetchone()[0] == 0:
            db.executescript("""
                INSERT INTO categories (name, type, is_default) VALUES ('餐飲', 'expense', 1);
                INSERT INTO categories (name, type, is_default) VALUES ('交通', 'expense', 1);
                INSERT INTO categories (name, type, is_default) VALUES ('購物', 'expense', 1);
                INSERT INTO categories (name, type, is_default) VALUES ('娛樂', 'expense', 1);
                INSERT INTO categories (name, type, is_default) VALUES ('水電網路', 'expense', 1);
                INSERT INTO categories (name, type, is_default) VALUES ('薪資', 'income', 1);
                INSERT INTO categories (name, type, is_default) VALUES ('獎金', 'income', 1);
                INSERT INTO categories (name, type, is_default) VALUES ('投資', 'income', 1);
            """)
        db.commit()
    print("Database Initialized Successfully with categories.")
