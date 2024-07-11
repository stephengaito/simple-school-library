
# consider: Accessible page titles in a Single Page App
# see: https://hidde.blog/accessible-page-titles-in-a-single-page-app/

from schoolLib.setup.configuration import config
from schoolLib.htmxComponents.utils import *

topLevelMenu = [
  { 'component' : 'button',
    'text' : 'Home',
    'get' : '/menu/home',
    'attrs' : {
      'hx-target' : '#level0div',
      'hx-swap'   : 'outerHTML'
    }
  },
  { 'component' : 'button',
    'text' : 'Books',
    'get' : "/menu/books",
    'attrs' : {
      'hx-target' : '#level0div',
      'hx-swap'   : 'outerHTML'
    }
  },
  { 'component' : 'button',
    'text' : 'People',
    'get' : '/menu/people',
    'attrs' : {
      'hx-target' : '#level0div',
      'hx-swap'   : 'outerHTML'
    }
  },
  { 'component' : 'button',
    'text' : 'Tasks',
    'get' : '/menu/tasks',
    'attrs' : {
      'hx-target' : '#level0div',
      'hx-swap'   : 'outerHTML'
    }
  }
]

def stdHeaders() :
  title = "Simple School Library"
  if 'title' in config : title = config['title']

  return f"""
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>

  <link rel="apple-touch-icon" sizes="192x192" href="/static/favicon/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon/favicon-16x16.png">
  <link rel="manifest" href="/static/favicon/site.webmanifest">

  <!-- link rel="stylesheet" href="/static/css/main.css" type="text/css" / -->

  <script src="/static/js/htmx.min.js"></script>
  """

def stdBody() :
  return """
  <div
    id="initialOuterDiv"
    hx-get="/menu/home"
    hx-trigger="load delay:100ms"
    hx-target="#initialOuterDiv"
    hx-swap="outerHTML"
  ></div>
  """

def htmlPage(headers, body) :
  headers = computeComponent(headers)
  body    = computeComponent(body)
  return f"""
<!DOCTYPE html>
<html lang="en">
<head>
{headers}
</head>
<body>
{body}
</body>
</html>
  """