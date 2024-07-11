
import os

from markdown import markdown

from starlette.exceptions import HTTPException

from schoolLib.setup.configuration import config
from schoolLib.htmxComponents.utils import *

def loadMarkdownFromFile(aMarkdownPath) :
  if 'markdownDir' not in config :
    print("Markdown directory not configured")
    raise HTTPException(404, detail="Markdown direcotry not configures")

  markdownDir = config['markdownDir']

  markdownPath = os.path.join(markdownDir, aMarkdownPath+'.md')
  if not os.path.isfile(markdownPath) :
    print(f"Markdown file [{markdownPath}] not found")
    raise HTTPException(404, detail=f"Markdown file [{markdownPath}] not found")

  markdownStr = ""
  with open(markdownPath) as mdFile :
    markdownStr = markdown(mdFile.read())
  return markdownStr

markdownClasses = {}
markdownStyles  = {}
markdownAttrs   = {}

def markdownDiv(someMarkdown, **kwargs) :
  htmxAttrs = computeHtmxAttrs(kwargs)

  markdownHTML = markdown(someMarkdown)
  # TODO: should this be escaped?

  return f"""
  <div {htmxAttrs}>
  {markdownHTML}
  </div>
  """
