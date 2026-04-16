from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.ledger import Ledger

ledger_bp = Blueprint('ledger_bp', __name__)

@ledger_bp.route('/ledgers/new', methods=['GET'])
def new_ledger():
    """
    顯示新增記帳本的表單頁面。
    渲染: ledgers/new.html
    """
    return render_template('ledgers/new.html')

@ledger_bp.route('/ledgers', methods=['POST'])
def create_ledger():
    """
    接收新增表單，存入資料庫，然後回到首頁。
    輸入: 表單欄位 `name`
    """
    name = request.form.get('name', '').strip()
    
    # 基本輸入驗證
    if not name:
        flash("記帳本名稱為必填項目", "danger")
        return render_template('ledgers/new.html')

    # 實作: 呼叫 Model 建立紀錄
    ledger_id = Ledger.create(name)
    if ledger_id:
        flash(f"已成功建立記帳本「{name}」！", "success")
        # 為了使用者體驗，建立完成後可直接切換到該帳本
        session['current_ledger_id'] = ledger_id
        return redirect(url_for('tx_bp.dashboard'))
    else:
        flash("建立記帳本發生錯誤，請稍後再試。", "danger")
        return render_template('ledgers/new.html')

@ledger_bp.route('/ledgers/<int:id>/switch', methods=['POST'])
def switch_ledger(id):
    """
    將選定的記帳本寫入 Session，方便首頁直接存取。
    然後導回首頁。
    """
    ledger = Ledger.get_by_id(id)
    if ledger:
        session['current_ledger_id'] = ledger.id
        flash(f"已切換至記帳本「{ledger.name}」", "success")
    else:
        flash("找不到指定的記帳本", "danger")
        
    return redirect(url_for('tx_bp.dashboard'))

@ledger_bp.route('/ledgers/<int:id>/delete', methods=['POST'])
def delete_ledger(id):
    """
    刪除記帳本與裡面所有的明細，回首頁。
    """
    ledger = Ledger.get_by_id(id)
    if not ledger:
        flash("找不到指定的記帳本", "danger")
        return redirect(url_for('tx_bp.dashboard'))

    success = Ledger.delete(id)
    if success:
        flash(f"已刪除記帳本「{ledger.name}」", "success")
        # 如果刪除的剛好是目前正在查看的記帳本，則清空 session 紀錄
        if session.get('current_ledger_id') == id:
            session.pop('current_ledger_id', None)
    else:
        flash("刪除記帳本失敗", "danger")
        
    return redirect(url_for('tx_bp.dashboard'))
