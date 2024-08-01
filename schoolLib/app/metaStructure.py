
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
  return HtmlPage( StdHeaders(), partsList)

getRoute('/pageParts/{aPath:path}', listPageParts)