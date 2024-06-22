
from contextlib import contextmanager
import os
import sqlite3
import yaml

from markdown import markdown

from starlette.routing import Route #, Mount, WebSocketRoute
from starlette.responses import *
from starlette.templating import Jinja2Templates

###############################################################
# School Library Exceptions

class SLException(Exception) :
  def __init__(self, message, errType, helpMessage=None, origErr=None) :
    self.slMessage = message
    self.slErrType = errType
    self.slHelpMsg = helpMessage
    self.slOrigErr = origErr

###############################################################
# A simple (global) configuration system

config = {}
templates = None

def sanitizeConfig(config) :
  if 'database' not in config :
    config['database'] = 'db.sqlite'
  if 'templatesDir' not in config :
    config['templatesDir'] = os.path.join(
      os.path.dirname(__file__),
      'templates'
    )
  global templates
  templates = Jinja2Templates(directory=config['templatesDir'])

  if 'makrdownDir' not in config :
    config['markdownDir'] = os.path.join(
      os.path.dirname(__file__),
      'markdown'
    )

def loadedConfig(aConfigPath, reportErrors=False) :
  try :
    with open(aConfigPath) as configFile :
      config.update(yaml.safe_load(configFile.read()))
    sanitizeConfig(config)
    print("----------------------------------------")
    print(yaml.dump(config))
    print("----------------------------------------")
    return True
  except Exception as err :
    if reportErrors :
      print(repr(err))
  return False

###############################################################
# Setup templates

def TemplateResponse(*args, **kwargs) :
  if not templates :
    raise SLException(
      "Templates Directory has not been configured yet",
      'Trying to use a template'
    )
  return templates.TemplateResponse(*args, **kwargs)

def GotoResponse(newUrl) :
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

###############################################################
# A very simple RESTful router for the SchoolLib project

routes = []

def callWithParameters(request, func) :
  params = {}
  if request.query_params :
    params.update(request.guery_params)
  if request.path_params :
    params.update(request.path_params)
  #print("-------------------------------------")
  #print(request.url)
  #print(yaml.dump(params))
  #print("-------------------------------------")
  try :
    return func(request, **params)
  except SLException as slErr :
    return TemplateResponse(request, '500.html', {
      'errorMessage' : slErr.slMessage,
      'errorType'    : slErr.slErrType,
      'helpMessage'  : slErr.slHelpMsg,
      'origError'    : slErr.slOrigErr
    })

def get(aRoute, name=None) :
  def getDecorator(func) :
    def getWrapper(request) :
      return callWithParameters(request, func)
    routes.append(Route(aRoute, getWrapper, name=name, methods=["GET"]))
    return getWrapper
  return getDecorator

def put(aRoute, name=None) :
  def putDecorator(func) :
    async def putWrapper(request) :
      return callWithParameters(request, func)
    routes.append(Route(aRoute, putWrapper, name=name, methods=["PUT"]))
    return putWrapper
  return putDecorator

def post(aRoute, name=None) :
  def postDecorator(func) :
    async def postWrapper(request) :
      return await callWithParameters(request, func)
    routes.append(Route(aRoute, postWrapper, name=name, methods=["POST"]))
    return postWrapper
  return postDecorator

def patch(aRoute, name=None) :
  def patchDecorator(func) :
    def patchWrapper(request) :
      return callWithParameters(request, func)
    routes.append(Route(aRoute, patchWrapper, name=name, methods=["PATCH"]))
    return patchWrapper
  return patchDecorator

def delete(aRoute, name=None) :
  def deleteDecorator(func) :
    def deleteWrapper(request) :
      return callWithParameters(request, func)
    routes.append(Route(aRoute, deleteWrapper, name=name, methods=["DELETE"]))
    return deleteWrapper
  return deleteDecorator

###############################################################
# Some simple database handling utilities

@contextmanager
def getDatabase() :
  try :
    db = sqlite3.connect(config['database'])
    try :
      yield db
    finally :
      db.close()
  except Exception as err :
    print(f"Could not connect to the database: [{config['database']}]")
    print(repr(err))
    raise SLException(
      f"Could not open database [{config['database']}]",
      'Trying to open the database',
      'Have you configured the database properly?',
      repr(err)
    )
