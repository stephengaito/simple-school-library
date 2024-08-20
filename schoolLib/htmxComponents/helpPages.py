
from schoolLib.setup.database                  import *
from schoolLib.htmxComponents.htmx            import *
from schoolLib.htmxComponents.simpleComponents import *
from schoolLib.htmxComponents.forms            import *

class HelpModalDialog(ModalDialog) :
  # just use the ModalDialog defaults as they are!
  pass

class HelpEditorModalDialog(ModalDialog) :
  def __init__(self, modalChildren, **kwargs) :
    kwargs['modalType']             = 'Editor'
    kwargs['additionalHyperscript'] = "call tinymce.activeEditor.destroy()"
    kwargs['underlayDismisses']     = False
    super().__init__(modalChildren, **kwargs)

class HelpPage(RawHtml) :
  def __init__(self, helpPageHtml, helpPagePath, isAdmin=False, **kwargs) :
    super().__init__(helpPageHtml, **kwargs)
    self.helpPagePath = helpPagePath
    self.isAdmin      = isAdmin

  def collectHtml(self, htmlFragments, **kwargs) :
    if self.isAdmin :
      EditorButton(
        hxGet=f"/editHelp/{self.helpPagePath}"
      ).collectHtml(htmlFragments)
    htmlFragments.append(f'<div {self.computeHtmxAttrs()}>')
    htmlFragments.append(self.rawHtml)
    htmlFragments.append('</div>')

class HelpEditor(TextAreaInput) :
  def __init__(self, hxPost=None, **kwargs) :
    kwargs['theId'] = 'helpEditor'
    self.hxPost = hxPost
    super().__init__(**kwargs)

  def collectHtml(self, htmlFragments) :
    super().collectHtml(htmlFragments)
    htmlFragments.append("""
    <script>
      tinymce.init({
        selector: 'textarea#helpEditor',
        license_key: 'gpl',
        promotion: false,
        browser_spellcheck: true,
        plugins: 'advlist autolink link image lists charmap preview'
      });
    </script>
    """)

class HelpEditorForm(Form) :
  def __init__(self, helpPageHtml, helpPagePath, hxPost, **kwargs) :
    super().__init__([], submitMsg="Save changes", hxPost=hxPost, **kwargs)
    self.appendChild(Label(f'Help page for {helpPagePath}'))
    self.appendChild(HelpEditor(
      value=helpPageHtml,
      placeholder=f'Add some text for {helpPagePath}',
      name='helpContent'
    ))
    self.appendChild(CancelButton(
      "Cancel",
      hyperscript="on click trigger closeEditorModal"
    ))

def getHelpPage(pageData, helpPagePath, modal=True, hxPost=None, **kwargs) :
  helpPageHtml = getHelpPageHtml(pageData.db, helpPagePath)
  if not helpPageHtml :
    if not pageData.user.is_authenticated :
      helpPageHtml = f"<p>Please ask the administrator to add this help page ({helpPagePath})</p>"
    elif not hxPost :
      helpPageHtml = f"<p>No hxPost supplied for {helpPagePath}</p>"
    else :
      return HelpEditorModalDialog([
        HelpEditorForm(
          helpPageHtml, helpPagePath, hxPost,
          buttonHyperscript="on click trigger closeEditorModal",
          **kwargs
        )
      ])

  helpComponent = HelpPage(
      helpPageHtml, helpPagePath,
      isAdmin=pageData.user.is_authenticated,
      **kwargs
    )
  if modal : helpComponent = HelpModalDialog([ helpComponent ])
  return helpComponent

def postHelpPage(pageData, helpPagePath, **kwargs) :
  print(f"postHepPage[helpPagePath]: [{helpPagePath}]")
  theForm = pageData.form
  selectSql = SelectSql(
  ).fields('content'
  ).tables('helpPages'
  ).whereValue('path', helpPagePath)
  results = selectSql.parseResults(
    pageData.db.execute(selectSql.sql()),
    fetchAll=False
  )
  if results :
    pageData.db.execute(UpdateSql(
    ).whereValue('path', helpPagePath
    ).sql('helpPages', {
      'content' : theForm['helpContent']
    }))
  else :
    pageData.db.execute(*InsertSql().sql('helpPages', {
      'path'    : helpPagePath,
      'content' : theForm['helpContent']
    }))
  pageData.db.commit()
  return getHelpPage(pageData, helpPagePath, **kwargs)
