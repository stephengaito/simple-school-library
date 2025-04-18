import os
import yaml

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from schoolLib.setup import pagePart, routes, config, \
  getRoute, computePagePartUsers, pageParts

from schoolLib.htmxComponents import Div, List, Text, Link, \
  LongCode, RawHtml, HtmlPage, StdHeaders

devUser = True

###############################################################################
# provide a list based GUI overview of entry points

@pagePart
def listRoutes(pageData, aPath=None, **kwargs) :
  if aPath :
    aPath = '/' + aPath
  routesList = Div([])
  for aRoute in routes :
    if aPath and not aRoute.path.startswith(aPath) :
      continue
    anEndpoint = str(aRoute.endpoint.__module__) + \
      '.' + str(aRoute.endpoint.__name__)
    anEndpoint = anEndpoint.lstrip('schoolLib.')
    aList = List([])
    aList.appendChildren([
      Link(aRoute.path, aRoute.path, target='_blank'),
      Text(str(aRoute.methods), textType='s'),
      Link(
        f'/pageParts/{anEndpoint}',
        anEndpoint,
        target="_blank"
      ),
      Text(
        f"AnyUser = {aRoute.anyUser}", textType='s'
      )
    ])
    routesList.appendAChild(aList)
  return HtmlPage(StdHeaders(), routesList)

getRoute('/routes/{aPath:path}', listRoutes, anyUser=devUser)

@pagePart
def listPageParts(pageData, aPath=None, **kwargs) :
  computePagePartUsers()
  partsList = Div([])
  pagePartKeys = sorted(pageParts.keys())
  for aPagePartKey in pagePartKeys :
    aPartList = List([])
    aPagePart = pageParts[aPagePartKey]
    if not aPagePart.name.startswith(aPath) :
      continue
    aPartList.appendChildren([
      Text(aPagePart.name, textType='none'),
      Text(aPagePart.sig, textType='none'),
      Text(aPagePart.doc, textType='none')
    ])
    usersList = List([])
    for aUser in sorted(aPagePart.users) :
      if '/' in aUser :
        usersList.appendAChild(Link(f'/routes{aUser}', aUser))
      else :
        usersList.appendAChild(Link(f'/pageParts/{aUser}', aUser))
    aPartList.appendAChild(
      Text(['Used by:', usersList], textType=None)
    )
    metaDataList = List([])
    for aMetaData in aPagePart.metaData :
      for aKey, aValue in aMetaData.items() :
        if aValue :
          if '{' in aValue :
            aValue = aValue.split('{')[0].rstrip('/')
          if aKey in ['pagePart'] :
            metaDataList.appendAChild(Text([
              Text(aKey + ':', textType='none'),
              Link(f'/pageParts/{aValue}', aValue, target='_blank')
            ], textType='none'))
          elif aKey in ['hxGet', 'hxPost', 'link'] :
            metaDataList.appendAChild(Text([
              Text(aKey + ':', textType='none'),
              Link(f'/routes{aValue}', aValue, target='_blank')
            ], textType=None))
          else :
            metaDataList.appendAChild(
              Text(f"{aKey}: {aValue}", textType='none')
            )
    aPartList.appendAChild(
      Text(['Meta-Structure:', metaDataList], textType='none')
    )
    pygmentedSrc = highlight(aPagePart.src, PythonLexer(), HtmlFormatter())
    aPartList.appendAChild(
      Text(['Source:', LongCode(pygmentedSrc)], textType=None)
    )
    partsList.appendAChild(aPartList)
  return HtmlPage(
    StdHeaders([
     '<link rel="stylesheet" href="/static/css/pygmentsSas.css" type="text/css" />'  # noqa
    ]),
     partsList
  )

getRoute('/pageParts/{aPath:path}', listPageParts, anyUser=devUser)


###############################################################################
# provide a D3 based GUI overview

def computeLinksNodesSeen(routes, nodes, links, nodesSeen, showPath) :
  for aRoute in routes :
    aPath = aRoute.path
    if '{' in aPath :
      aPath = aPath.split('{')[0].rstrip('/')
    if aPath not in nodesSeen :
      # add the nodes
      radius = 2.5
      if aPath == showPath :
        print(f"Showing the route {aPath}")
        radius = 10
      nodes.append({
        'id'       : aPath,
        'path'     : f'/routes{aPath}',
        'nodeType' : 'default',
        'color'    : 'blue',
        'radius'   : radius
      })
      nodesSeen.add(aPath)

    # add the links
    anEndpoint = str(aRoute.endpoint.__module__) + \
      '.' + str(aRoute.endpoint.__name__)
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

def updateNodesLinks(nodes, links, nodesSeen, showPath) :
  for aPagePartName, aPagePart in pageParts.items() :
    if aPagePartName not in nodesSeen :
      # add the nodes
      radius = 2.5
      if aPagePartName == showPath :
        print(f"Showing the aPagePart {aPagePartName}")
        radius = 10
      nodes.append({
        'id'       : aPagePartName,
        'path'     : f'/pageParts/{aPagePartName}',
        'nodeType' : 'default',
        'color'    : 'red',
        'radius'   : radius
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

    for someMetaData in aPagePart.metaData :
      for aKey, aValue in someMetaData.items() :
        if not aValue :
          continue
        if aKey in ['hxGet', 'hxPost', 'link'] :
          if '{' in aValue :
            aValue = aValue.split('{')[0].rstrip('/')
          if aValue not in nodesSeen :
            print(f"Could not find the url {aValue} in {aPagePartName}")
            continue

          links.append({
            'source'   : aPagePartName,
            'target'   : aValue,
            'linkType' : aKey,
            'color'    : "blue"
          })

@pagePart
def provideUIOverview(pageData, aPath=None, **kwargs) :
  savePath = None
  showPath = ""
  if aPath :
    if aPath.startswith('save/') :
      savePath = aPath.removeprefix('save/')
    elif aPath.startswith('show/') :
      showPath = aPath.removeprefix('show/')

  computePagePartUsers()

  nodes = []
  nodesSeen = set()
  links = []

  computeLinksNodesSeen(routes, nodes, links, nodesSeen, showPath)

  updateNodesLinks(nodes, links, nodesSeen, showPath)

  jsonData = {"nodes": nodes, "links": links}

  if savePath :
      savePath = os.path.abspath(os.path.expanduser(savePath))
      try :
        os.makedirs(os.path.dirname(savePath), exist_ok=True)
        with open(savePath, 'w') as dataFile :
          dataFile.write(yaml.dump(jsonData))
        print(f"Saved ui overview data in {savePath}")
      except Exception as err :
        print(f"Could not save ui overview data in {savePath}")
        print(repr(err))

  svgHeight = 800
  if 'develop' in config and 'svgHeight' in config['develop'] :
    svgHeight = config['develop']['svgHeight']

  svgWidth = 800
  if 'develop' in config and 'svgWidth' in config['develop'] :
    svgWidth = config['develop']['svgWidth']

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
      <svg width="{svgWidth}" height="{svgHeight}" ></svg>
      <script>
      var graph = {jsonData};
      </script>
      <script src="/static/js/conceptmapper.js"></script>
      """
    )
  )

getRoute('/uiOverview/{aPath:path}', provideUIOverview, anyUser=devUser)
