
# consider: Accessible page titles in a Single Page App
# see: https://hidde.blog/accessible-page-titles-in-a-single-page-app/

from schoolLib.setup.configuration import config
from schoolLib.htmxComponents.htmx import HtmxBase, theme

class StdHeaders(HtmxBase) :
  def __init__(self, additionalHeaders=[], **kwargs) :
    super().__init__(**kwargs)
    if not isinstance(additionalHeaders, list) :
      additionalHeaders = [ additionalHeaders ]
    self.additionalHeaders = additionalHeaders

  def collectHtml(self, htmlFragments) :

    title = "Simple School Library"
    if 'title' in config : title = config['title']

    htmlFragments.append(f"""
      <meta charset="utf-8">
      <title>{title}</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>

      <link rel="apple-touch-icon" sizes="192x192" href="/static/favicon/apple-touch-icon.png">
      <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon/favicon-32x32.png">
      <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon/favicon-16x16.png">
      <link rel="manifest" href="/static/favicon/site.webmanifest">

      <link rel="stylesheet" href="/static/css/main.css" type="text/css" />

      <script src="/static/tinymce/js/tinymce/tinymce.min.js" referrerpolicy="origin"></script>
      <script src="/static/js/htmx.min.js"></script>
      <script src="/static/js/idiomorph-ext.min.js"></script>
      <script src="/static/js/hyperscript.min.js"></script>
    """)  # noqa
    htmlFragments.extend(self.additionalHeaders)

class InitialOuterDiv(HtmxBase) :
  def collectHtml(self, htmlFragments) :
    htmlFragments.append("""
      <div
        id="initialOuterDiv"
        hx-get="/menu/home"
        hx-trigger="load delay:100ms"
        hx-target="#initialOuterDiv"
        hx-swap="outerHTML"
      ></div>
    """)

class RefreshContent(HtmxBase) :
  def __init__(self, content, **kwargs) :
    super().__init__(**kwargs)
    if not isinstance(content, list) :
      self.content = [ content ]
    else :
      self.content  = content

  def collectHtml(self, htmlFragments) :
    htmlFragments.append('<section id="content" class="w-4/5 flex-none" >')
    if self.content :
      for anItem in self.content :
        anItem.collectHtml(htmlFragments)
    htmlFragments.append('</section>')

class RefreshSubContent(RefreshContent) :
  def __init__(self, subMenu, content, **kwargs) :
    super().__init__(content, **kwargs)
    self.subMenu  = subMenu

  def collectHtml(self, htmlFragments) :
    htmlFragments.append('<div id="subContent" class="flex flex-row">')

    htmlFragments.append('<asside id="subMenu" class="w-1/5 flex-none" >')
    if self.subMenu :
      self.subMenu.collectHtml(htmlFragments)
    htmlFragments.append('</asside>')

    super().collectHtml(htmlFragments)

    htmlFragments.append('</div>')

class RefreshMainContent(RefreshSubContent) :
  def __init__(self, mainMenu, subMenu, content, message=None, **kwargs) :
    super().__init__(subMenu, content, **kwargs)
    self.mainMenu = mainMenu
    self.message = message

  def collectHtml(self, htmlFragments) :
    htmlFragments.append('<main id="mainContent">')

    htmlFragments.append('<nav id="mainMenu" >')
    if self.mainMenu :
      self.mainMenu.collectHtml(htmlFragments)
    htmlFragments.append('</nav>')

    super().collectHtml(htmlFragments)

    if self.message :
      footerMessageDelay = "5s"
      if theme and 'footerMessageDelay' in theme :
        footerMessageDelay = theme['footerMessageDelay']
      htmlFragments.append(f"""
        <footer id="footerMessages" class="fixed bottom-0 w-screen"
         script="init wait {footerMessageDelay} then remove me"
        >
      """)
      self.message.collectHtml(htmlFragments)
      htmlFragments.append('</footer>')

    htmlFragments.append('</main>')

  def addMessage(self, messageHtmx) :
    self.message = messageHtmx
    return self

class StdBody(HtmxBase) :
  def __init__(self, htmxComponent, url='/', **kwargs) :
    super().__init__(**kwargs)
    self.htmxComponent = htmxComponent
    self.url           = url

  def collectHtml(self, htmlFragments) :
    htmlFragments.append("""
      <header id="header" > </header>
    """)
    self.htmxComponent.collectHtml(htmlFragments)
    htmlFragments.append("""
    """)
    if 'develop' in config :
      htmlFragments.append(f"""
        <div id="developerMessages" class="fixed bottom-0 w-screen">
          <a href="/routes{self.url}" target="_blank">/routes{self.url}</a>
          <a href="/uiOverview" target="_blank">/uiOverview{self.url}</a>
        </div>
      """)

class HtmlPage(HtmxBase) :
  def __init__(self, headers, body, **kwargs) :
    super().__init__(**kwargs)
    self.headers = headers
    self.body    = body

  def collectHtml(self, htmlFragments) :
    htmlFragments.append('<!DOCTYPE html>')
    htmlFragments.append('<html lang="en"><head>')
    self.headers.collectHtml(htmlFragments)
    htmlFragments.append('</head><body>')
    self.body.collectHtml(htmlFragments)
    htmlFragments.append('</body></html>')
