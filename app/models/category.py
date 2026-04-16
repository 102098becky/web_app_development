import sqlite3

DATABASE = 'instance/database.db'

def get_db_connection():
    """建立並回傳與資料庫的連線"""
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
        """取得所有收支分類記錄"""
        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM categories').fetchall()
                return [Category(**dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            return []

    @staticmethod
    def get_by_type(category_type):
        """根據分類類型取得紀錄
        Args:
            category_type (str): 'income' 或 'expense'
        """
        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM categories WHERE type = ?', (category_type,)).fetchall()
                return [Category(**dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching categories by type: {e}")
            return []

    @staticmethod
    def get_by_id(category_id):
        """根據 ID 取得單筆分類記錄"""
        try:
            with get_db_connection() as conn:
                row = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
                if row:
                    return Category(**dict(row))
                return None
        except sqlite3.Error as e:
            print(f"Error fetching category by id: {e}")
            return None

    @staticmethod
    def create(name, type, is_default=False):
        """新增一筆分類記錄"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO categories (name, type, is_default) VALUES (?, ?, ?)', (name, type, is_default))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating category: {e}")
            return None

    @staticmethod
    def update(category_id, name, type):
        """更新一筆分類記錄"""
        try:
            with get_db_connection() as conn:
                conn.execute('UPDATE categories SET name = ?, type = ? WHERE id = ?', (name, type, category_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating category: {e}")
            return False

    @staticmethod
    def delete(category_id):
        """刪除一筆分類記錄"""
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting category: {e}")
            return False
