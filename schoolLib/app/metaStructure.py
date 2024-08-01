
import yaml

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from schoolLib.setup          import *
from schoolLib.htmxComponents import *

@pagePart
async def listRoutes(request, db, aPath=None, **kwargs) :
  if aPath : aPath = '/'+aPath
  routesList = Div([])
  for aRoute in routes :
    if aPath and not aRoute.path.startswith(aPath) : continue
    anEndpoint = str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__)
    anEndpoint = anEndpoint.lstrip('schoolLib.')
    aList = List([])
    aList.appendChild(Link(aRoute.path, aRoute.path, target='_blank'))
    aList.appendChild(Text(str(aRoute.methods), textType='s'))
    aList.appendChild(Link(
      f'/pageParts/{anEndpoint}',
      anEndpoint,
      target="_blank"
    ))
    routesList.appendChild(aList)
  return HtmlPage( StdHeaders(), routesList )

getRoute('/routes/{aPath:path}', listRoutes)

@pagePart
async def listPageParts(request, db, aPath=None, **kwargs) :
  computePagePartUsers()
  partsList = Div([])
  pagePartKeys = sorted(pageParts.keys())
  for aPagePartKey in pagePartKeys :
    aPartList = List([])
    aPagePart = pageParts[aPagePartKey]
    if not aPagePart.name.startswith(aPath) : continue
    aPartList.appendChild(Text(aPagePart.name, textType='none'))
    aPartList.appendChild(Text(aPagePart.sig, textType='none'))
    aPartList.appendChild(Text(aPagePart.doc, textType='none'))
    usersList = List([])
    for aUser in sorted(aPagePart.users) :
      if '/' in aUser :
        usersList.appendChild(Link(f'/routes{aUser}', aUser ))
      else :
        usersList.appendChild(Link(f'/pageParts/{aUser}', aUser ))
    aPartList.appendChild(
      Text(['Used by:', usersList], textType=None)
    )
    metaDataList = List([])
    for aMetaData in aPagePart.metaData :
      for aKey, aValue in aMetaData.items() :
        if aValue :
          if '{' in aValue : aValue = aValue.split('{')[0]
          if aKey in ['callPagePart'] :
            metaDataList.appendChild(Text([
              Text(aKey+':', textType='none'),
              Link(f'/pageParts/{aValue}', aValue, target='_blank')
            ], textType='none'))
          elif aKey in ['hxGet', 'hxPost', 'link'] :
            metaDataList.appendChild(Text([
              Text(aKey+':', textType='none'),
              Link(f'/routes{aValue}', aValue, target='_blank')
            ], textType=None))
          else :
            metaDataList.appendChild(Text(f"{aKey}: {aValue}", textType='none'))
    aPartList.appendChild(
      Text(['Meta-Structure:', metaDataList], textType='none')
    )
    pygmentedSrc = highlight(aPagePart.src, PythonLexer(), HtmlFormatter())
    aPartList.appendChild(
      Text(['Source:', LongCode(pygmentedSrc)], textType=None)
    )
    partsList.appendChild(aPartList)
  return HtmlPage(
    StdHeaders([
     '<link rel="stylesheet" href="/static/css/pygmentsSas.css" type="text/css" />'
    ]),
     partsList
  )

getRoute('/pageParts/{aPath:path}', listPageParts)

@pagePart
async def provideUIOverview(request, db, **kwargs) :

  computePagePartUsers()

  nodes = []
  nodesSeen = set()
  links = []

  for aRoute in routes :
    aPath = aRoute.path
    if '{' in aPath : aPath = aPath.split('{')[0]
    if aPath not in nodesSeen :
      # add the nodes
      nodes.append({
        'id'       : aPath,
        'path'     : f'/routes{aPath}',
        'nodeType' : 'default',
        'color'    : 'blue'
      })
      nodesSeen.add(aPath)

    # add the links
    anEndpoint = str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__)
    anEndpoint = anEndpoint.lstrip('schoolLib.')
    if anEndpoint not in pageParts :
      print(f"Could not find the endpoint: {anEndpoint} for {aPath}")
      continue
    links.append({
      'source'   : aPath,
      'target'   : anEndpoint,
      'linkType' : "uses",
      'color'    : "green"
    })

  for aPagePartName, aPagePart in pageParts.items() :
    if aPagePartName not in nodesSeen :
      # add the nodes
      nodes.append({
        'id'       : aPagePartName,
        'path'     : f'/pageParts/{aPagePartName}',
        'nodeType' : 'default',
        'color'    : 'red'
      })
      nodesSeen.add(aPagePartName)

    # add the links
    for aUser in sorted(aPagePart.users) :
      if aUser not in pageParts :
        if '/' not in aUser :
          print(f"Could not find page part {aUser} for {aPagePartName}")
        continue

      links.append({
      'source'   : aUser,
      'target'   : aPagePartName,
      'linkType' : "uses",
      'color'    : "purple"
    })

  jsonData = { "nodes": nodes, "links": links }

  return HtmlPage(
    StdHeaders([
      '<script src="/static/js/d3.v7.min.js"></script>',
    ]),
    RawHtml(
      f"""
      <style>
      .nodes circle {{
        pointer-events: all;
        stroke: none;
        stroke-width: 40px;
      }}
      </style>
      <svg width = "800" height="600" ></svg>
      <script>
      var graph = {jsonData};
      </script>
      <script src="/static/js/conceptmapper.js"></script>
      """
    )
  )

getRoute('/uiOverview', provideUIOverview)
