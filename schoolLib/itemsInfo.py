"""
Work with itemsInfo

    - create a new itemsInfo
    - edit a new itemsInfo

"""

from schoolLib.setup import *

@get('/itemsInfo/new')
def getNewItemsInfoForm(request) :
  pass

@post('/itemsInfo/new')
async def postSaveNewItemsInfo(request) :
  pass

@get('/itemsInfo/edit/{itemsInfoId:int}')
def getEditAnItemsInfoForm(request, itemsInfoId=None) :
  pass

@put('/itemsInfo/edit/{itemsInfoId:int}')
async def putUpdateAnItemsInfo(request, itemsInfoId=None) :
  pass
