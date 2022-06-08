from NODES.Nodes import *
from ERRORS.Errors import *
from CONSTANTS.Constants import *
#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.nextCount = 0

    def registerNext(self):
        self.nextCount += 1

    def register(self, res):
        self.nextCount += res.nextCount
        if res.error: self.error = res.error
        return res.node 

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.nextCount == 0:      
            self.error = error
        return self


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenidx = -1
        self.currToken = None
        self.next()

    def next(self):
        self.tokenidx += 1
        if self.tokenidx < len(self.tokens):
            self.currToken = self.tokens[self.tokenidx]
        return self.currToken

    def parse(self):
        ret = self.expr()
        if not ret.error and self.currToken.type != EOF:
            return ret.failure(InvalidSyntaxError(self.currToken.startPos, self.currToken.endPos, "Expected '+', '-', '*', '/', '^', '&' or '|'"))
        return ret
    
    def atom(self):
        res = ParseResult()
        token = self.currToken

        if token.type in (INT, FLOAT):
            res.registerNext()
            self.next()
            return res.success(NumberNode(token))
        
        elif token.type == IDENTIFIER:
            res.registerNext()
            self.next()
            return res.success(VariableAccessNode(token))

        elif token.type == LPAREN:
            res.registerNext()
            self.next()
            exp = res.register(self.expr())
            if res.error: return res
            if self.currToken.type == RPAREN:
                res.registerNext()
                self.next()
                return res.success(exp)
            else: return res.failure(InvalidSyntaxError(self.currToken.startPos, self.currToken.endPos, "Expected ')'"))
        return res.failure(InvalidSyntaxError(token.startPos, token.endPos, "Expected INT, FLOAT, variable, '+', '-' or '('"))
    
    def advancedOP(self):
        return self.binaryOp(self.atom, (POW, AND, OR), self.factor)

    def factor(self):
        res = ParseResult()
        token = self.currToken

        if token.type in (PLUS, MINUS):
            res.registerNext()
            self.next()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        return self.advancedOP()


    def term(self):
        return self.binaryOp(self.factor, (MUL, DIV))

    def expr(self):
        res = ParseResult()
        if self.currToken.isIdentifier():
            res.registerNext()
            self.next()

            if self.currToken.type != IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.currToken.startPos, self.currToken.endPos, 'Expected Identifier'))
            variableName = self.currToken
            res.registerNext()
            self.next()
            
            if self.currToken.type != EQUAL:
                return res.failure(InvalidSyntaxError(self.currToken.startPos, self.currToken.endPos, "Expected '='"))
            res.registerNext()
            self.next()

            exp = res.register(self.expr())
            if res.error: return res
            return res.success(VariableAssignNode(variableName, exp))   

        node = res.register(self.binaryOp(self.term, (PLUS, MINUS)))
        if res.error:
            return res.failure(InvalidSyntaxError(self.currToken.startPos, self.currToken.endPos, 
            "Expected 'say', INT, FLOAT, variable, '+', '-' or '('"))


        return res.success(node)


    def binaryOp(self, leftFunc, ops, rightFunc = None):
        if not rightFunc: rightFunc = leftFunc

        res = ParseResult()
        left = res.register(leftFunc())

        if res.error: return res
        while self.currToken.type in ops:
            opToken = self.currToken
            res.registerNext()
            self.next()
            right = res.register(rightFunc())
            if res.error: return res
            left = BinaryOpNode(left, opToken, right)
        return res.success(left)


