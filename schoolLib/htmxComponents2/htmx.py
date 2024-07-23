

from starlette.responses import HTMLResponse
from starlette.exceptions import HTTPException

def mergeLists(origList, additionalList) :
  newList = []
  for anItem in origList :
    if anItem not in newList : newList.append(anItem)

  for anItem in additionalList :
    if anItem not in newList : newList.append(anItem)

  return newList

class HtmxBase :

  def __init__(self, **kwargs) :
    self.kwargs = kwargs
    self.id     = None
    if 'id' in kwargs : self.id = kwargs['id']

  def collectHtml(self, htmlFragments, **kwargs) :
    pass

  def response(self, *args, **kwargs) :
    htmlFragments = []
    self.collectHtml(htmlFragments)
    return HTMLResponse(' '.join(htmlFragments), *args, **kwargs)

  #################################################################
  # build HTML attributes from kwargs and theme

  def getFromKWArgs(self, aKey, aDefault) :
    theValue = aDefault
    if aKey in self.kwargs : theValue = self.kwargs[aKey]
    return theValue

  def computeClass(self, classDict) :
    klass     = self.getFromKWArgs('class', [])
    className = self.getFromKWArgs('className', 'default')
    if isinstance(klass, str) : klass = [ klass ]
    if className in classDict :
      klass = mergeLists(classDict[className], klass)
    if not klass : return ""
    return f'class="{' '.join(klass)}"'

  def computeStyle(self, styleDict) :
    style     = self.getFromKWArgs('style', [])
    styleName = self.getFromKWArgs('styleName', 'default')
    if isinstance(style, str) : style = [ style ]
    elif isinstance(style, dict) :
      styleList = []
      for aKey, aValue in style.items() :
        styleList.append(f"{aKey}: {aValue}")
      style = styleList
    if styleName in styleDict :
      style = mergeLists(styleDict[styleName], style)
    if not style : return ""
    return f'style="{'; '.join(style)}"'

  def computeAttrs(self, attrsDict) :
  attrs     = self.getFromKWArgs('attrs', [])
  attrsName = self.getFromKWArgs('attrsName', 'default')
  if isinstance(attrs, str) : attrs = [ attrs ]
  elif isinstance(attrs, dict) :
    attrsList = []
    for aKey, aValue in attrs.items() :
      if aValue : attrsList.append(f'{aKey}="{aValue}"')
      else: attrsList.append(aKey)
    attrs = attrsList
  if attrsName in attrsDict :
    attrs = mergeLists(attrsDict[attrsName], attrs)
  return ' '.join(attrs)

  def computeAction(self) :
    get  = self.getFromKWArgs('get', None)
    post = self.getFromKWArgs('post', None)
    actionStr = ""
    if 'get'    in self.kwargs : actionStr = f'hx-get="{self.kwargs['get']}"'
    elif 'post' in self.kwargs : actionStr = f'hx-post="{self.kwargs['post']}"'
    return actionStr

  def computeTrigger(self) :
    trigger = self.getFromKWArgs('trigger', None)
    triggerStr = ""
    if trigger :
      triggerStr = f'hx-trigger="{trigger}"'
    return triggerStr

  def computeTarget(self) :
    target = self.getFromKWArgs('target', None)
    swap   = self.getFromKWArgs('swap', None)

    targetStr = ""
    if target :
      targetStr = f'hx-target="{target}"'
      if not swap : swap = 'outerHTML'
    if swap :
      targetStr += f' hx-swap="{swap}"'
    return targetStr

  def computeId(self) :
    anId = self.getFromKWArgs('theId', None)

    idStr = ""
    if anId : idStr = f'id="{anId}"'
    return idStr

  def computeHtmxAttrs(self) :
    className = self.__class__.__name__
    classDict = className+'Classes'
    if classDict not in theme : theme[classDict] = {}
    classDict = theme[classDict]
    styleDict = className+'Styles'
    if styleDict not in theme : theme[styleDict] = {}
    styleDict = theme[styleDict]
    attrsDict = className+'Attrs'
    if attrsDict not in theme : theme[attrsDict] = {}
    attrsDict = theme[attrsDict]

    allAttrs = [
      self.computeId(),
      self.computeAction(kwargs),
      self.computeTarget(kwargs),
      self.computeTrigger(kwargs),
      self.computeClass(classDict),
      self.computeStyle(styleDict),
      self.computeAttrs(attrsDict)
    ]
    theAttrs = [x for x in allAttrs if x]
    return " ".join(theAttrs)

class HtmxChildrenBase(HtmxBase) :
  def __init__(self, someChildren **kwargs) :
    super().__init__(**kwargs)
    if not isinstance(someChildren, list) :
      someChildren = [ someChildren ]
    self.children = someChildren

  def appendChild(self, aChild) :
    self.children.append(aChild)

  def collectChildrenHtml(self, htmlFragments) :
    for aChild in self.children :
      aChild.collectHtml(htmlFragments, **self.childKWArgs)
