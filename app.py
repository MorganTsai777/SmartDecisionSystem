"""
app.py
Streamlit 應用程式入口。

啟動方式：
    streamlit run app.py
"""

import streamlit as st

from agent import AIAgent
from agent.config import config
from utils.helpers import format_timestamp, truncate_text

# -----------------------------------------------------------------------
# 頁面基本設定
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="SmartDecision AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------
# 自訂 CSS（簡潔現代風格）
# -----------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* 主要內容區域 */
        .main .block-container {
            max-width: 860px;
            padding-top: 2rem;
        }

        /* 使用者訊息泡泡 */
        .user-bubble {
            background: #DCF8C6;
            border-radius: 12px 12px 0 12px;
            padding: 0.6rem 1rem;
            margin: 0.4rem 0;
            max-width: 80%;
            margin-left: auto;
            color: #1a1a1a;
            font-size: 0.95rem;
        }

        /* AI 訊息泡泡 */
        .ai-bubble {
            background: #F0F0F0;
            border-radius: 12px 12px 12px 0;
            padding: 0.6rem 1rem;
            margin: 0.4rem 0;
            max-width: 80%;
            color: #1a1a1a;
            font-size: 0.95rem;
        }

        /* 時間戳 */
        .msg-time {
            font-size: 0.72rem;
            color: #888;
            margin-bottom: 0.15rem;
        }

        /* 側邊欄歷史項目 */
        .history-item {
            font-size: 0.82rem;
            color: #444;
            padding: 0.25rem 0;
            border-bottom: 1px solid #eee;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------
# Session State 初始化
# -----------------------------------------------------------------------
def init_session() -> None:
    """初始化 Streamlit session state"""
    if "agent" not in st.session_state:
        st.session_state.agent = None  # AIAgent 實例
    if "chat_history" not in st.session_state:
        # 每筆記錄格式：{"role": "user"|"assistant", "content": str, "time": str}
        st.session_state.chat_history = []
    if "error_msg" not in st.session_state:
        st.session_state.error_msg = ""


def get_agent() -> AIAgent | None:
    """
    取得或建立 AIAgent 實例。

    Returns:
        AIAgent 實例；若 API 金鑰未設定則回傳 None 並顯示錯誤。
    """
    if st.session_state.agent is None:
        try:
            st.session_state.agent = AIAgent()
            st.session_state.error_msg = ""
        except ValueError as e:
            st.session_state.error_msg = str(e)
            return None
    return st.session_state.agent


# -----------------------------------------------------------------------
# 側邊欄
# -----------------------------------------------------------------------
def render_sidebar() -> None:
    """渲染側邊欄：顯示聊天歷史與操作按鈕"""
    with st.sidebar:
        st.title("🗂️ 對話紀錄")
        st.caption(f"模型：`{config.MODEL_NAME}`")
        st.divider()

        # 清除對話按鈕
        if st.button("🗑️ 清除對話", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            if st.session_state.agent:
                st.session_state.agent.reset()
            st.rerun()

        st.divider()

        # 顯示歷史訊息摘要
        history = st.session_state.chat_history
        if not history:
            st.info("目前無對話紀錄。")
        else:
            # 只顯示使用者訊息作為歷史摘要
            user_msgs = [m for m in history if m["role"] == "user"]
            for i, msg in enumerate(reversed(user_msgs), start=1):
                preview = truncate_text(msg["content"], max_length=45)
                st.markdown(
                    f'<div class="history-item">#{len(user_msgs) - i + 1} {preview}</div>',
                    unsafe_allow_html=True,
                )


# -----------------------------------------------------------------------
# 主內容區
# -----------------------------------------------------------------------
def render_chat() -> None:
    """渲染主聊天區域"""
    st.title("🤖 SmartDecision AI Agent")
    st.caption("由 OpenAI 驅動的智慧問答助理")
    st.divider()

    # 顯示錯誤訊息（例如 API Key 未設定）
    if st.session_state.error_msg:
        st.error(st.session_state.error_msg)

    # 顯示對話歷史
    chat_container = st.container()
    with chat_container:
        history = st.session_state.chat_history
        if not history:
            st.markdown(
                "<p style='color:#aaa; text-align:center; margin-top:2rem;'>"
                "尚無對話，請在下方輸入您的問題 👇"
                "</p>",
                unsafe_allow_html=True,
            )
        else:
            for msg in history:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="msg-time" style="text-align:right;">{msg["time"]}</div>'
                        f'<div class="user-bubble">👤 {msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="msg-time">{msg["time"]}</div>'
                        f'<div class="ai-bubble">🤖 {msg["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown("<br>", unsafe_allow_html=True)

    st.divider()

    # 輸入區
    render_input()


def render_input() -> None:
    """渲染使用者輸入框與送出按鈕"""
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            label="輸入您的問題",
            placeholder="請輸入您想詢問的問題，例如：什麼是機器學習？",
            height=100,
            label_visibility="collapsed",
        )
        col1, col2 = st.columns([5, 1])
        with col2:
            submitted = st.form_submit_button(
                "送出 ✈️", use_container_width=True, type="primary"
            )

    if submitted:
        handle_submit(user_input)


def handle_submit(user_input: str) -> None:
    """
    處理使用者送出事件。

    Args:
        user_input: 使用者輸入的文字。
    """
    # 驗證空白輸入
    user_input = user_input.strip()
    if not user_input:
        st.warning("⚠️ 請輸入問題後再送出。")
        return

    # 取得 Agent（同時驗證 API Key）
    agent = get_agent()
    if agent is None:
        return

    # 記錄使用者訊息
    now = format_timestamp()
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input, "time": now}
    )

    # 呼叫 Agent 取得回應
    with st.spinner("AI 思考中..."):
        try:
            response = agent.run(user_input)
        except (ValueError, RuntimeError) as e:
            st.error(f"❌ {e}")
            # 移除剛才加入的使用者訊息（保持一致性）
            st.session_state.chat_history.pop()
            return

    # 記錄 AI 回應
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response, "time": format_timestamp()}
    )

    # 重新渲染頁面以顯示新訊息
    st.rerun()


# -----------------------------------------------------------------------
# 主程式
# -----------------------------------------------------------------------
def main() -> None:
    """應用程式主入口"""
    init_session()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()
