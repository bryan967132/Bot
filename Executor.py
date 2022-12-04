from Scanner import Scanner
from Parser import Parser
from DataBase import DB,Request
class Executor:
    def __init__(self):
        self.__lexical = Scanner()
        self.__syntax = Parser()
        self.__db = DB()
        self.__request = Request(self.__db)

    def getResponse(self,command):
        self.__lexical.analyze(command)
        self.__syntax.analyze(self.__lexical.getTokens())
        response = self.__syntax.getResponse()
        if not response:
            return '¡Ups! No te entendí, pregúntame de nuevo.'
        return self.__request.new(response)