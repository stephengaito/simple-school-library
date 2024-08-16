
from schoolLib.setup.database                  import *
from schoolLib.htmxComponents.simpleComponents import *
from schoolLib.htmxComponents.forms            import *

class HelpPage(RawHtml) :
  def collectHtml(self, htmlFragments, **kwargs) :
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
      tinymce.init([
        selector: 'textarea#helpEditor',
        browser_spellcheck: true,
        plugins: ''advlist autolink link image lists charmap preview''
      ]);
    </script>
    """)

def getHelpPage(pageData, helpPagePath, hxPost=None, **kwargs) :
  helpPageHtml = getHelpPageHtml(pageData.db, helpPagePath)
  if not helpPageHtml :
    if not pageData.user.is_authenticated :
      helpPageHtml = f"<p>Please ask the administrator to add this help page ({helpPagePath})</p>"
    elif not hxPost :
      helpPageHtml = f"<p>No hxPost supplied for {helpPagePath}</p>"
    else :
      return Form([
        Label(f'Help page for {helpPagePath}'),
        HelpEditor(name='helpContent', **kwargs)
      ], hxPost=hxPost, submitMsg="Save changes")

  return HelpPage(helpPageHtml, **kwargs)

async def postHelpPage(pageData, helpPagePath, **kwargs) :
  theForm = pageData.form
  selectSql = SelectSql(
  ).fields('content'
  ).tables('helpPages'
  ).whereValue('path', helpPagePath)
  results = selectSql.parseResults(
    db.execute(selectSql.sql()),
    fetchAll=False
  )
  if results :
    db.execute(UpdateSql(
    ).whereValue('path', helpPagePath
    ).sql('helpPages', {
      'content' : theForm['content']
    }))
  else :
    db.execute(InsertSql().sql('helpPages', {
      'path'    : helpPagePath,
      'content' : theForm['content']
    }))
  db.commit()
  return getHelpPage(pageData, helpPagePath, **kwargs)
