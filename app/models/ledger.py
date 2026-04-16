import sqlite3

DATABASE = 'instance/database.db'

def get_db_connection():
    """建立並回傳與資料庫的連線"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class Ledger:
    def __init__(self, id, name, created_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at

    @staticmethod
    def get_all():
        """取得所有的記帳本記錄"""
        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM ledgers ORDER BY created_at DESC').fetchall()
                return [Ledger(**dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching ledgers: {e}")
            return []

    @staticmethod
    def get_by_id(ledger_id):
        """根據 ID 取得單筆記帳本記錄"""
        try:
            with get_db_connection() as conn:
                row = conn.execute('SELECT * FROM ledgers WHERE id = ?', (ledger_id,)).fetchone()
                if row:
                    return Ledger(**dict(row))
                return None
        except sqlite3.Error as e:
            print(f"Error fetching ledger by id: {e}")
            return None

    @staticmethod
    def create(name):
        """新增一筆記帳本記錄
        Args:
            name (str): 記帳本名稱
        Returns:
            int: 新增的紀錄 ID，如果失敗則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO ledgers (name) VALUES (?)', (name,))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating ledger: {e}")
            return None

    @staticmethod
    def update(ledger_id, name):
        """更新一筆記帳本記錄
        Args:
            ledger_id (int): 要更新的記帳本 ID
            name (str): 記帳本新名稱
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            with get_db_connection() as conn:
                conn.execute('UPDATE ledgers SET name = ? WHERE id = ?', (name, ledger_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating ledger: {e}")
            return False

    @staticmethod
    def delete(ledger_id):
        """刪除一筆記帳本記錄
        Args:
            ledger_id (int): 要刪除的記帳本 ID
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM ledgers WHERE id = ?', (ledger_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting ledger: {e}")
            return False
