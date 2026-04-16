import sqlite3

DATABASE = 'instance/database.db'

def get_db_connection():
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
    def get_all_by_ledger(ledger_id):
        with get_db_connection() as conn:
            rows = conn.execute('SELECT * FROM transactions WHERE ledger_id = ? ORDER BY date DESC, created_at DESC', (ledger_id,)).fetchall()
            return [Transaction(**dict(row)) for row in rows]

    @staticmethod
    def create(ledger_id, category_id, type, amount, date, description):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (ledger_id, category_id, type, amount, date, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ledger_id, category_id, type, amount, date, description))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(tx_id):
        with get_db_connection() as conn:
            row = conn.execute('SELECT * FROM transactions WHERE id = ?', (tx_id,)).fetchone()
            if row:
                return Transaction(**dict(row))
            return None

    @staticmethod
    def update(tx_id, category_id, type, amount, date, description):
        with get_db_connection() as conn:
            conn.execute('''
                UPDATE transactions
                SET category_id = ?, type = ?, amount = ?, date = ?, description = ?
                WHERE id = ?
            ''', (category_id, type, amount, date, description, tx_id))
            conn.commit()

    @staticmethod
    def delete(tx_id):
        with get_db_connection() as conn:
            conn.execute('DELETE FROM transactions WHERE id = ?', (tx_id,))
            conn.commit()
