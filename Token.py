class Token:
    def __init__(self,lexeme,type,line,column):
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.column = column