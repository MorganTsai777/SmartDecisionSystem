"""
memory.py
管理 AI Agent 的對話紀錄（記憶體）。
目前以 in-session list 實作；未來可擴充為持久化儲存（資料庫、檔案等）。
"""

from dataclasses import dataclass
from typing import List, Literal


# 訊息角色型別
Role = Literal["user", "assistant", "system"]


@dataclass
class Message:
    """單一對話訊息"""
    role: Role
    content: str


class ConversationMemory:
    """
    對話記憶體管理器。

    職責：
    - 儲存本次 session 的所有對話訊息
    - 提供訊息新增、讀取、清除功能
    - 將記憶轉換為 OpenAI Chat 格式的 messages list

    擴充空間：
    - 可加入摘要壓縮（Summarization）以節省 token
    - 可加入持久化儲存（SQLite / Redis）
    - 可加入滑動視窗限制記憶長度
    """

    def __init__(self, system_prompt: str = "") -> None:
        """
        初始化記憶體。

        Args:
            system_prompt: 系統提示詞，設定 Agent 的角色與行為。
        """
        self._messages: List[Message] = []
        self._system_prompt = system_prompt

        # 若有系統提示詞，加入為第一則訊息
        if system_prompt:
            self._messages.append(Message(role="system", content=system_prompt))

    # ------------------------------------------------------------------
    # 訊息操作
    # ------------------------------------------------------------------

    def add_user_message(self, content: str) -> None:
        """新增使用者訊息"""
        self._messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """新增 AI 回應訊息"""
        self._messages.append(Message(role="assistant", content=content))

    def clear(self) -> None:
        """清除所有對話紀錄（保留系統提示詞）"""
        self._messages = []
        if self._system_prompt:
            self._messages.append(Message(role="system", content=self._system_prompt))

    # ------------------------------------------------------------------
    # 資料讀取
    # ------------------------------------------------------------------

    def get_messages(self) -> List[Message]:
        """回傳所有訊息（含系統提示詞）"""
        return list(self._messages)

    def get_chat_messages(self) -> List[Message]:
        """回傳不含系統提示詞的對話訊息（供 UI 顯示用）"""
        return [m for m in self._messages if m.role != "system"]

    def to_openai_format(self) -> List[dict]:
        """
        將訊息轉換為 OpenAI API 所需格式。

        Returns:
            [{"role": "...", "content": "..."}, ...]
        """
        return [{"role": m.role, "content": m.content} for m in self._messages]

    def is_empty(self) -> bool:
        """檢查是否無任何對話紀錄（不計系統提示詞）"""
        return len(self.get_chat_messages()) == 0

    def __len__(self) -> int:
        """回傳對話訊息數量（不含系統提示詞）"""
        return len(self.get_chat_messages())
