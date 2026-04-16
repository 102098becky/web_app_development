import sqlite3

DATABASE = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class Category:
    def __init__(self, id, name, type, is_default):
        self.id = id
        self.name = name
        self.type = type
        self.is_default = is_default

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            rows = conn.execute('SELECT * FROM categories').fetchall()
            return [Category(**dict(row)) for row in rows]

    @staticmethod
    def get_by_type(category_type):
        with get_db_connection() as conn:
            rows = conn.execute('SELECT * FROM categories WHERE type = ?', (category_type,)).fetchall()
            return [Category(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(category_id):
        with get_db_connection() as conn:
            row = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
            if row:
                return Category(**dict(row))
            return None

    @staticmethod
    def create(name, type, is_default=False):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO categories (name, type, is_default) VALUES (?, ?, ?)', (name, type, is_default))
            conn.commit()
            return cursor.lastrowid
