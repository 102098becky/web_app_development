# 路由設計與頁面規劃 (Routes & Templates)

本文件根據 PRD、架構與資料庫設計，規劃了系統的 Flask 路由以及需要實作的 Jinja2 HTML 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁與儀表板** | GET | `/` | `dashboard.html` | 顯示當前選定記帳本的餘額、收支統計及近期的收支列表 |
| **新增記帳本** | GET | `/ledgers/new` | `ledgers/new.html` | 顯示新增記帳本表單 |
| **建立記帳本** | POST | `/ledgers` | — | 接收新增表單，存入 DB，儲存後重導向回首頁 |
| **切換記帳本** | POST | `/ledgers/<int:id>/switch` | — | 將選定的記帳本設定到 Session 中 |
| **刪除記帳本** | POST | `/ledgers/<int:id>/delete` | — | 刪除記帳本以及其擁有的明細，之後重導向回首頁 |
| **新增收支明細** | GET | `/transactions/new` | `transactions/new.html` | 顯示新增收支明細表單（需先選擇所在記帳本） |
| **建立收支明細** | POST | `/transactions` | — | 接收填妥的紀錄並寫入資料庫，成功後重導向回首頁 |
| **編輯明細頁面** | GET | `/transactions/<int:id>/edit` | `transactions/edit.html`| 顯示單項收支編輯表單 |
| **更新明細** | POST | `/transactions/<int:id>/update` | — | 更新特定的紀錄 |
| **刪除明細** | POST | `/transactions/<int:id>/delete` | — | 刪除該筆帳款紀錄並重導向回首頁 |
| **匯出 CSV 紀錄**| GET | `/transactions/export` | — | 將目前記帳本的所有紀錄匯出為 CSV 供使用者下載 |

## 2. 每個路由的詳細說明

### `ledger_bp` (記帳本路由)
- **`GET /ledgers/new`**
    - 輸入：無
    - 處理：無特別邏輯
    - 輸出：渲染 `ledgers/new.html`
- **`POST /ledgers`**
    - 輸入：表單欄位 `name`
    - 處理：呼叫 `Ledger.create(name)`
    - 輸出：重導向至 `/`
- **`POST /ledgers/<id>/switch`**
    - 輸入：URL 參數 `id`
    - 處理：確認記帳本存在，並寫入到 session 變數中
    - 輸出：重導向至 `/`
- **`POST /ledgers/<id>/delete`**
    - 輸入：URL 參數 `id`
    - 處理：呼叫 `Ledger.delete(id)` 等等相關聯的防呆機制
    - 輸出：重導向至 `/`

### `tx_bp` (明細路由)
- **`GET /` 或者 `GET /dashboard`**
    - 輸入：無特別輸入（會由 Session 讀取目前所選的 `ledger_id`）
    - 處理：呼叫 `Transaction.get_all_by_ledger(ledger_id)` 與各項分類統計計算
    - 輸出：渲染 `dashboard.html` 將明細與統計圖表顯示出來
- **`GET /transactions/new`**
    - 輸入：無
    - 處理：根據 Session 把目前的 `ledger_id` 抓出，以及撈取所有分類 `Category.get_all()` 給表單產出下拉選項
    - 輸出：渲染 `transactions/new.html`
- **`POST /transactions`**
    - 輸入：表單欄位 `category_id`, `type`, `amount`, `date`, `description`, Session 中的 `ledger_id`
    - 處理：根據輸入呼叫 `Transaction.create(...)`
    - 輸出：重導向 `/` 顯示最新成果
- **`GET /transactions/<id>/edit`**
    - 輸入：URL 參數 `id`
    - 處理：呼叫 `Transaction.get_by_id(id)`、`Category.get_all()` 用於填充編輯表單
    - 輸出：渲染 `transactions/edit.html`
- **`POST /transactions/<id>/update`**
    - 輸入：包含更新內容的表單欄位以及欲更改的記錄 `id`
    - 處理：呼叫 `Transaction.update(...)`
    - 輸出：修改完成並重導向 `/`
- **`POST /transactions/<id>/delete`**
    - 輸入：欲刪除的紀錄 `id`
    - 處理：呼叫 `Transaction.delete(id)`
    - 輸出：重導向 `/`
- **`GET /transactions/export`**
    - 輸入：Session 內的 `ledger_id`
    - 處理：讀取名單將所有列由 CSV 結構打包
    - 輸出：利用 Flask `send_file` 或 Response 直接彈出下載任務

## 3. Jinja2 模板清單

所有的模板將放置在 `app/templates/` 中。我們會建立一個基礎的 `base.html`，讓其他檔案繼承包覆。

- `base.html`：包含系統的最外圍版型（Nav bar、Header、Footer）與共用的 CSS/JS 引入。
- `dashboard.html`：**繼承 base.html**，放入統整資訊的核心畫面。
- `ledgers/new.html`：**繼承 base.html**，一個簡單的單列的表單畫面。
- `transactions/new.html`：**繼承 base.html**，針對每個款項屬性填寫的表單（附帶分類與日期選擇）。
- `transactions/edit.html`：**繼承 base.html**，重新帶入現有資訊的表單介面。
