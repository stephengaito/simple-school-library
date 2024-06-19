# A very simple RESTful router for the SchoolLib project

from starlette.routing import Route, Mount, WebSocketRoute

routes = []

def get(aRoute, name=None) :
  def getDecorator(func) :
    routes.append(
      Route(aRoute, func, name=name, methods=["GET"])
    )
    return func
  return getDecorator

def put(aRoute, name=None) :
  def putDecorator(func) :
    routes.append(
      Route(aRoute, func, name=name, methods=["PUT"])
    )
    return func
  return putDecorator

def post(aRoute, name=None) :
  def postDecorator(func) :
    routes.append(
      Route(aRoute, func, name=name, methods=["POST"])
    )
    return func
  return postDecorator

def patch(aRoute, name=None) :
  def patchDecorator(func) :
    routes.append(
      Route(aRoute, func, name=name, methods=["PATCH"])
    )
    return func
  return patchDecorator


def delete(aRoute, name=None) :
  def deleteDecorator(func) :
    routes.append(
      Route(aRoute, func, name=name, methods=["DELETE"])
    )
    return func
  return deleteDecorator
