# 🤖 SmartDecision AI Agent

基於 Python + Streamlit + OpenAI 的互動式 AI 問答助理系統。

---

## 📁 專案結構

```
SmartDecisionSystem/
├── app.py                # Streamlit 應用程式入口
├── agent/
│   ├── __init__.py       # 套件初始化，匯出 AIAgent
│   ├── agent.py          # AIAgent 核心類別
│   ├── config.py         # 環境變數設定管理
│   └── memory.py         # 對話記憶體管理
├── utils/
│   ├── __init__.py       # 套件初始化
│   └── helpers.py        # 共用輔助函式
├── .env.example          # 環境變數範本
├── requirements.txt      # Python 依賴套件清單
└── README.md             # 本說明文件
```

---

## ✨ 功能特色

- 🗨️ 互動式聊天介面（Streamlit Web UI）
- 🧠 保留本次 session 的完整對話紀錄
- 📋 側邊欄顯示聊天歷史摘要
- 🗑️ 一鍵清除對話
- ⚠️ 完整錯誤處理（API Key 未設定、空白輸入、模型呼叫失敗）
- 🔧 模組化設計，預留 Tools、Memory、Multi-Agent 擴充空間

---

## 🚀 安裝與啟動

### 1. 安裝 Python

確認已安裝 **Python 3.10+**：

```bash
python --version
```

### 2. 建立虛擬環境（建議）

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 4. 設定環境變數

複製範本並填入您的 OpenAI API 金鑰：

```bash
cp .env.example .env
```

編輯 `.env` 檔案：

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=1024
TEMPERATURE=0.7
```

> 💡 API 金鑰請至 [OpenAI Platform](https://platform.openai.com/api-keys) 申請。

### 5. 啟動應用程式

```bash
streamlit run app.py
```

瀏覽器將自動開啟 `http://localhost:8501`。

---

## 🖥️ 使用說明

1. 在主頁面下方的輸入框中輸入您的問題
2. 點擊「送出 ✈️」按鈕送出問題
3. AI 回應將顯示在對話區域中
4. 左側邊欄可查看本次對話的歷史摘要
5. 點擊側邊欄的「🗑️ 清除對話」按鈕可重置對話

---

## 🔧 CLI 測試模式

也可以透過命令列直接測試 Agent：

```bash
python agent/agent.py
```

---

## 🛠️ 技術架構

| 元件 | 說明 |
|------|------|
| **Streamlit** | Web UI 框架，快速建立互動介面 |
| **OpenAI API** | GPT 語言模型，負責生成回應 |
| **python-dotenv** | 環境變數管理，安全儲存 API 金鑰 |

---

## 📦 擴充指南

### 新增工具（Tool Use）

在 `agent/agent.py` 的 `_build_tools()` 方法中定義 OpenAI Function Calling 工具：

```python
def _build_tools(self) -> list:
    return [
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "搜尋網路上的最新資訊",
                "parameters": {...}
            }
        }
    ]
```

### 升級記憶體

替換 `agent/memory.py` 中的 `ConversationMemory` 類別，例如加入：
- 摘要壓縮（Summarization）
- 持久化儲存（SQLite / Redis）
- 滑動視窗限制長度

### 多代理系統（Multi-Agent）

在 `agent/agent.py` 的 `run()` 方法中呼叫多個 `AIAgent` 實例協作，
例如路由代理、專業領域代理等。

---

## 📄 授權

MIT License