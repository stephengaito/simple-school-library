
##############################################
# We need to test the following pageParts:
#
#  'app.home.home.editHelpPage',  # (1)  (DONE)
#
#  'app.home.home.helpPages',  # (1)   (DONE)
#
#  'app.home.home.postHelpPages',  # (1) (DONE)

import yaml

# import pytest

import schoolLib

from schoolLib.htmxComponents import HelpPage, \
  HelpModalDialog, HelpEditorModalDialog, HelpEditorForm, \
  HelpEditor, Label, CancelButton, Button

from tests.utils.utils import MockPageData, getMockPageDataFrom

def test_helpPages_nonModal(database, addSomeHelpPages) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.home.home.helpPages(
    pageData, aHelpPage='helpPage1', isModal='no'
  )

  print(yaml.dump(htmx))

  assert htmx.isA(HelpPage)
  assert htmx.helpPagePath == 'helpPage1'
  assert htmx.rawHtml == 'This is the help for page 1'
  assert htmx.modal is False


def test_helpPages_modal(database, addSomeHelpPages) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.home.home.helpPages(
    pageData, aHelpPage='helpPage1', isModal='yes'
  )

  print(yaml.dump(htmx))

  assert htmx.isA(HelpModalDialog)
  assert len(htmx.children) == 1
  helpPage = htmx.children[0]

  assert helpPage.isA(HelpPage)
  assert helpPage.helpPagePath == 'helpPage1'
  assert helpPage.rawHtml == 'This is the help for page 1'
  assert helpPage.modal is True


def test_postHelpPages_nonModal(database, addSomeHelpPages) :
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      helpContent: This is the help for page 3
  """)

  htmx = schoolLib.app.home.home.postHelpPages(
    pageData, aHelpPage='helpPage3', isModal='no'
  )

  print(yaml.dump(htmx))

  assert htmx.isA(HelpPage)
  assert htmx.helpPagePath == 'helpPage3'
  assert htmx.rawHtml == 'This is the help for page 3'
  assert htmx.modal is False

def test_postHelpPages_modal(database, addSomeHelpPages) :
  pageData = getMockPageDataFrom(database, """
    authenticated: True
    theForm:
      helpContent: This is the help for page 3
  """)

  htmx = schoolLib.app.home.home.postHelpPages(
    pageData, aHelpPage='helpPage3', isModal='yes'
  )

  print(yaml.dump(htmx))

  assert htmx.isA(HelpModalDialog)
  assert len(htmx.children) == 1
  helpPage = htmx.children[0]

  assert helpPage.isA(HelpPage)
  assert helpPage.helpPagePath == 'helpPage3'
  assert helpPage.rawHtml == 'This is the help for page 3'
  assert helpPage.modal is True

def test_editHelpPage_modal(database, addSomeHelpPages) :
  pageData = MockPageData(database)
  htmx = schoolLib.app.home.home.editHelpPage(
    pageData, aHelpPage='helpPage1', isModal='yes'
  )

  print(yaml.dump(htmx))

  assert htmx.isA(HelpEditorModalDialog)
  assert len(htmx.children) == 1
  helpEditor = htmx.children[0]

  assert helpEditor.isA(HelpEditorForm)
  assert len(helpEditor.children) == 3
  assert helpEditor.children[0].isA(Label)
  assert helpEditor.children[0].children[0] == 'Help page for helpPage1'

  assert helpEditor.children[1].isA(HelpEditor)
  assert helpEditor.children[1].taValue == 'This is the help for page 1'

  assert helpEditor.children[2].isA(CancelButton)
  assert helpEditor.children[2].children[0] == 'Cancel'

  assert helpEditor.hxPost == '/editHelp/helpPage1/modal'
  assert helpEditor.submitButton.isA(Button)
  assert helpEditor.submitButton.children[0] == 'Save changes'

