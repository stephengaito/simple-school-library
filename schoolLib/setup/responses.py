
import os
#import yaml

from markdown import markdown

from starlette.responses import *
from starlette.templating import Jinja2Templates

from schoolLib.setup.exceptions import SLException
from schoolLib.setup.configuration import config

###############################################################
# Setup templates

def TemplateResponse(*args, **kwargs) :
  templates = config['templates']
  if not templates :
    raise SLException(
      "Templates Directory has not been configured yet",
      'Trying to use a template'
    )
  return templates.TemplateResponse(*args, **kwargs)

def GotoResponse(newUrl) :
  print(f"GOTO response {newUrl}")
  return RedirectResponse(url=newUrl, status_code=303)

###############################################################
# Markdown pages

def MarkdownResponse(request, path, template="help.html") :
  if 'markdownDir' not in config :
    print("Markdown direcotry not configured")
    return TemplateResponse(request, "404.html")
  markdownDir = config['markdownDir']

  markdownPath = os.path.join(markdownDir, path+'.md')
  if not os.path.isfile(markdownPath) :
    print(f"Markdown file [{markdownPath}] not found")
    return TemplateResponse(request, "404.html")

  makedownStr = ""
  with open(markdownPath) as mdFile :
    markdownStr = markdown(mdFile.read())

  return TemplateResponse(request, template, {
    'markdown' : markdownStr
  })
