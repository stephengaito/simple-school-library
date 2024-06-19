
import os

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from schoolLib.router import *
from schoolLib.templates import *

@get('/')
def homepage(request):
    return TemplateResponse(request, 'index.html')

@get('/user/me')
def user_me(request):
    username = "John Doe"
    return PlainTextResponse('Hello, %s!' % username)

@get('/user/{username}')
def user(request):
    username = request.path_params['username']
    return PlainTextResponse('Hello, %s!' % username)

@get('/ws')
async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text('Hello, websocket!')
    await websocket.close()

app = Starlette(debug=True, routes=routes)
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')
