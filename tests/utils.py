
def getResponseBody(response) :
  return b"\n".join(list(response.stream)).decode('utf-8')
