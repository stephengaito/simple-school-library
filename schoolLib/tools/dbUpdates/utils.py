

knownDbVersions = {}

def addDbVersion(aVersionId, updateFunc) :
  knownDbVersions[aVersionId] = updateFunc

