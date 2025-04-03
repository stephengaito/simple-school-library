
from schoolLib.htmxComponents.htmx import HtmxBase, HtmxChildrenBase

class Table(HtmxChildrenBase) :
  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f"<table {self.computeHtmxAttrs()}>")
    self.collectChildrenHtml(htmlFragments)
    htmlFragments.append("</table>")

  def needsTemplate(self) :
    return True

class TableHead(HtmxChildrenBase) :
  def __init__(self, rows, tablePart='thead', **kwargs) :
    super().__init__(rows, **kwargs)
    self.tablePart = tablePart

  def needsTemplate(self) :
    return True

  def collectHtml(self, htmlFragments) :
    htmlFragments.append(f"<{self.tablePart} {self.computeHtmxAttrs()}>")
    self.collectChildrenHtml(htmlFragments)
    htmlFragments.append(f"</{self.tablePart}>")

class TableBody(TableHead) :
  def __init__(self, rows, tablePart='tbody', **kwargs) :
    super().__init__(rows, tablePart=tablePart, **kwargs)

class TableFoot(TableHead) :
  def __init__(self, rows, tablePart='tfoot', **kwargs) :
    super().__init__(rows, tablePart=tablePart, **kwargs)

class TableRow(HtmxChildrenBase) :
  def needsTemplate(self) :
    return True

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

  def needsTemplate(self) :
    return True

  def collectHtml(self, htmlFragments) :
    teAttrs = self.computeHtmxAttrs()
    if self.colspan : teAttrs += f' colspan="{self.colspan}"'
    htmlFragments.append(f'<{self.tableCode} {teAttrs}>')
    self.component.collectHtml(htmlFragments)
    htmlFragments.append(f"</{self.tableCode}>")

class TableHeader(TableEntry) :
  def __init__(self, aComponent, tableCode='th', colspan=None, **kwargs) :
    super().__init__(
      aComponent, tableCode=tableCode, colspan=colspan, **kwargs
    )
