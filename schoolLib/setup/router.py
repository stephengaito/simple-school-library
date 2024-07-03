
from functools import wraps
#import yaml

from starlette.routing import Route #, Mount, WebSocketRoute

from schoolLib.setup.exceptions import SLException
from schoolLib.setup.responses import TemplateResponse

###############################################################
# A very simple RESTful router for the SchoolLib project
#
# see: https://restfulapi.net/http-methods/

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
    @wraps(func)
    def getWrapper(request) :
      return callWithParameters(request, func)
    routes.append(Route(aRoute, getWrapper, name=name, methods=["GET"]))
    return getWrapper
  return getDecorator

def put(aRoute, name=None) :
  def putDecorator(func) :
    @wraps(func)
    async def putWrapper(request) :
      return await callWithParameters(request, func)
    routes.append(Route(aRoute, putWrapper, name=name, methods=["PUT", "POST"]))
    return putWrapper
  return putDecorator

def post(aRoute, name=None) :
  def postDecorator(func) :
    @wraps(func)
    async def postWrapper(request) :
      return await callWithParameters(request, func)
    routes.append(Route(aRoute, postWrapper, name=name, methods=["POST"]))
    return postWrapper
  return postDecorator

def patch(aRoute, name=None) :
  def patchDecorator(func) :
    @wraps(func)
    async def patchWrapper(request) :
      return await callWithParameters(request, func)
    routes.append(Route(aRoute, patchWrapper, name=name, methods=["PATCH", "POST"]))
    return patchWrapper
  return patchDecorator

def delete(aRoute, name=None) :
  def deleteDecorator(func) :
    @wraps(func)
    def deleteWrapper(request) :
      return callWithParameters(request, func)
    routes.append(Route(aRoute, deleteWrapper, name=name, methods=["GET", "DELETE"]))
    return deleteWrapper
  return deleteDecorator