

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