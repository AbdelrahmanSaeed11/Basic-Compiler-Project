#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.startPos = self.token.startPos
        self.endPos = self.token.endPos
        
    def __repr__(self):
        return f'{self.token}'

class BinaryOpNode:
    def __init__(self, leftNode, opToken, rightNode):
        self.leftNode = leftNode
        self.opToken = opToken
        self.rightNode = rightNode
        self.startPos = self.leftNode.startPos
        self.endPos = self.rightNode.endPos
    def __repr__(self):
        return f'({self.leftNode}, {self.opToken}, {self.rightNode})'

class UnaryOpNode:
    def __init__(self, opToken, node):
        self.opToken = opToken
        self.node = node
        self.startPos = self.opToken.startPos
        self.endPos = self.node.endPos
    def __repr__(self):
        return f'{self.opToken} , {self.node}'

class VariableAccessNode:
    def __init__(self, tokenName):
        self.tokenName = tokenName
        self.startPos = self.tokenName.startPos
        self.endPos = self.tokenName.endPos


class VariableAssignNode:
    def __init__(self, tokenName, nodeValue):
        self.tokenName = tokenName
        self.nodeValue = nodeValue
        self.startPos = self.tokenName.startPos
        self.endPos = self.nodeValue.endPos


