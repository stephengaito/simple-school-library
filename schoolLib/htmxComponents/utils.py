
from copy import deepcopy
import inspect

def mergeLists(origList, additionalList) :
  newList = []
  for anItem in origList :
    if anItem not in newList : newList.append(anItem)

  for anItem in additionalList :
    if anItem not in newList : newList.append(anItem)

  return newList

def computeStyle(styleName, styleDict, style) :
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

def computeClass(className, classDict, klass) :
  if isinstance(klass, str) : klass = [ klass ]
  if className and className in classDict :
    klass = mergeLists(classDict[className], klass)
  if not klass : return ""
  return f'class="{' '.join(klass)}"'

def computeAttrs(attrsName, attrsDict, attrs) :
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

def computeGet(get) :
  getStr = ""
  if get : getStr = f'hx-get="{get}"'
  return getStr

def computeId(anId) :
  idStr = ""
  if anId : idStr = f'id="{anId}"'
  return idStr

def computeComponent(aComponent) :
  if isinstance(aComponent, list) :
    componentHtml = []
    for aSubComponent in aComponent :
      componentHtml.append(computeComponent(aSubComponent))
    return '\n'.join(componentHtml)

  if not isinstance(aComponent, dict) : return aComponent

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