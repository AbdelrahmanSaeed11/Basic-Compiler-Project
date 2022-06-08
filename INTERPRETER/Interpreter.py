from ERRORS.Errors import *
from CONSTANTS.Constants import *
#######################################
# RUNTIMERESULT
#######################################

class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self

#######################################
# VALUES
#######################################

class Number: 
    def __init__(self, value):
        self.value = value
        self.setPos()
        self.setContext()

    def setPos(self, startPos = None, endPos = None):
        self.startPos = startPos
        self.endPos = endPos
        return self
    
    def setContext(self, context = None):
        self.context = context
        return self
    
    def add(self, number2):
        if isinstance(number2, Number):
            return Number(self.value + number2.value).setContext(self.context), None

    def subtract(self, number2):
        if isinstance(number2, Number):
            return Number(self.value - number2.value).setContext(self.context), None

    def multiply(self, number2):
        if isinstance(number2, Number):
            return Number(self.value * number2.value).setContext(self.context), None

    def divide(self, number2):
        if isinstance(number2, Number):
            if number2.value == 0: return None, RunTimeError(number2.startPos, number2.endPos, 'Divided by zero', self.context)
            return Number(self.value / number2.value).setContext(self.context), None
    
    def power(self, number2):
        if isinstance(number2, Number):
            return Number(self.value ** number2.value).setContext(self.context), None
    
    def adding(self, number2):
        if isinstance(number2, Number):
            return Number(self.value & number2.value).setContext(self.context), None

    def oring(self, number2):
        if isinstance(number2, Number):
            return Number(self.value | number2.value).setContext(self.context), None
    
    def copy(self):
        copy = Number(self.value)
        copy.setPos(self.startPos, self.endPos)
        copy.setContext(self.context)
        return copy

    def __repr__(self):
        return f'{self.value}'

#######################################
# CONTEXT
#######################################
# To keep tracking the current place of excution

class Context:
    def __init__(self, displayName, parent = None, parentEntryPos = None):
        self.displayName = displayName
        self.parent = parent
        self.parentEntryPos = parentEntryPos
        self.symbolTable = None
    

#######################################
# SYMBOL TABLE
#######################################
# To memorised the variables

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

#######################################
# INTERPRETER
#######################################

class Interpreter:
    def visit(self, node, context):
        methodName = f'visit_{type(node).__name__}'
        method = getattr(self, methodName, self.undefinedMethod)
        return method(node, context)
        
    def undefinedMethod(self, node, context):
        raise Exception(f'visit_{type(node).__name__} method is undefined')

    def visit_NumberNode(self, node, context):
        return RunTimeResult().success(Number(node.token.value).setContext(context).setPos(node.startPos, node.endPos))
    
    
    def visit_BinaryOpNode(self, node, context):
        res = RunTimeResult()
        left = res.register(self.visit(node.leftNode, context))
        if res.error: return res
        right = res.register(self.visit(node.rightNode, context))
        if res.error: return res
        
        if node.opToken.type == PLUS:
            ret, error = left.add(right)

        elif node.opToken.type == MINUS:
            ret, error = left.subtract(right)

        elif node.opToken.type == MUL:
            ret, error = left.multiply(right)

        elif node.opToken.type == DIV:
            ret, error = left.divide(right)
        
        elif node.opToken.type == POW:
            ret, error = left.power(right)
        
        elif node.opToken.type == AND:
            ret, error = left.adding(right)
        
        elif node.opToken.type == OR:
            ret, error = left.oring(right)

        if error: return res.failure(error)
        
        return res.success(ret.setPos(node.startPos, node.endPos))

    def visit_UnaryOpNode(self, node, context):
        res = RunTimeResult()
        ret = res.register(self.visit(node.node, context))
        if res.error: return res

        if node.opToken.type == MINUS:
            ret, error = ret.multiply(Number(-1))
        if error: return res.failure(error)

        return res.success(ret.setPos(node.startPos, node.endPos))

    def visit_VariableAccessNode(self, node, context):
        res = RunTimeResult()
        variableName = node.tokenName.value
        value = context.symbolTable.get(variableName)
        
        if not value:
            return res.failure(RunTimeError(node.startPos, node.endPos, f"'{ValueError}' is not defined", context))
        
        value = value.copy().setPos(node.startPos, node.endPos)
        return res.success(value)
    
    def visit_VariableAssignNode(self, node, context):
        res = RunTimeResult()
        variableName = node.tokenName.value
        value = res.register(self.visit(node.nodeValue, context))
        
        if res.error: return res
        context.symbolTable.set(variableName, value)

        return res.success(value)

