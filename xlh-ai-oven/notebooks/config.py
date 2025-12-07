from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
import uuid

if uuid.getnode() == 255521439737186:
    # workstation phe dev
    dotenv_path = Path(__file__).resolve().parents[3] / 'xlh_ai_oven.env'
else:
    dotenv_path = Path(__file__).resolve().parents[0] / 'env.env'
print(dotenv_path)

load_dotenv(dotenv_path=dotenv_path)

class Config(BaseSettings):
    openai_api_key: str = ''
    openrouter_api_key: str = ''

config = Config()

if __name__ == '__main__':
    for item in config.__dict__.items():
        print(f'{item[0]}: {item[1]}')
    # print(uuid.getnode())


