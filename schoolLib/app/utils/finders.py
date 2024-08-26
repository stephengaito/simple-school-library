
import yaml
from schoolLib.setup import *
from schoolLib.htmxComponents import *

import schoolLib

##########################################################################
# generic finder (get front end)

@pagePart
def findAThing(
  pageData, probe=None, thingRows=[],
  theId='level2div', hxPost='/search/borrowers',
  helpName='findBorrower', placeHolder="Type a person's name",
  **kwargs
) :
  hxTarget = '#'+theId
  return Div([
    SearchBox(
      hxPost=hxPost,
      name='search',
      helpName=helpName,
      value=probe,
      placeholder=placeHolder,
      hxTarget=hxTarget
    ),
    Table(thingRows, theId='searchResults')
  ], theId=theId, attrs={'hx-ext':'morph'})

##########################################################################
# generic search results HTMX (post back end)

@pagePart
def searchForThings(
  pageData, thingsIterClass,
  hxTarget='#level1div', targetUrl='/borrowers/show',
  theId='level2div', hxPost='/search/borrowers',
  helpName='findBorrower', placeHolder="Type a person's name",
  **kwargs
) :
  theForm = pageData.form
  thingsIter = thingsIterClass(targetUrl, theForm, pageData.db)

  linkHyperscript=None
  if thingsIter.numResults == 1 :
    linkHyperscript = "init wait 250ms then trigger click on me"

  thingRows =[]
  for linkUrl, linkText in thingsIter :
    thingRows.append(TableRow(TableEntry(Link(
      linkUrl, linkText,
      hyperscript=linkHyperscript,
      hxTarget=hxTarget
    ))))
  return schoolLib.app.utils.finders.findAThing(
    pageData,
    probe=theForm['search'], thingRows=thingRows,
    theId=theId, hxPost=hxPost,
    helpName=helpName, placeHolder=placeHolder,
    **kwargs
  )

##########################################################################
# generic iterator (class)

class SearchIter(object) :

  def __init__(self, results, targetUrl) :
    self.results = results
    self.targetUrl = targetUrl
    self.numResults = len(results)
    self.curIter = 0

  def __iter__(self) :
    return self

  def __next__(self) :
    return self.next()

  def nextRow(self) :
    if self.numResults <= self.curIter : raise StopIteration()
    curRow = self.results[self.curIter]
    self.curIter += 1
    return curRow
