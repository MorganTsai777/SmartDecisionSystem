"""
agent.py
核心 AI Agent 類別。

目前實作：單一 LLM 問答模式（OpenAI Chat Completions API）。

擴充空間（預留介面）：
- Tools / Function Calling：可在 _build_tools() 中定義工具
- Memory 升級：可替換 ConversationMemory 為更複雜的實作
- Multi-Agent：可在 run() 中呼叫多個子 Agent 協作
"""

from openai import OpenAI, OpenAIError

from .config import config
from .memory import ConversationMemory


# 預設系統提示詞
DEFAULT_SYSTEM_PROMPT = (
    "你是一個友善且專業的 AI 助理，使用繁體中文回答使用者的問題。"
    "請盡量提供清楚、有條理且正確的回答。"
)


class AIAgent:
    """
    AI Agent 主類別。

    職責：
    - 接收使用者輸入
    - 透過 LLM 生成回應
    - 維護對話記憶體

    使用範例：
        agent = AIAgent()
        response = agent.run("什麼是機器學習？")
        print(response)
    """

    def __init__(self, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> None:
        """
        初始化 Agent。

        Args:
            system_prompt: 自訂系統提示詞，預設使用 DEFAULT_SYSTEM_PROMPT。

        Raises:
            ValueError: 若 OPENAI_API_KEY 未設定。
        """
        # 驗證 API 金鑰是否存在
        config.validate()

        # 初始化 OpenAI 用戶端
        self._client = OpenAI(api_key=config.OPENAI_API_KEY)

        # 初始化對話記憶體
        self.memory = ConversationMemory(system_prompt=system_prompt)

        # 預留工具清單（Tool Use / Function Calling 擴充點）
        self._tools: list = self._build_tools()

    # ------------------------------------------------------------------
    # 公開方法
    # ------------------------------------------------------------------

    def run(self, user_input: str) -> str:
        """
        處理使用者輸入並回傳 AI 回應。

        Args:
            user_input: 使用者輸入的文字。

        Returns:
            AI 回應的文字字串。

        Raises:
            ValueError: 若輸入為空白。
            RuntimeError: 若 API 呼叫失敗。
        """
        # 驗證輸入
        user_input = user_input.strip()
        if not user_input:
            raise ValueError("輸入不可為空白，請輸入您的問題。")

        # 將使用者訊息加入記憶體
        self.memory.add_user_message(user_input)

        try:
            # 呼叫 OpenAI API
            response = self._call_llm()
        except OpenAIError as e:
            # API 呼叫失敗時，僅移除剛才加入的使用者訊息，保留之前的對話歷史
            messages = self.memory.get_messages()
            if messages and messages[-1].role == "user":
                self.memory._messages.pop()
            raise RuntimeError(f"模型呼叫失敗：{e}") from e

        # 將 AI 回應加入記憶體
        self.memory.add_assistant_message(response)

        return response

    def reset(self) -> None:
        """清除對話記憶體，開始新的對話"""
        self.memory.clear()

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _call_llm(self) -> str:
        """
        呼叫 LLM API 並回傳回應文字。

        Returns:
            模型回應的文字內容。
        """
        completion = self._client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=self.memory.to_openai_format(),
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE,
        )
        return completion.choices[0].message.content or ""

    def _build_tools(self) -> list:
        """
        預留工具定義方法。

        未來可在此定義 OpenAI Function Calling 工具，例如：
        - 搜尋網頁
        - 查詢資料庫
        - 執行程式碼

        Returns:
            工具定義清單（目前為空）。
        """
        return []


if __name__ == "__main__":
    # 簡易 CLI 測試模式
    import sys

    print("=== AI Agent CLI 測試模式 ===")
    print("輸入 'exit' 或 'quit' 退出\n")

    try:
        agent = AIAgent()
    except ValueError as e:
        print(e)
        sys.exit(1)

    while True:
        user_input = input("您：").strip()
        if user_input.lower() in ("exit", "quit", ""):
            print("再見！")
            break
        try:
            answer = agent.run(user_input)
            print(f"AI：{answer}\n")
        except (ValueError, RuntimeError) as e:
            print(f"[錯誤] {e}\n")
