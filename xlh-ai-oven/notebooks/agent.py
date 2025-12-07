from dataclasses import dataclass
from pydantic_ai import Tool
from rich import print
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from deps import Deps
from tools import set_oven_temperature
from llm_model import get_model, LlmModel
from object_to_file import base_model_to_file

@dataclass
class Deps:
    name: str

class Ingredient(BaseModel):
    name: str = Field(description='Name der Zutat')
    quantity: str = Field(description='Menge')
    unit: str = Field(description='Einheit')

class Recipe(BaseModel):
    title: str = Field(description='Name der Pizza')
    ingredients: list[Ingredient] = Field(description='Zutaten für die Menuezubereitung')
    preparation_steps: list[str] = Field(description='Zubereitungsschritte')

def get_agent():
    model = get_model(llm_model=LlmModel.OPENROUTER_GPT_5_MINI)
    # model = get_model(llm_model=LlmModel.OPENROUTER_GPT_5_NANO)
    # model = get_model(llm_model=LlmModel.OPENROUTER_GEMINI_2_5_FLASH)
    # model = get_model(llm_model=LlmModel.OLLAMA_GPT_OSS_20B)
    return Agent(
        model=model,
        system_prompt=('Du bist ein Pizzabäcker welcher Rezepte für kreative Pizzas kreirt. '
                       'Nutze das Tool set_oven_temperature für die Einstellung des Backofens.'),
        deps_type=Deps,
        tools=[
            Tool(set_oven_temperature, takes_ctx=True),
        ],
        retries=3,
        output_type=Recipe,
    )

def main(user_prompt: str):
    deps = Deps(name='-')
    agent = get_agent()
    response = agent.run_sync(user_prompt=user_prompt, deps=deps)
    result: Recipe = response.output
    base_model_to_file(result)

    print(f'Antwort: {result.model_dump_json(indent=4)}')

    print('=====================================================================')
    settings = agent.model.settings
    print(f'Settings: {settings}')
    print(f'temperature: {settings.get('temperature')}')
    print(f'presence_penalty: {settings.get('presence_penalty')}')
    print(f'frequency_penalty: {settings.get('frequency_penalty')}')

    usage = response.usage()
    print(f'Input Tokens: {usage.input_tokens}')
    print(f'Output Tokens: {usage.output_tokens}')
    print(f'Total Tokens: {usage.total_tokens}')

if __name__ == '__main__':
    main(user_prompt='Ich habe im Kühlschrank Lachs, Salami und Tomaten '
                     'Kreire mir eine Pizza. '
                     'Da mein Backofen etwas alterschwach ist, '
                     'kann die Temperatur nicht höher als 225 Grad eingestellt werden '
                     'und die Backzeit darf 30 Minuten nicht überschreiten.')
