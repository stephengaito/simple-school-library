
###############################################################
# School Library Exceptions

class SLException(Exception) :
  def __init__(self, message, errType, helpMessage=None, origErr=None) :
    self.slMessage = message
    self.slErrType = errType
    self.slHelpMsg = helpMessage
    self.slOrigErr = origErr
