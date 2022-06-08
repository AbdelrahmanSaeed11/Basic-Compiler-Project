from main import *


while True:
    line = input('JngDiff >> ')
    result, error = run('<stdin>', line)
    if error:
        print(error.printError())
    else:
        print(result)
