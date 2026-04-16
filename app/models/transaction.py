import sqlite3

DATABASE = 'instance/database.db'

def get_db_connection():
    """建立並回傳與資料庫的連線"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class Transaction:
    def __init__(self, id, ledger_id, category_id, type, amount, date, description, created_at=None):
        self.id = id
        self.ledger_id = ledger_id
        self.category_id = category_id
        self.type = type
        self.amount = amount
        self.date = date
        self.description = description
        self.created_at = created_at

    @staticmethod
    def get_all():
        """取得所有記錄"""
        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM transactions ORDER BY date DESC, created_at DESC').fetchall()
                return [Transaction(**dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all transactions: {e}")
            return []

    @staticmethod
    def get_all_by_ledger(ledger_id):
        """取得特定記帳本的所有收支紀錄"""
        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM transactions WHERE ledger_id = ? ORDER BY date DESC, created_at DESC', (ledger_id,)).fetchall()
                return [Transaction(**dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching transactions for ledger: {e}")
            return []

    @staticmethod
    def get_by_id(tx_id):
        """根據 ID 取得單筆收支明細"""
        try:
            with get_db_connection() as conn:
                row = conn.execute('SELECT * FROM transactions WHERE id = ?', (tx_id,)).fetchone()
                if row:
                    return Transaction(**dict(row))
                return None
        except sqlite3.Error as e:
            print(f"Error fetching transaction by id: {e}")
            return None

    @staticmethod
    def create(ledger_id, category_id, type, amount, date, description):
        """新增一筆收支明細"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (ledger_id, category_id, type, amount, date, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (ledger_id, category_id, type, amount, date, description))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating transaction: {e}")
            return None

    @staticmethod
    def update(tx_id, category_id, type, amount, date, description):
        """更新一筆收支明細
        Args:
            tx_id (int): 欲更新的收支紀錄 ID
            category_id (int): 新的分類 ID
            type (str): 'income' 或 'expense'
            amount (float): 金額
            date (str): 收支日期 YYYY-MM-DD
            description (str): 備註
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            with get_db_connection() as conn:
                conn.execute('''
                    UPDATE transactions
                    SET category_id = ?, type = ?, amount = ?, date = ?, description = ?
                    WHERE id = ?
                ''', (category_id, type, amount, date, description, tx_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating transaction: {e}")
            return False

    @staticmethod
    def delete(tx_id):
        """刪除一筆收支明細
        Args:
            tx_id (int): 紀錄 ID
        Returns:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM transactions WHERE id = ?', (tx_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting transaction: {e}")
            return False
