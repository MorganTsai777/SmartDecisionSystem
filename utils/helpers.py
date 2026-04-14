"""
helpers.py
共用輔助函式，供 app.py 或其他模組使用。
"""

from datetime import datetime


def format_timestamp(dt: datetime | None = None) -> str:
    """
    將 datetime 物件格式化為易讀字串。

    Args:
        dt: 要格式化的 datetime，預設使用當前時間。

    Returns:
        格式化後的時間字串，例如 "2024-01-15 14:30:00"。
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 100, suffix: str = "…") -> str:
    """
    截斷過長的文字，用於 UI 預覽顯示。

    Args:
        text: 原始文字。
        max_length: 最大允許字元數（預設 100）。
        suffix: 截斷後附加的結尾符號。

    Returns:
        截斷後的文字；若原始文字不超過 max_length 則原樣回傳。
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


def sanitize_input(text: str) -> str:
    """
    清理使用者輸入，移除前後空白及多餘換行。

    Args:
        text: 原始輸入文字。

    Returns:
        清理後的文字。
    """
    return " ".join(text.split())
