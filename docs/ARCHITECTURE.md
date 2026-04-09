# 系統架構設計 (System Architecture) - 個人記帳簿系統

本文件根據 PRD 需求，規劃了專案的技術架構、資料夾結構與元件職責，作為開發時的指引藍圖。

## 1. 技術架構說明

為了達到輕量、開發快速且滿足主要使用者需求，本系統不採用前後端分離，而是透過後端直接渲染頁面。

### 選用技術與原因
- **後端：Python + Flask**
  - **原因**：Flask 是輕巧的 Python 網站框架，非常適合中小型專案以及快速打造 MVP（ Minimum Viable Product）。學習曲線平緩，佈署也很方便。
- **模板引擎：Jinja2**
  - **原因**：Flask 內建的模板引擎，負責將後端的資料動態渲染成 HTML 頁面並傳給瀏覽器。相較於 React 或 Vue 等前端框架，搭配 Jinja2 不需要處理複雜的 API 與狀態管理。
- **資料庫：SQLite (搭配 SQLAlchemy 或 sqlite3)**
  - **原因**：不需要額外安裝或架設資料庫伺服器，所有資料皆儲層於專案目錄下的單一檔案中，適合供個人使用的記帳系統。

### Flask MVC 模式說明
雖然 Flask 本身是微框架（Microframework），但我們會依循類似 MVC（Model-View-Controller）的架構來分隔職責，以保持原始碼的乾淨：
- **Model (資料庫模型)**：負責定義資料長什麼樣子（如收支紀錄表、記帳本表）、與資料庫進行溝通。
- **View (HTML 模板)**：位於 `templates/` 資料夾，以 Jinja2 語法撰寫，負責最終畫面呈現給使用者的結構與樣式。
- **Controller (Flask 路由)**：位於 `routes/` 資料夾中，負責接收使用者的 HTTP 請求、從 Model 提取資料，並將資料丟給 View 渲染成 HTML。

---

## 2. 專案資料夾結構

為確保專案程式碼便於維護與擴充，我們規劃了如下的專案樹狀結構：

```text
personal_expense_tracker/
│
├── app/                      # 應用系統核心目錄
│   ├── __init__.py           # 初始化 Flask 應用與相關套件
│   ├── models/               # 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── ledger.py         # 記帳本模型
│   │   ├── transaction.py    # 收支紀錄模型
│   │   └── category.py       # 收支分類模型
│   │
│   ├── routes/               # Flask 路由控制器 (Controller)
│   │   ├── __init__.py
│   │   ├── ledger_routes.py  # 處理記帳本相關的請求
│   │   └── tx_routes.py      # 處理收支紀錄、導出的請求
│   │
│   ├── templates/            # Jinja2 HTML 模板 (View)
│   │   ├── base.html         # 母版 (包含共用 Header/Footer)
│   │   ├── dashboard.html    # 首頁／儀表板 (顯示餘額統計)
│   │   └── form.html         # 新增/編輯收支紀錄表單
│   │
│   └── static/               # 靜態資源檔案
│       ├── css/
│       │   └── style.css     # 自訂樣式表
│       └── js/
│           └── main.js       # 表單驗證或簡單的前端互動指令碼
│
├── instance/                 # 放置不需加入 Git 的運行期檔案
│   └── database.db           # SQLite 本地資料庫檔案
│
├── docs/                     # 專案說明文件目錄
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 系統架構設計文件 (本文件)
│
├── app.py                    # 專案的啟動入口腳本
└── requirements.txt          # 記錄專案所有依賴的 Python 套件
```

---

## 3. 元件關係圖

以下展示使用者如何透過瀏覽器與本系統的各個元件互動：

```mermaid
flowchart TD
    Browser[瀏覽器 (Browser)]
    
    subgraph Flask App
        Route[Flask Route (Controller)]
        Model[Database Model]
        Template[Jinja2 Template (View)]
    end
    
    DB[(SQLite 資料庫)]
    Static[Static 資源 (CSS/JS)]

    %% 互動流程
    Browser -- "1. 發送 HTTP 請求 (例如：新增支出)" --> Route
    Route -- "2. 讀寫資料" --> Model
    Model -- "3. 執行 SQL 語法" --> DB
    DB -- "4. 回傳資料" --> Model
    Model -- "5. 將資料變成 Python 物件" --> Route
    Route -- "6. 將資料注入模板" --> Template
    Template -- "7. 產生最終 HTML" --> Route
    Route -- "8. 回傳 HTTP 回應 (HTML)" --> Browser
    Browser -- "9. 請求靜態檔案" --> Static
    Static -- "10. 回傳 CSS / JS" --> Browser
```

---

## 4. 關鍵設計決策

1. **依功能拆分路由與模型 (Modular Design)**
   - **決策**：將 `routes` 分為 `ledger_routes` 與 `tx_routes`，將 `models` 依照物件狀態獨立出來。
   - **原因**：雖然記帳本 MVP 規模不大，但未來可能增加設定頁面、使用者驗證等功能。提前將資料夾結構模組化，避免日後所有邏輯全擠在 `app.py` 中。

2. **採用 Jinja2 模板繼承 (`base.html`)**
   - **決策**：在 `templates/` 中建立一個全域共用的 `base.html`，其它頁面皆繼承此檔案。
   - **原因**：為了讓應用程式維持一致的版面配置（如標題列導覽網址、頁尾版權聲明），並降低重複的 HTML 程式碼，未來若需要新增版面功能（如側邊欄）也只要修改母版即可套用至全站。

3. **從輕量方案入門資料庫 (`instance/database.db`)**
   - **決策**：不架設 MySQL/PostgreSQL，直接使用放置在 `instance/` 資料夾下的 SQLite。
   - **原因**：符合 PRD 中的非功能需求與 MVP 快速開發策略；將 `.db` 檔放在預設忽略的 `instance/` 資料夾，可避免將敏感或開發用資料不小心推送到 Git 環境。
