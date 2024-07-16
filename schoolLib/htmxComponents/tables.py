
from schoolLib.htmxComponents.utils import *

def table(rows, **kwargs) :
  tAttrs = computeHtmxAttrs(
    'tableClasses', 'tableStyles', 'tableAttrs', kwargs
  )
  rowHtml = []
  for aRow in rows :
    rowHtml.append(computeComponent(aRow))
  rowHtml = '\n'.join(rowHtml)
  return f"""
    <table {tAttrs}>
    {rowHtml}
    </table>
  """

def tableRow(columns, **kwargs) :
  trAttrs = computeHtmxAttrs(
    'tableRowClasses', 'tableRowStyles', 'tableRowAttrs', kwargs
  )
  columnHtml = []
  for aColumn in columns :
    columnHtml.append(computeComponent(aColumn))
  columnHtml = '\n'.join(columnHtml)
  return f"""
    <tr {trAttrs}>
    {columnHtml}
    </tr>
  """

def tableEntry(aComponent, tableCode='td', colspan=None, **kwargs) :
  teAttrs = computeHtmxAttrs(
    'tableEntryClasses', 'tableEntryStyles', 'tableEntryAttrs', kwargs
  )
  if colspan :
    teAttrs += f' colspan="{colspan}"'
  entryHtml = computeComponent(aComponent)
  return f"""
    <{tableCode} {teAttrs}>
    {entryHtml}
    </{tableCode}>
  """

def tableHeader(aComponent, **kwargs) :
  return tableEntry(aComponent, tableCode='th', **kwargs)
