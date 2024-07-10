
from schoolLib.htmxComponents.utils import *

buttonClasses = {}
buttonStyles  = {}
buttonAttrs   = {}

def button(
  theId="", text="", image="", get="",
  className=None, klass=[],
  styleName=None, style={},
  attrsName=None, attrs={},
  **kwargs
) :
  print("---------------------------")
  theId  = computeId(theId)
  print(theId)
  getStr = computeGet(get)
  print(getStr)
  klass  = computeClass(className, buttonClasses, klass)
  print(klass)
  style  = computeStyle(styleName, buttonStyles, style)
  print(style)
  attrs  = computeAttrs(attrsName, buttonAttrs, attrs)
  print(attrs)
  return f"<button {theId} {getStr} {klass} {style} {attrs}>{text}</button>"


def menu(menuList, selected=0,
  theId="", get="",
  className=None, klass=[],
  styleName=None, style={},
  attrsName=None, attrs={},
  **kwargs
):
  theId  = computeId(theId)
  getStr = computeGet(get)
  klass  = computeClass(className, buttonClasses, klass)
  style  = computeStyle(styleName, buttonStyles, style)
  attrs  = computeAttrs(attrsName, buttonAttrs, attrs)

  menuList = selectComponentInList(selected, menuList, 'class', 'selected')
  menuListHtml = [ f'<div {theId} {getStr} {klass} {style} {attrs}>' ]
  for anItem in menuList :
    menuListHtml.append(computeComponent(anItem))
  menuListHtml.append('</div>')
  return '\n'.join(menuListHtml)
