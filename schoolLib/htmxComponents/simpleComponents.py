
from schoolLib.htmxComponents.htmx import *

class Div(HtmxChildrenBase) :

  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f'<div {self.computeHtmxAttrs()}>')
    self.collectChildrenHtml(htmlFragments)
    htmlFragments.append('</div>')

# we defined a set of level divs which each act as replacement points.

# The intent is that each larger number should be nested inside the lower
# numbers, so that only the dom which needs to be replaced can be
# replaced.

class Level0div(Div) :
  def __init__(self, someChildren, **kwargs) :
    if 'theId' not in kwargs : kwargs['theId'] = 'level0div'
    super().__init__(someChildren, **kwargs)

class Level1div(Div) :
  def __init__(self, someChildren, **kwargs) :
    if 'theId' not in kwargs : kwargs['theId'] = 'level1div'
    super().__init__(someChildren, **kwargs)

class Level2div(Div) :
  def __init__(self, someChildren, **kwargs) :
    if 'theId' not in kwargs : kwargs['theId'] = 'level2div'
    super().__init__(someChildren, **kwargs)

class Level3div(Div) :
  def __init__(self, someChildren, **kwargs) :
    if 'theId' not in kwargs : kwargs['theId'] = 'level3div'
    super().__init__(someChildren, **kwargs)

class Level4div(Div) :
  def __init__(self, someChildren, **kwargs) :
    if 'theId' not in kwargs : kwargs['theId'] = 'level4div'
    super().__init__(someChildren, **kwargs)

class List(HtmxChildrenBase) :
  def __init__(
    self,
    someChildren,
    listType='u',
    **kwargs
  ) :
    super().__init__(someChildren, **kwargs)
    if listType.startswith('u')  : listType = 'ul'
    else                         : listType = 'ol'
    self.listType = listType

  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f'<{self.listType} {self.computeHtmxAttrs()}>')
    for aChild in self.children :
      htmlFragments.append('<li>')
      if isinstance(aChild, str) :
        htmlFragments.append(aChild)
      else :
        aChild.collectHtml(htmlFragments)
      htmlFragments.append('</li>')
    htmlFragments.append(f'</{self.listType}>')

class Menu(HtmxChildrenBase) :
  def __init__(
    self,
    someChildren,
    selectedId=None,
    **kwargs
  ) :
    super().__init__(someChildren, **kwargs)
    self.selectedId=selectedId

  def select(self, selectedId) :
    self.selectedId=selectedId
    return self

  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f'<div {self.computeHtmxAttrs()}>')
    for aChild in self.children :
      selected = None
      if self.selectedId and aChild.theId == self.selectedId :
        selected = "selected"
      aChild.collectHtml(htmlFragments, selected=selected)
    htmlFragments.append('</div>')

class RawHtml(HtmxBase) :
  def __init__(self, rawHtml, **kwargs) :
    super().__init__(**kwargs)
    self.rawHtml = rawHtml

  def collectHtml(self, htmlFragments, **kwargs) :
    htmlFragments.append(self.rawHtml)

class Text(HtmxChildrenBase) :
  def __init__(self, someText, textType='p', **kwargs) :
    super().__init__(someText, **kwargs)
    # sanitize textType
    if not textType                : textType = None
    elif textType.startswith('pr') : textType = 'pre'
    elif textType.startswith('p')  : textType = 'p'
    elif textType.startswith('s')  : textType = 'span'
    elif textType.startswith('l')  : textType = 'label'
    elif textType.startswith('b')  : textType = 'button'
    elif textType.startswith('a')  : textType = 'a'
    elif textType.startswith('c')  : textType = 'code'
    else                           : textType = None
    self.textType = textType

  def collectHtml(self, htmlFragments, selected=None, **kwargs) :
    oldKlassName = self.klassName
    if self.textType == 'button' and selected :
      self.klassName += '-selected'
    tAttrs = self.computeHtmxAttrs()
    self.klassName = oldKlassName
    if self.textType :
      htmlFragments.append(f"<{self.textType} {tAttrs}>")
    for aChild in self.children :
      if isinstance(aChild, str) :
        htmlFragments.append(aChild)
      else :
        aChild.collectHtml(htmlFragments)
    if self.textType :
      htmlFragments.append(f"</{self.textType}>")

class Button(Text) :
  def __init__(self, text, textType='b', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class LongCode(Text) :
  def __init__(self, text, textType='pre', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class ShortCode(Text) :
  def __init__(self, text, textType='c', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class Span(Text) :
  def __init__(self, text, textType='s', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class Label(Text) :
  def __init__(self, text, textType='l', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class Link(Text) :
  def __init__(self, url, text, textType='a', target=None, **kwargs) :
    if 'attrs' not in kwargs : kwargs['attrs'] = []
    if 'hxTarget' in kwargs :
      kwargs['hxGet'] = url
    else :
      kwargs['attrs'].append(f'href="{url}"')
    if target : kwargs['attrs'].append(f'target="{target}"')
    super().__init__(text, textType=textType, **kwargs)

