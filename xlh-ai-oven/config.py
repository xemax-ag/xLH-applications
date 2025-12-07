from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

dotenv_path = Path(__file__).resolve().parents[0] / '.env'
print(dotenv_path)
load_dotenv()

class Config(BaseSettings):
    openai_api_key: str = ''
    openrouter_api_key: str = ''

config = Config()

if __name__ == '__main__':
    for item in config.__dict__.items():
        print(f'{item[0]}: {item[1]}')
