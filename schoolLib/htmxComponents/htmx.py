
import glob
import json
import os
import yaml

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
    # print(yaml.dump(theme))
    return True
  except Exception as err :
    print(f"Could not load theme from [{config['themeDir']}]")
    print(repr(err))
  return False

#######################################################################

def mergeLists(origList, additionalList) :
  newList = []
  for anItem in origList :
    if anItem not in newList :
      newList.append(anItem)

  for anItem in additionalList :
    if anItem not in newList :
      newList.append(anItem)

  return newList

class HtmxBase :

  def __init__(
    self,
    theId=None,
    klass=[],
    klassName='default',
    style=[],
    styleName='default',
    attrs=[],
    attrsName='default',
    hxGet=None,
    hxPost=None,
    hxTrigger=None,
    hxTarget=None,
    hxSwap=None,
    hxSwapOob=None,
    hxHeaders={},
    hyperscript=None,
    **kwargs
  ) :
    self.kwargs      = kwargs
    self.theId       = theId
    self.klass       = klass
    self.klassName   = klassName
    self.style       = style
    self.styleName   = styleName
    self.attrs       = attrs
    self.attrsName   = attrsName
    self.hxGet       = hxGet
    self.hxPost      = hxPost
    self.hxTrigger   = hxTrigger
    self.hxTarget    = hxTarget
    self.hxSwap      = hxSwap
    self.hxSwapOob   = hxSwapOob
    self.hxHeaders   = hxHeaders
    self.hyperscript = hyperscript

  def isA(self, klass) :
    return isinstance(self, klass)

  def collectHtmlStr(self) :
    htmlFragments = []
    self.collectHtml(htmlFragments)
    return ' '.join(htmlFragments)

  def addKwargs(
    self,
    theId=None,
    klass=[],
    klassName=None,
    style=[],
    styleName=None,
    attrs=[],
    attrsName=None,
    hxGet=None,
    hxPost=None,
    hxTrigger=None,
    hxTarget=None,
    hxSwap=None,
    hxSwapOob=None,
    hxHeaders={},
    hyperscript=None,
    **kwargs
  ) :
    if kwargs      : self.kwargs.extend(kwargs)
    if theId       : self.theId       = theId
    if klass       : self.klass.extend(klass)
    if klassName   : self.klassName   = klassName
    if style       : self.style.extend(style)
    if styleName   : self.styleName   = styleName
    if attrs       : self.attrs.extend(attrs)
    if attrsName   : self.attrsName   = attrsName
    if hxGet       : self.hxGet       = hxGet
    if hxPost      : self.hxPost      = hxPost
    if hxTrigger   : self.hxTrigger   = hxTrigger
    if hxTarget    : self.hxTarget    = hxTarget
    if hxSwap      : self.hxSwap      = hxSwap
    if hxSwapOob   : self.hxSwapOob   = hxSwapOob
    if hxHeaders   : self.hxHeaders.extend(hxHeaders)
    if hyperscript : self.hyperscript = hyperscript

  def collectHtml(self, htmlFragments, **kwargs) :
    pass

  #################################################################
  # build HTML attributes from kwargs and theme

  def computeClass(self, classDict) :
    klass = self.klass
    if isinstance(klass, str) : klass = [ klass ]
    if self.klassName in classDict :
      klass = mergeLists(classDict[self.klassName], klass)
    if not klass : return ""
    return f'class="{' '.join(klass)}"'

  def computeStyle(self, styleDict) :
    style     = self.style
    if isinstance(style, str) : style = [ style ]
    elif isinstance(style, dict) :
      styleList = []
      for aKey, aValue in style.items() :
        styleList.append(f"{aKey}: {aValue}")
      style = styleList
    if self.styleName in styleDict :
      style = mergeLists(styleDict[self.styleName], style)
    if not style : return ""
    return f'style="{'; '.join(style)}"'

  def computeAttrs(self, attrsDict) :
    attrs     = self.attrs
    if isinstance(attrs, str) : attrs = [ attrs ]
    elif isinstance(attrs, dict) :
      attrsList = []
      for aKey, aValue in attrs.items() :
        if aValue : attrsList.append(f'{aKey}="{aValue}"')
        else: attrsList.append(aKey)
      attrs = attrsList
    if self.attrsName in attrsDict :
      attrs = mergeLists(attrsDict[self.attrsName], attrs)
    return ' '.join(attrs)

  def computeAction(self) :
    actionStr = ""
    if self.hxGet    : actionStr = f'hx-get="{self.hxGet}"'
    elif self.hxPost : actionStr = f'hx-post="{self.hxPost}"'
    return actionStr

  def computeTrigger(self) :
    triggerStr = ""
    if self.hxTrigger :
      triggerStr = f'hx-trigger="{self.hxTrigger}"'
    return triggerStr

  def computeTarget(self) :
    targetStr = ""
    if self.hxTarget :
      targetStr = f'hx-target="{self.hxTarget}"'
      if not self.hxSwap : self.hxSwap = 'outerHTML'
    if self.hxSwap :
      targetStr += f' hx-swap="{self.hxSwap}"'
    if self.hxSwapOob :
      targetStr += f' hx-swap-oob="{self.hxSwapOob}"'
    return targetStr

  def computeHeaders(self) :
    headersStr = ""
    if self.hxHeaders :
      headersStr = f"hx-headers='{json.dumps(self.hxHeaders)}'"
      print(headersStr)
    return headersStr

  def computeId(self) :
    idStr = ""
    if self.theId : idStr = f'id="{self.theId}"'
    return idStr

  def computeHyperscript(self) :
    hyperscript = ""
    if self.hyperscript : hyperscript = f'script="{self.hyperscript}"'
    return hyperscript

  def computeHtmxAttrs(self) :
    className = self.__class__.__name__
    classDict = className + 'Classes'
    if classDict not in theme : theme[classDict] = {}
    classDict = theme[classDict]
    styleDict = className + 'Styles'
    if styleDict not in theme : theme[styleDict] = {}
    styleDict = theme[styleDict]
    attrsDict = className + 'Attrs'
    if attrsDict not in theme : theme[attrsDict] = {}
    attrsDict = theme[attrsDict]

    allAttrs = [
      self.computeId(),
      self.computeAction(),
      self.computeTarget(),
      self.computeTrigger(),
      self.computeHeaders(),
      self.computeHyperscript(),
      self.computeClass(classDict),
      self.computeStyle(styleDict),
      self.computeAttrs(attrsDict)
    ]
    theAttrs = [x for x in allAttrs if x]
    return " ".join(theAttrs)

class HtmxChildrenBase(HtmxBase) :
  def __init__(
    self,
    someChildren,
    **kwargs
  ) :
    super().__init__(**kwargs)
    if not isinstance(someChildren, list) :
      someChildren = [ someChildren ]
    self.children = someChildren

  def appendAChild(self, aChild) :
    self.children.append(aChild)

  def appendChildren(self, someChildren) :
    self.children.extend(someChildren)

  def collectChildrenHtml(self, htmlFragments) :
    for aChild in self.children :
      if isinstance(aChild, str) :
        htmlFragments.append(aChild)
      elif aChild :
        aChild.collectHtml(htmlFragments)
      else:
        print(repr(self))
        print("contains a None child")
