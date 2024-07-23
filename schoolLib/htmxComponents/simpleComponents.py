
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

class Menu(HtmxChildrenBase) :
  def __init__(
    self,
    someChildren,
    selectedId=None,
    target='#level0div',
    swap='outerHTML',
    **kwargs
  ) :
    super().__init__(someChildren, **kwargs)
    self.childKWArgs = {
      'target' : target,
      'swap'   : swap
    }
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
      aChild.collectHtml(
        htmlFragments, selected=selected, **self.childKWArgs
      )
    htmlFragments.append('</div>')

class Text(HtmxBase) :
  def __init__(self, text, textType='p', **kwargs) :
    super().__init__(**kwargs)
    self.text     = text
    # sanitize textType
    if textType.startswith('p')   : textType = 'p'
    elif textType.startswith('s') : textType = 'span'
    elif textType.startswith('l') : textType = 'label'
    elif textType.startswith('b') : textType = 'button'
    elif textType.startswith('a') : textType = 'a'
    else                          : textType = 'div'
    self.textType = textType

  def collectHtml(self, htmlFragments, selected=None, **kwargs) :
    oldKlassName = self.klassName
    if self.textType == 'button' and selected :
      self.klassName += '-selected'
    tAttrs = self.computeHtmxAttrs()
    self.klassName = oldKlassName
    htmlFragments.append(
      f"<{self.textType} {tAttrs}>{self.text}</{self.textType}>"
    )

class Button(Text) :
  def __init__(self, text, textType='b', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class Span(Text) :
  def __init__(self, text, textType='s', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class Label(Text) :
  def __init__(self, text, textType='l', **kwargs) :
    super().__init__(text, textType=textType, **kwargs)

class Link(Text) :
  def __init__(self, url, text, textType='a', **kwargs) :
    # PUT url into kwargs...
    super().__init__(text, textType=textType, **kwargs)
