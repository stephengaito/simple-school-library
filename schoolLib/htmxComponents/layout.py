
# consider: Accessible page titles in a Single Page App
# see: https://hidde.blog/accessible-page-titles-in-a-single-page-app/

from schoolLib.setup.configuration import config
from schoolLib.htmxComponents.htmx import *

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
    """)
    htmlFragments.extend(self.additionalHeaders)

class StdBody(HtmxBase) :
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

class HtmlPage(HtmxBase) :
  def __init__(self, headers, body, **kwargs) :
    super().__init__(**kwargs)
    self.headers = headers
    self.body    = body

  def collectHtml(self, htmlFragments) :
    htmlFragments.append('<!DOCTYPE html>')
    htmlFragments.append('<html lang="en"><head>')
    self.headers.collectHtml(htmlFragments)
    htmlFragments.append("</head><body><div>")
    self.body.collectHtml(htmlFragments)
    htmlFragments.append("</div></body></html>")
