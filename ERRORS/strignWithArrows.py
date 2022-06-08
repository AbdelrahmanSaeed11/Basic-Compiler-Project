def strWithArrows(text, startPos, endPos):
    ret = text + '\n'
    ret += ' ' * startPos.idx + '^' * (endPos.idx - startPos.idx)
    return ret

