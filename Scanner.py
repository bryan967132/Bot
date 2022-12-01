from Token import Token
from Error import Error
from prettytable import PrettyTable
class Scanner:
    def __reset(self):
        self.__tokens = []
        self.__errors = []
        self.__status = 0
        self.__line = 1
        self.__column = 1
        self.__buffer = ''
        self.__i = 0
    
    def __addToken(self,type):
        self.__tokens.append(Token(self.__buffer,type,self.__line,self.__column))
        self.__buffer = ''
        self.__status = 0
        self.__i -= 1
    
    def __addError(self):
        self.__errors.append(Error(f'Caracter \'{self.__buffer}\' no reconocido',self.__line,self.__column))
        self.__buffer = ''
        self.__status = 0

    def printTokens(self):
        x = PrettyTable()
        x.field_names = ['Lexeme','Type','Line','Column']
        for token in self.__tokens:
            x.add_row([token.lexeme,token.type,token.line,token.column])
        print(x)
    
    def printErrors(self):
        x = PrettyTable()
        x.field_names = ['Description','Line','Column']
        for error in self.__errors:
            x.add_row([error.description,error.line,error.column])
        print(x)

    def getTokens(self) -> list:
        return self.__tokens
    
    def getErrors(self) -> list:
        return self.__errors
    
    def __S0(self,character):
        if character.isalpha():
            self.__status = 1
            self.__column += 1
            self.__buffer += character
        elif character == '"':
            self.__status = 2
            self.__column += 1
            self.__buffer += character
        elif character == '<':
            self.__status = 5
            self.__column += 1
            self.__buffer += character
        elif character == '>':
            self.__status = 6
            self.__column += 1
            self.__buffer += character
        elif character.isdigit():
            self.__status = 7
            self.__column += 1
            self.__buffer += character
        elif character == '-':
            self.__status = 8
            self.__column += 1
            self.__buffer += character
        elif character == ' ':
            self.__column += 1
        elif character == '\n':
            self.__line += 1
            self.__column = 1
        elif character == '#':
            pass
        else:
            self.__buffer += character
            self.__addError()
            self.__column += 1
        
    def __S1(self,character):
        if character.isalpha() or character.isdigit():
            self.__status = 1
            self.__column += 1
            self.__buffer += character
        elif self.__buffer in ['RESULTADO','TEMPORADA','JORNADA','GOLES','TABLA','PARTIDOS','TOP','ADIOS','VS','LOCAL','VISITANTE','TOTAL','SUPERIOR','INFERIOR']:
            self.__addToken(f'RW_{self.__buffer}')
        else:
            self.__addToken('String')

    def __S2(self,character):
        if character.isalpha() or character == ' ':
            self.__status = 3
            self.__column += 1
            self.__buffer += character
        elif character == '"':
            self.__status = 4
            self.__column += 1
            self.__buffer += character
        else:
            self.__addError()
            self.__i -= 1
    
    def __S3(self,character):
        if character.isalpha() or character == ' ':
            self.__status = 3
            self.__column += 1
            self.__buffer += character
        elif character == '"':
            self.__status = 4
            self.__column += 1
            self.__buffer += character
        else:
            self.__addError()
            self.__i -= 1
    
    def __S4(self):
        self.__addToken('TeamName')
    
    def __S5(self):
        self.__addToken('LessThan')
    
    def __S6(self):
        self.__addToken('MoreThan')
    
    def __S7(self,character):
        if character.isdigit():
            self.__status = 7
            self.__column += 1
            self.__buffer += character
        else:
            self.__addToken('Number')
    
    def __S8(self,character):
        if character == 'f':
            self.__status = 9
            self.__column += 1
            self.__buffer += character
        elif character == 'j':
            self.__status = 10
            self.__column += 1
            self.__buffer += character
        elif character == 'n':
            self.__status = 12
            self.__column += 1
            self.__buffer += character
        else:
            self.__addToken(f'Hyphen'.replace('-',''))
    
    def __S9(self):
        self.__addToken(f'Flag_{self.__buffer}'.replace('-',''))
    
    def __S10(self,character):
        if character in ['i','f']:
            self.__status = 11
            self.__column += 1
            self.__buffer += character
        else:
            self.buffer += character
            self.__addError()
    
    def __S11(self):
        self.__addToken(f'Flag_{self.__buffer}'.replace('-',''))
    
    def __S12(self):
        self.__addToken(f'Flag_{self.__buffer}'.replace('-',''))
    
    def analyze(self,string):
        string += '#'
        self.__reset()
        while self.__i < len(string):
            if self.__status == 0:
                self.__S0(string[self.__i])
            elif self.__status == 1:
                self.__S1(string[self.__i])
            elif self.__status == 2:
                self.__S2(string[self.__i])
            elif self.__status == 3:
                self.__S3(string[self.__i])
            elif self.__status == 4:
                self.__S4()
            elif self.__status == 5:
                self.__S5()
            elif self.__status == 6:
                self.__S6()
            elif self.__status == 7:
                self.__S7(string[self.__i])
            elif self.__status == 8:
                self.__S8(string[self.__i])
            elif self.__status == 9:
                self.__S9()
            elif self.__status == 10:
                self.__S10(string[self.__i])
            elif self.__status == 11:
                self.__S11()
            elif self.__status == 12:
                self.__S12()
            self.__i += 1