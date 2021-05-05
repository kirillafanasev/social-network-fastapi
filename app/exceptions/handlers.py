import pathlib
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import status, FastAPI
from fastapi.exception_handlers import http_exception_handler
from fastapi.templating import Jinja2Templates

app_path = pathlib.Path(__file__).parent.parent.absolute()
print(app_path)
template_path = (app_path / 'templates').absolute()

templates = Jinja2Templates(directory=template_path)


def register_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def custom_exception_handler(request, exc):
        if exc.status_code == status.HTTP_403_FORBIDDEN:
            return templates.TemplateResponse(
                'access_forbidden.html',
                {'request': request}
            )

        return await http_exception_handler(request, exc)
