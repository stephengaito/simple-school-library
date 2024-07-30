
import os
import yaml

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles

from schoolLib.setup import *
from schoolLib.htmxComponents import *
from schoolLib.app.menus import *

loadedConfig('config.yaml', verbose=True)
loadedTheme()

# The ORDER here is important!
import schoolLib.app.home.menu
import schoolLib.app.books
import schoolLib.app.people
import schoolLib.app.tasks.menu

@pagePart
async def homePage(request, db, **kwargs):
  """ The Home Page """
  return HtmlPage(
    StdHeaders(),
    StdBody()
  )

getRoute('/', homePage)

@pagePart
async def listRoutes(request, db, aPath=None, **kwargs) :
  if aPath : aPath = '/'+aPath
  routesStrs = []
  for aRoute in routes :
    if aPath and not aRoute.path.startswith(aPath) : continue
    routesStrs.append(
      ' '.join([
        '<p>',
        str(aRoute.path),
        str(aRoute.methods),
        str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__),
        '</p>'
      ]))
  return Text('\n'.join(sorted(routesStrs)))

getRoute('/routes/{aPath:path}', listRoutes)

@pagePart
async def listPageParts(request, db, aPath=None, **kwargs) :
  if aPath : aPath = '/'+aPath
  pagePartStrs = []
  pagePartKeys = sorted(pageParts.keys())
  for aPagePartKey in pagePartKeys :
    aPagePart    = pageParts[aPagePartKey]
    await aPagePart.collectMetaData()
    pagePartName = aPagePart.name
    pagePartSig  = aPagePart.sig
    pagePartDoc  = aPagePart.doc
    if not aPagePart.name.startswith(aPath) : continue
    pagePartStrs.append(
      ' '.join([
        '<p><ul>',
        '<li>', aPagePart.name, '</li>',
        '<li>', aPagePart.sig, '</li>',
        '<li>', aPagePart.doc, '</li>',
        '<li>MetaData: <ul><li>', '</li><li>'.join(aPagePart.metaData), '</li></ul></li>'
        #'<pre>',
        #aPagePart.src,
        #'</pre>',
        '</ul></p>'
      ]))
  return Text('\n'.join(sorted(pagePartStrs)))

getRoute('/pageParts/{aPath:path}', listPageParts)

@pagePart
async def helpPages(request, db, aPath=None, **kwargs) :
  if not aPath : aPath = 'help'
  someMarkdown = loadMarkdownFromFile(aPath)

  return Level0div([
    TopLevelMenu.select('home'),
    Level1div(MarkdownDiv(someMarkdown))
  ])

getRoute('/help/{aPath:path}', helpPages)

async def notFound(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return htmlResponseFromHtmx(Level0div([
    TopLevelMenu.select('home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!"),
      Text(f"Looking for: [{request.url}]")
    ])
  ], status_code=404))

async def serverError(request, theException) :
  print("-------------")
  print(repr(request))
  print(repr(theException))
  print("-------------")
  return htmlResponseFromHtmx(Level0div([
    TopLevelMenu.select('home'),
    Level1div([
      Text("Opps! Something went wrong! We can't find that page!", type='p'),
      Text(f"Looking for: [{request.url}]", type='p'),
      Text(f"Error: {repr(theException)}", type="p"),
    ])
  ], status_code=500))

app = Starlette(
  debug=True,
  routes=routes,
  exception_handlers={
    404: notFound,
    500: serverError
  }
)
app.mount('/static', StaticFiles(packages=['schoolLib']), name='static')

