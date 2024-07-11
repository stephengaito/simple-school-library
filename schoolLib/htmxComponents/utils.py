
from copy import deepcopy
import inspect

from starlette.responses import HTMLResponse

def mergeLists(origList, additionalList) :
  newList = []
  for anItem in origList :
    if anItem not in newList : newList.append(anItem)

  for anItem in additionalList :
    if anItem not in newList : newList.append(anItem)

  return newList

def getFromKWArgs(aKey, aDefault, kwargs) :
  theValue = aDefault
  if aKey in kwargs : theValue = kwargs[aKey]
  return theValue

def computeStyle(kwargs) :
  style     = getFromKWArgs('style', [], kwargs)
  styleName = getFromKWArgs('styleName', None, kwargs)
  styleDict = getFromKWArgs('styleDict', {}, kwargs)

  if isinstance(style, str) : style = [ style ]
  elif isinstance(style, dict) :
    styleList = []
    for aKey, aValue in style.items() :
      styleList.append(f"{aKey}: {aValue}")
    style = styleList
  if styleName and styleName in styleDict :
    style = mergeLists(styleDict[styleName], style)
  if not style : return ""
  return f'style="{'; '.join(style)}"'

def computeClass(kwargs) :
  klass     = getFromKWArgs('klass', [], kwargs)
  className = getFromKWArgs('className', None, kwargs)
  classDict = getFromKWArgs('classDict', {}, kwargs)

  if isinstance(klass, str) : klass = [ klass ]
  if className and className in classDict :
    klass = mergeLists(classDict[className], klass)
  if not klass : return ""
  return f'class="{' '.join(klass)}"'

def computeAttrs(kwargs) :
  attrs     = getFromKWArgs('attrs', [], kwargs)
  attrsName = getFromKWArgs('attrsName', None, kwargs)
  attrsDict = getFromKWArgs('attrsDict', {}, kwargs)

  if isinstance(attrs, str) : attrs = [ attrs ]
  elif isinstance(attrs, dict) :
    attrsList = []
    for aKey, aValue in attrs.items() :
      if aValue : attrsList.append(f'{aKey}="{aValue}"')
      else: attrsList.append(aKey)
    attrs = attrsList
  if attrsName and attrsName in attrsDict :
    attrs = mergeLists(attrsDict[attrsName], attrs)
  return ' '.join(attrs)

def computeGet(kwargs) :
  get = getFromKWArgs('get', None, kwargs)

  getStr = ""
  if get : getStr = f'hx-get="{get}"'
  return getStr

def computePost(kwargs) :
  post = getFromKWArgs('post', None, kwargs)

  postStr = ""
  if post : postStr = f'hx-post="{post}"'
  return postStr

def computeId(kwargs) :
  anId = getFromKWArgs('theId', None, kwargs)

  idStr = ""
  if anId : idStr = f'id="{anId}"'
  return idStr

def computeHtmxAttrs(kwargs) :
  allAttrs = [
    computeId(kwargs),
    computeGet(kwargs),
    computePost(kwargs),
    computeClass(kwargs),
    computeStyle(kwargs),
    computeAttrs(kwargs)
  ]
  theAttrs = [x for x in allAttrs if x]
  return " ".join(theAttrs)

def computeComponent(aComponent) :
  if isinstance(aComponent, list) :
    componentHtml = []
    for aSubComponent in aComponent :
      componentHtml.append(computeComponent(aSubComponent))
    return '\n'.join(componentHtml)

  if isinstance(aComponent, str) : return aComponent
  if not isinstance(aComponent, dict) :
    raise HTTPException(404, details="Corrupted htmx component")

  try :
    theComponentHtml = \
      inspect.currentframe().f_back.f_globals[aComponent['component']](**aComponent)
  except Exception as err:
    print(repr(err))
    return ""
  return theComponentHtml

emptySelectors = {
  'style' : {},
  'attrs' : {},
  'class' : []
}

def selectComponentInList(
  aComponentIndex, aComponentList,
  selectorType, selectorKey, selectorValue=""
) :
  if not isinstance(aComponentList, list) : return aComponentList
  if aComponentIndex not in range(len(aComponentList)) :
    return aComponentList

  aComponentList = deepcopy(aComponentList)

  theSelectedComponent = aComponentList[aComponentIndex]
  if not isinstance(theSelectedComponent, dict) : return aComponentList

  if selectorType not in theSelectedComponent :
    theSelectedComponent[selectorType] = \
      deepcopy(emptySelectors[selectorType])
  if isinstance(theSelectedComponent[selectorType], dict) :
    theSelectedComponent[selectorType][selectorKey] = selectorValue
  else :
    theSelectedComponent[selectorType].append(selectorKey)

  return aComponentList

def HTMXResponse(request, theHtmxComponent, *args, **kwargs) :
  return HTMLResponse(computeComponent(theHtmxComponent), *args, **kwargs)
