from flask import Blueprint, render_template, request, redirect, url_for, session

ledger_bp = Blueprint('ledger_bp', __name__)

@ledger_bp.route('/ledgers/new', methods=['GET'])
def new_ledger():
    """
    顯示新增記帳本的表單頁面。
    渲染: ledgers/new.html
    """
    pass

@ledger_bp.route('/ledgers', methods=['POST'])
def create_ledger():
    """
    接收新增表單，存入資料庫，然後回到首頁。
    輸入: 表單欄位 `name`
    """
    pass

@ledger_bp.route('/ledgers/<int:id>/switch', methods=['POST'])
def switch_ledger(id):
    """
    將選定的記帳本寫入 Session，方便首頁直接存取。
    然後導回首頁。
    """
    pass

@ledger_bp.route('/ledgers/<int:id>/delete', methods=['POST'])
def delete_ledger(id):
    """
    刪除記帳本與裡面所有的明細，回首頁。
    """
    pass
