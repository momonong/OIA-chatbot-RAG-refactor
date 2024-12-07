import os
from dotenv import load_dotenv
import openai

# 載入 .env 檔案
load_dotenv()

# 設定 OpenAI API 相關參數
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-09-01-preview"


def call_llm(prompt, model="gpt-35-turbo-instruct", max_tokens=100, temperature=0.5):
    """
    呼叫 Azure OpenAI 模型生成結果

    Args:
        prompt (str): 要提供給模型的提示詞
        model (str): 模型部署名稱
        max_tokens (int): 最大 token 數
        temperature (float): 溫度參數 (控制生成的隨機性)

    Returns:
        str: 模型生成的結果
    """
    try:
        # 呼叫模型
        response = openai.completions.create(
            model="gpt-35-turbo-instruct",  # 請替換為您的模型部署名稱
            prompt=prompt,
            max_tokens=100,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None
