from CONSTANTS.Constants import *
from ERRORS.Errors import *

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def next(self, currentChar = None):
        self.idx += 1
        self.col += 1
        if currentChar == '\n':
            self.ln += 1
            self.col = 0
        return self
        
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKEN
#######################################

class Token: 
    def __init__(self, type, value = None, startPos = None, endPos = None):
        self.type = type
        self.value = value
        if startPos:
            self.startPos = startPos.copy()
            self.endPos = startPos.copy()
            self.endPos.next()
        if endPos:
            self.endPos = endPos
    # check if the current token is identifier/keyword (say)
    def isIdentifier(self):
        return self.type == KEYWORD and self.value == KEYWORDS

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fileName, statemnt):
        self.fn = fileName
        self.text = statemnt
        self.currChar = None
        self.pos = Position(-1, 0, -1, fileName, statemnt)
        self.next()

    def next(self):
        self.pos.next(self.currChar)
        self.currChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def createTokens(self):
        tokens = []
        while self.currChar != None:
            if self.currChar == ' ':
                self.next()

            elif self.currChar == '+':
                tokens.append(Token(PLUS, startPos= self.pos))
                self.next()

            elif self.currChar == '-':
                tokens.append(Token(MINUS, startPos= self.pos))
                self.next()

            elif self.currChar == '*':
                tokens.append(Token(MUL, startPos= self.pos))
                self.next()

            elif self.currChar == '/':
                tokens.append(Token(DIV, startPos= self.pos))
                self.next()

            elif self.currChar == '(':
                tokens.append(Token(LPAREN, startPos= self.pos))
                self.next()

            elif self.currChar == ')':
                tokens.append(Token(RPAREN, startPos= self.pos))
                self.next()

            elif self.currChar == '^':
                tokens.append(Token(POW, startPos=self.pos))
                self.next()

            elif self.currChar == '&':
                tokens.append(Token(AND, startPos=self.pos))
                self.next()

            elif self.currChar == '|':
                tokens.append(Token(OR, startPos=self.pos))
                self.next()

            elif self.currChar == '=':
                tokens.append(Token(EQUAL, startPos=self.pos))
                self.next()

            elif self.currChar in DIGITS:
                tokens.append(self.getNumber())

            elif self.currChar in LETTERS:
                tokens.append(self.getIdentifier())

            else:
                posStart = self.pos.copy()
                char = self.currChar
                self.next()
                return [], IllegalCharError(posStart, self.pos, "'" + char + "'")

        tokens.append(Token(EOF, startPos=self.pos))
        return tokens, None

    def getNumber(self):
        retNum = ''
        hasDot = False
        startPos = self.pos.copy()
        while self.currChar != None and self.currChar in DIGITS + '.':
            if self.currChar == '.':
                if hasDot: break
                hasDot = True
            retNum += self.currChar
            self.next()
        if hasDot: return Token(FLOAT, float(retNum), startPos, self.pos)
        return Token(INT, int(retNum), startPos, self.pos)
    
    def getIdentifier(self):
        retId = ''
        startPos = self.pos.copy()
        while self.currChar != None and self.currChar in LETTERS_DIGITS + '_':
            retId += self.currChar
            self.next()
        tokenType = KEYWORD if retId == KEYWORDS else IDENTIFIER
        return Token(tokenType, retId, startPos, self.pos)
