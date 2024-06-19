
import os

from starlette.templating import Jinja2Templates

templatesDir = os.path.join(
  os.path.dirname(__file__),
  'templates'
)

templates = Jinja2Templates(directory=templatesDir)

def TemplateResponse(*args, **kwargs) :
  return templates.TemplateResponse(*args, **kwargs)

