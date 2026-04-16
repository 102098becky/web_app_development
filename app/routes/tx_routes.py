from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.ledger import Ledger
import csv
import io
from datetime import datetime

tx_bp = Blueprint('tx_bp', __name__)

@tx_bp.route('/', methods=['GET'])
def dashboard():
    """
    首頁：顯示選定記帳本的餘額、收支統計。
    渲染: dashboard.html
    """
    ledger_id = session.get('current_ledger_id')
    ledgers = Ledger.get_all()

    if not ledgers:
        return redirect(url_for('ledger_bp.new_ledger'))

    if not ledger_id:
        ledger_id = ledgers[0].id
        session['current_ledger_id'] = ledger_id
        
    current_ledger = Ledger.get_by_id(ledger_id)
    if not current_ledger:
        session.pop('current_ledger_id', None)
        return redirect(url_for('tx_bp.dashboard'))

    transactions = Transaction.get_all_by_ledger(ledger_id)
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    categories = Category.get_all()
    cat_dict = {c.id: c.name for c in categories}

    return render_template('dashboard.html', 
                           ledgers=ledgers, 
                           current_ledger=current_ledger,
                           transactions=transactions,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance,
                           cat_dict=cat_dict)

@tx_bp.route('/transactions/new', methods=['GET'])
def new_transaction():
    """顯示新增收支明細表單"""
    ledger_id = session.get('current_ledger_id')
    if not ledger_id:
        flash("請先選擇或建立一個記帳本", "warning")
        return redirect(url_for('tx_bp.dashboard'))
        
    categories = Category.get_all()
    return render_template('transactions/new.html', categories=categories, today=datetime.now().strftime('%Y-%m-%d'))

@tx_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """接收收支明細表單然後存庫"""
    ledger_id = session.get('current_ledger_id')
    if not ledger_id:
        flash("請先選擇或建立一個記帳本", "warning")
        return redirect(url_for('tx_bp.dashboard'))

    tx_type = request.form.get('type')
    category_id = request.form.get('category_id')
    amount = request.form.get('amount')
    date = request.form.get('date')
    description = request.form.get('description', '')

    if not all([tx_type, category_id, amount, date]):
        flash("請填寫所有必填欄位", "danger")
        return redirect(url_for('tx_bp.new_transaction'))

    try:
        amount = float(amount)
        category_id = int(category_id)
    except ValueError:
        flash("金額與分類必須是有效的數字", "danger")
        return redirect(url_for('tx_bp.new_transaction'))

    tx_id = Transaction.create(ledger_id, category_id, tx_type, amount, date, description)
    if tx_id:
        flash("新增收支成功！", "success")
    else:
        flash("新增失敗，請稍後再試。", "danger")
        
    return redirect(url_for('tx_bp.dashboard'))

@tx_bp.route('/transactions/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """顯示特定明細的編輯表單"""
    tx = Transaction.get_by_id(id)
    if not tx:
        flash("找不到指定的收支紀錄", "danger")
        return redirect(url_for('tx_bp.dashboard'))
        
    categories = Category.get_all()
    return render_template('transactions/edit.html', tx=tx, categories=categories)

@tx_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """更新指定的紀錄"""
    tx_type = request.form.get('type')
    category_id = request.form.get('category_id')
    amount = request.form.get('amount')
    date = request.form.get('date')
    description = request.form.get('description', '')

    try:
        amount = float(amount)
        category_id = int(category_id)
    except ValueError:
        flash("金額與分類必須是有效的數字", "danger")
        return redirect(url_for('tx_bp.edit_transaction', id=id))

    success = Transaction.update(id, category_id, tx_type, amount, date, description)
    if success:
        flash("更新紀錄成功！", "success")
    else:
        flash("更新失敗", "danger")
        
    return redirect(url_for('tx_bp.dashboard'))

@tx_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """刪除紀錄"""
    success = Transaction.delete(id)
    if success:
        flash("已刪除紀錄", "success")
    else:
        flash("刪除失敗", "danger")
    return redirect(url_for('tx_bp.dashboard'))

@tx_bp.route('/transactions/export', methods=['GET'])
def export_transactions():
    """匯出成 CSV"""
    ledger_id = session.get('current_ledger_id')
    if not ledger_id:
        flash("請先選擇記帳本", "warning")
        return redirect(url_for('tx_bp.dashboard'))

    ledger = Ledger.get_by_id(ledger_id)
    transactions = Transaction.get_all_by_ledger(ledger_id)
    categories = {c.id: c.name for c in Category.get_all()}

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])

    for tx in transactions:
        c_name = categories.get(tx.category_id, "未知")
        t_type = "收入" if tx.type == 'income' else "支出"
        writer.writerow([tx.date, t_type, c_name, tx.amount, tx.description])

    output.seek(0)
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8-sig')) # BOM for excel
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        download_name=f"{ledger.name}_records.csv",
        as_attachment=True
    )
