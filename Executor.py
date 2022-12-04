from Scanner import Scanner
from Parser import Parser
class Executor:
    def __init__(self):
        self.__lexical = Scanner()
        self.__syntax = Parser()

    def getResponse(self,command):
        self.__lexical.analyze(command)
        self.__syntax.analyze(self.__lexical.getTokens())
        print(self.__syntax.getResponse())