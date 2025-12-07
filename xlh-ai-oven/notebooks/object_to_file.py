from pathlib import Path
from pydantic import BaseModel

def base_model_to_file(model: BaseModel, folder: Path | None = None, file_name: str | None = None):
    if file_name is None:
        file_name = (model.__class__.__name__).lower() + '.json'
    if folder is None:
        folder = Path(__file__).parents[0]
    (folder / file_name).write_text(model.model_dump_json(indent=2), encoding='utf-8')

def text_to_file(text: str, folder: Path, file_name: str):
    with open(folder / file_name, 'w', encoding="utf-8") as f:
        f.write(text)