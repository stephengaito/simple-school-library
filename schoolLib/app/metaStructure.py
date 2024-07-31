
import yaml

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from schoolLib.setup          import *
from schoolLib.htmxComponents import *

@pagePart
async def listRoutes(request, db, aPath=None, **kwargs) :
  if aPath : aPath = '/'+aPath
  stdHeaders = StdHeaders()
  htmlStrs = ['<!DOCTYPE html><html lang="en"><head>']
  stdHeaders.collectHtml(htmlStrs)
  htmlStrs.append("</head><body>")
  for aRoute in routes :
    if aPath and not aRoute.path.startswith(aPath) : continue
    anEndpoint = str(aRoute.endpoint.__module__)+'.'+str(aRoute.endpoint.__name__)
    anEndpoint = anEndpoint.lstrip('schoolLib.')
    htmlStrs.append(
      ' '.join([
        '<p>', '<ul>'
        f'<li><a href="{aRoute.path}" target="_blank">{aRoute.path}</a></li>',
        '<li>', str(aRoute.methods), '</li>'
        '<li>', f'<a href="/pageParts/{anEndpoint}" target="_blank">{anEndpoint}</a>', '</li>'
        '</ul>', '</p>'
      ]))
  htmlStrs.append("</body></html>")
  return '\n'.join(sorted(htmlStrs))

getRoute('/routes/{aPath:path}', listRoutes)

@pagePart
async def listPageParts(request, db, aPath=None, **kwargs) :
  #if aPath : aPath = '/'+aPath
  stdHeaders = StdHeaders()
  htmlStrs = ['<!DOCTYPE html><html lang="en"><head>']
  stdHeaders.collectHtml(htmlStrs)
  htmlStrs.append("</head><body>")
  pagePartKeys = sorted(pageParts.keys())
  for aPagePartKey in pagePartKeys :
    aPagePart    = pageParts[aPagePartKey]
    await aPagePart.collectMetaData()
    pagePartName = aPagePart.name
    pagePartSig  = aPagePart.sig
    pagePartDoc  = aPagePart.doc
    if not aPagePart.name.startswith(aPath) : continue
    pygmentedSrc = highlight(aPagePart.src, PythonLexer(), HtmlFormatter())
    metaDataStrs = []
    for aMetaData in aPagePart.metaData :
      for aKey, aValue in aMetaData.items() :
        if aValue :
          if aKey in ['callPagePart'] :
            metaDataStrs.append(
              f'{aKey}: <a href="/pageParts/{aValue}" target="_blank">{aValue}</a>'
            )
          elif aKey in ['hxGet', 'hxPost'] :
            metaDataStrs.append(
              f'{aKey}: <a href="/routes{aValue}" target="_blank">{aValue}</a>'
            )
          else :
            metaDataStrs.append(
              f"{aKey}: {aValue}"
            )
    htmlStrs.append(
      ' '.join([
        '<p><ul>',
        '<li>', aPagePart.name, '</li>',
        '<li>', aPagePart.sig, '</li>',
        '<li>', aPagePart.doc, '</li>',
        '<li>MetaData: <ul><li>', '</li><li>'.join(metaDataStrs), '</li></ul></li>',
        pygmentedSrc,
        '</ul></p>'
      ]))
  htmlStrs.append("</body></html>")
  return '\n'.join(sorted(htmlStrs))

getRoute('/pageParts/{aPath:path}', listPageParts)