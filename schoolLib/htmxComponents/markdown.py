
# import os

from markdown import markdown

# from starlette.exceptions import HTTPException

# from schoolLib.setup.configuration import config
from schoolLib.htmxComponents.htmx import HtmxBase

# def loadMarkdownFromFile(aMarkdownPath) :
#   if 'markdownDir' not in config :
#     print("Markdown directory not configured")
#     raise HTTPException(404, detail="Markdown directory not configures")
#
#   markdownDir = config['markdownDir']
#
#   markdownPath = os.path.join(markdownDir, aMarkdownPath + '.md')
#   if not os.path.isfile(markdownPath) :
#     print(f"Markdown file [{markdownPath}] not found")
#     raise HTTPException(
#       404, detail=f"Markdown file [{markdownPath}] not found"
#     )
#
#   markdownStr = ""
#   with open(markdownPath) as mdFile :
#     markdownStr = markdown(mdFile.read())
#   return markdownStr

class MarkdownDiv(HtmxBase) :
  def __init__(self, someMarkdown, **kwargs) :
    super().__init__(**kwargs)
    self.someMarkdown = someMarkdown

  def collectHtml(self, htmlFragments) :
    markdownHTML = markdown(self.someMarkdown)
    # TODO: should this be escaped?
    htmlFragments.append(f"<div {self.computeHtmxAttrs()}>")
    htmlFragments.append(markdownHTML)
    htmlFragments.append("</div>")
