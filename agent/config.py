"""
config.py
負責從環境變數（.env 檔案）讀取設定值。
所有設定集中管理，方便後續擴充。
"""

import os
from dotenv import load_dotenv

# 載入 .env 檔案（若存在）
load_dotenv()


class Config:
    """集中管理應用程式設定"""

    # OpenAI API 金鑰
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # 使用的模型名稱，預設為 gpt-3.5-turbo
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

    # 最大 token 數限制
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1024"))

    # 對話溫度（0~2，越高越隨機）
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    @classmethod
    def validate(cls) -> None:
        """驗證必要設定是否存在，若缺少則拋出例外"""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "❌ 未設定 OPENAI_API_KEY。\n"
                "請複製 .env.example 為 .env，並填入您的 API 金鑰。"
            )


# 建立全域設定實例，供其他模組直接引用
config = Config()
