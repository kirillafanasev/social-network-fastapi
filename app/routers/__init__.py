import pathlib
from fastapi.templating import Jinja2Templates

app_path = pathlib.Path(__file__).parent.parent.absolute()
template_path = (app_path / 'templates').absolute()

templates = Jinja2Templates(directory=template_path)
