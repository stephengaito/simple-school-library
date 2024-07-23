
from schoolLib.htmxComponents.htmx import *

class Table(HtmxChildrenBase) :
  def __init__(self, rows, **kwargs) :
    super().__init__(rows, **kwargs)

  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f"<table {self.computeHtmxAttrs()}>")
    self.collectChildrenHtml(htmlFragments)
    htmlFragments.append("</table>")

class TableRow(HtmxChildrenBase) :
  def __init__(self, columns, **kwargs) :
    super().__init__(columns, **kwargs)

  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f"<tr {self.computeHtmxAttrs()}>")
    self.collectChildrenHtml(htmlFragments)
    htmlFragments.append("</tr>")

class TableEntry(HtmxBase) :
  def __init__(self, aComponent, tableCode='td', colspan=None, **kwargs) :
    super().__init__(**kwargs)
    self.component = aComponent
    self.tableCode = tableCode
    self.colspan   = colspan

  def collectHtml(self, htmlFragments) :
    teAttrs = self.computeHtmxAttrs()
    if self.colspan : teAttrs += f' colspan="{self.colspan}"'
    htmlFragments.append(f'<{self.tableCode} {teAttrs}>')
    self.component.collectHtml(htmlFragments)
    htmlFragments.append(f"</{self.tableCode}>")

class TableHeader(TableEntry) :
  def __init__(self, aComponent, tableCode='th', colspan=None, **kwargs) :
    super().__init__(aComponent, tableCode=tableCode, colspan=colspan, **kwargs)
