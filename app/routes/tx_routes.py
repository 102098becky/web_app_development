from flask import Blueprint, render_template, request, redirect, url_for, session

tx_bp = Blueprint('tx_bp', __name__)

@tx_bp.route('/', methods=['GET'])
def dashboard():
    """
    首頁：顯示選定記帳本的餘額、收支統計。
    渲染: dashboard.html
    """
    pass

@tx_bp.route('/transactions/new', methods=['GET'])
def new_transaction():
    """
    顯示新增收支明細表單。
    會讀出所有的分類 (`Category.get_all()`) 以呈現下拉選單。
    渲染: transactions/new.html
    """
    pass

@tx_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """
    接收收支明細表單，存放至資料庫並重導向回首頁。
    需要對應到 session 的 current_ledger_id。
    """
    pass

@tx_bp.route('/transactions/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    顯示特定明細的編輯表單，帶著原先紀錄呈現於畫面。
    渲染: transactions/edit.html
    """
    pass

@tx_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """
    接收到編輯完畢的表單內容，更新指定的紀錄，回首頁。
    """
    pass

@tx_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    刪除特定紀錄項目，回首頁。
    """
    pass

@tx_bp.route('/transactions/export', methods=['GET'])
def export_transactions():
    """
    將目前記帳本的所有紀錄匯出為 CSV 功能，使用者點擊後會觸發檔案下載。
    """
    pass
