
from schoolLib.setup import pagePart, getRoute, registerHomePage, \
  getHelpPageHtml, postRoute
from schoolLib.htmxComponents import Menu, Level0div, Level1div,  \
  getHelpPage, HtmlPage, StdHeaders, StdBody, InitialOuterDiv,    \
  HelpEditorModalDialog, HelpEditorForm, postHelpPage
import schoolLib.app.menus

##########################################################################
# content

@pagePart
def secondLevelHomeMenu(pageData, selectedId=None, **kwargs) :
  return Menu([], selectedId=selectedId, klassName='vertical')

@pagePart
def getHomeMenu(pageData, **kwargs) :
  return Level0div([
    schoolLib.app.menus.topLevelMenu(pageData, selectedId='home'),
    Level1div([
      secondLevelHomeMenu(pageData),
      getHelpPage(
        pageData, 'homePage', modal=False,
        hxPost='/editHelp/homePage/nonModal'
      )
    ])
  ], theId='level0div')

##########################################################################
# routes

getRoute('/menu/home', getHomeMenu, anyUser=True)

registerHomePage(getHomeMenu)

@pagePart
def homePage(pageData, **kwargs):
  """ The Home Page """
  return HtmlPage(
    StdHeaders(),
    StdBody(InitialOuterDiv())
  )

getRoute('/', homePage, anyUser=True)

@pagePart
def helpPages(pageData, aHelpPage=None, isModal='yes', **kwargs) :
  if not aHelpPage :
    aHelpPage = 'uknownPage'
  print(f"HelpPages: [{aHelpPage}]")
  print(f"isModal: [{isModal}]")
  modal = True
  modalStr = 'modal'
  if isModal.startswith('no') :
    modal = False
    modalStr = 'nonModal'
  print(f"modalStr: [{modalStr}]")
  return getHelpPage(
    pageData, aHelpPage,
    hxPost=f'/editHelp/{aHelpPage}/{modalStr}',
    modal=modal
  )

getRoute('/help/{aHelpPage:str}/{isModal:str}', helpPages, anyUser=True)

@pagePart
def editHelpPage(pageData, aHelpPage=None, isModal='yes', **kwargs) :
  if not aHelpPage :
    aHelpPage = 'unknownPage'
  helpPageHtml = getHelpPageHtml(pageData.db, aHelpPage)
  print(helpPageHtml)
  modal = True
  modalStr = 'modal'
  if isModal.startswith('no') :
    modal = False
    modalStr = 'nonModal'
  # see: https://stackoverflow.com/a/33794114
  return HelpEditorModalDialog([
    HelpEditorForm(
      helpPageHtml, aHelpPage,
      f'/editHelp/{aHelpPage}/{modalStr}',
      hxTarget='#helpPage',
      hxSwap='outerHTML',
      modal=modal
    )
  ])

getRoute('/editHelp/{aHelpPage:str}/{isModal:str}', editHelpPage)

@pagePart
def postHelpPages(pageData, aHelpPage=None, isModal='yes', **kwargs) :
  if not aHelpPage :
    aHelpPage = 'unknownPage'
  modal = True
  modalStr = 'modal'
  if isModal.startswith('no') :
    modal = False
    modalStr = 'nonModal'
  return postHelpPage(
    pageData, aHelpPage, modal=modal,
    hxPost=f'/editHelp/{aHelpPage}/{modalStr}',
    **kwargs
  )

postRoute('/editHelp/{aHelpPage:str}/{isModal:str}', postHelpPages)

