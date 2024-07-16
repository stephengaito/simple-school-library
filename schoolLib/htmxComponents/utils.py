
from copy import deepcopy
import glob
import inspect
import os
import yaml

from starlette.responses import HTMLResponse

from schoolLib.setup.configuration import config

#######################################################################
# theme

theme = {}

def loadedTheme() :
  if 'themeDir' not in config :
    config['themeDir'] = os.path.join(
      os.path.dirname(__file__),
      'theme'
    )

  themeGlob = os.path.join(
    config['themeDir'],
    '*.yaml'
  )

  try :
    for aYamlPath in glob.iglob(themeGlob) :
      with open(aYamlPath) as yamlFile :
         theme.update(yaml.safe_load(yamlFile.read()))
    return True
  except Exception as err :
    print(f"Could not load theme from [{config['themeDir']}]")
    print(repr(err))
  return False

#######################################################################

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

def computeClass(classDict, kwargs) :
  klass     = getFromKWArgs('class', [], kwargs)
  className = getFromKWArgs('className', 'default', kwargs)
  if isinstance(klass, str) : klass = [ klass ]
  if className in classDict :
    klass = mergeLists(deepcopy(classDict[className]), klass)
  if not klass : return ""
  return f'class="{' '.join(klass)}"'

def computeStyle(styleDict, kwargs) :
  style     = getFromKWArgs('style', [], kwargs)
  styleName = getFromKWArgs('styleName', 'default', kwargs)
  if isinstance(style, str) : style = [ style ]
  elif isinstance(style, dict) :
    styleList = []
    for aKey, aValue in style.items() :
      styleList.append(f"{aKey}: {aValue}")
    style = styleList
  if styleName in styleDict :
    style = mergeLists(deepcopy(styleDict[styleName]), style)
  if not style : return ""
  return f'style="{'; '.join(style)}"'

def computeAttrs(attrsDict, kwargs) :
  attrs     = getFromKWArgs('attrs', [], kwargs)
  attrsName = getFromKWArgs('attrsName', 'default', kwargs)
  if isinstance(attrs, str) : attrs = [ attrs ]
  elif isinstance(attrs, dict) :
    attrsList = []
    for aKey, aValue in attrs.items() :
      if aValue : attrsList.append(f'{aKey}="{aValue}"')
      else: attrsList.append(aKey)
    attrs = attrsList
  if attrsName in attrsDict :
    attrs = mergeLists(deepcopy(attrsDict[attrsName]), attrs)
  return ' '.join(attrs)

def computeAction(kwargs) :
  get  = getFromKWArgs('get', None, kwargs)
  post = getFromKWArgs('post', None, kwargs)
  actionStr = ""
  if 'get'    in kwargs : actionStr = f'hx-get="{kwargs['get']}"'
  elif 'post' in kwargs : actionStr = f'hx-post="{kwargs['post']}"'
  return actionStr

def computeTarget(kwargs) :
  target = getFromKWArgs('target', None, kwargs)
  swap   = getFromKWArgs('swap', None, kwargs)

  targetStr = ""
  if target :
    targetStr = f'hx-target="{target}"'
    if not swap : swap = 'outerHTML'
  if swap :
    targetStr += f' hx-swap="{swap}"'
  return targetStr

def computeId(kwargs) :
  anId = getFromKWArgs('theId', None, kwargs)

  idStr = ""
  if anId : idStr = f'id="{anId}"'
  return idStr

def computeHtmxAttrs(classDict, styleDict, attrsDict, kwargs) :
  if isinstance(classDict, str) :
    if classDict not in theme : theme[classDict] = {}
    classDict = theme[classDict]
  if isinstance(styleDict, str) :
    if styleDict not in theme : theme[styleDict] = {}
    styleDict = theme[styleDict]
  if isinstance(attrsDict, str) :
    if attrsDict not in theme : theme[attrsDict] = {}
    attrsDict = theme[attrsDict]
  allAttrs = [
    computeId(kwargs),
    computeAction(kwargs),
    computeTarget(kwargs),
    computeClass(classDict, kwargs),
    computeStyle(styleDict, kwargs),
    computeAttrs(attrsDict, kwargs)
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

def selectComponentInList(aComponentName, aComponentList) :
  aComponentList = deepcopy(aComponentList)

  for aComponent in aComponentList :
    if 'c-name' in aComponent \
    and aComponent['c-name'] == aComponentName :

      if 'className' not in aComponent :
        aComponent['className'] = 'selected'
      else :
        aComponent['className'] +='-selected'

      break

  return aComponentList

def HTMXResponse(request, theHtmxComponent, *args, **kwargs) :
  return HTMLResponse(computeComponent(theHtmxComponent), *args, **kwargs)
