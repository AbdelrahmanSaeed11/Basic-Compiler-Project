from LEXER.Lexer import *
from PARSER.Parser import *
from INTERPRETER.Interpreter import *
#######################################
# RUN
#######################################

globalSymbolTable = SymbolTable()
globalSymbolTable.set('null', Number(0))

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.createTokens()
    if error: return None, error
    parser = Parser(tokens)
    AST = parser.parse()
    if AST.error: return None, AST.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbolTable = globalSymbolTable
    finalResult = interpreter.visit(AST.node, context)
    return finalResult.value, finalResult.error