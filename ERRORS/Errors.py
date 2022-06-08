from ERRORS.strignWithArrows import *

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, startPos, endPos, errorName, details):
        self.startPos = startPos
        self.endPos = endPos
        self.errorName = errorName
        self.details = details
    def printError(self):
        ret = f'{self.errorName}: {self.details}\nFile {self.startPos.fn}, line {self.startPos.ln + 1}'
        ret += '\n\n' + strWithArrows(self.startPos.ftxt, self.startPos, self.endPos)
        return ret

class IllegalCharError(Error):
    def __init__(self, startPos, endPos, details):
        super().__init__(startPos, endPos,'Illegal Character',  details)

class InvalidSyntaxError(Error):
    def __init__(self, startPos, endPos, details = ' '):
        super().__init__(startPos, endPos,'Invalid Syntax',  details)

class RunTimeError(Error):
    def __init__(self, startPos, endPos, details, context):
        super().__init__(startPos, endPos,'RunTime Error',  details)
        self.context = context
    
    # Override the error printing func to track the runtime error position using context
    def printError(self):
        ret = self.generateTraceback()
        ret += f'{self.errorName}: {self.details}'
        ret += '\n\n' + strWithArrows(self.startPos.ftxt, self.startPos, self.endPos)
        return ret

    def generateTraceback(self):
        ret = '' 
        pos = self.startPos
        cntxt  = self.context
        while cntxt:
            ret = f'   File {pos.fn}, line {str(pos.ln + 1)}, in {cntxt.displayName}\n' + ret
            pos = cntxt.parentEntryPos
            cntxt = cntxt.parent
        return 'Traceback (most recent call last):\n' + ret
