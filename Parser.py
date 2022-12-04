from Token import Token
class Parser:  
    def __init__(self):
        self.__errors = []

    def __reset(self):
        self.__command = {}
        self.__flags = {}
        self.__response = None
    
    def __addError(self,expected,obtained):
        self.__errors.append(f'SYNTAX ERROR: It was obtained {obtained}, but it was expected {expected}')
    
    def __popToken(self) -> Token:
        try:
            return self.__tokens.pop(0)
        except:
            return None

    def __INIT(self):
        token = self.__popToken()
        if not token:
            self.__addError('RW_RESULTADO | RW_JORNADA | RW_GOLES | RW_TABLA | RW_PARTIDOS | RW_TOP | RW_ADIOS','EOF')
        elif token.type == 'RW_RESULTADO':
            self.__SCORE()
        elif token.type == 'RW_JORNADA':
            self.__MATCHDAY()
        elif token.type == 'RW_GOLES':
            self.__GOALS()
        elif token.type == 'RW_TABLA':
            self.__STANDINGS()
        elif token.type == 'RW_PARTIDOS':
            self.__MATCHES()
        elif token.type == 'RW_TOP':
            self.__TOP()
        elif token.type == 'RW_ADIOS':
            print('Command Accepted')
        else:
            self.__addError('RW_RESULTADO | RW_JORNADA | RW_GOLES | RW_TABLA | RW_PARTIDOS | RW_TOP | RW_ADIOS',token.type)

    def __SCORE(self):
        token = self.__popToken()
        if not token:
            self.__addError('TeamName','EOF')
        elif token.type == 'TeamName':
            self.__command['teamName1'] = token.lexeme.replace('"','')
            token = self.__popToken()
            if not token:
                self.__addError('RW_VS','EOF')
            elif token.type == 'RW_VS':
                token = self.__popToken()
                if not token:
                    self.__addError('TeamName','EOF')
                elif token.type == 'TeamName':
                    self.__command['teamName2'] = token.lexeme.replace('"','')
                    if self.__SEASON():
                        self.__response = {'function':'SCORE','command':self.__command}
                else:
                    self.__addError('TeamName',token.type)
            else:
                self.__addError('RW_VS',token.type)
        else:
            self.__addError('TeamName',token.type)

    def __MATCHDAY(self):
        token = self.__popToken()
        if not token:
            self.__addError('Number','EOF')
        elif token.type == 'Number':
            self.__command['matchday'] = int(token.lexeme)
            if self.__SEASON():
                self.__flags['-f'] = 'jornada'
                if self.__FLAGS():
                    self.__response = {'function':'MATCHDAY','command':self.__command,'flags':self.__flags}
        else:
            self.__addError('Number',token.type)

    def __GOALS(self):
        token = self.__popToken()
        if not token:
            self.__addError('RW_TOTAL | RW_LOCAL | RW_VISITANTE','EOF')
        elif token.type == 'RW_TOTAL' or token.type == 'RW_LOCAL' or token.type == 'RW_VISITANTE':
            self.__command['condition'] = token.lexeme
            token = self.__popToken()
            if not token:
                self.__addError('TeamName','EOF')
            elif token.type == 'TeamName':
                self.__command['teamName'] = token.lexeme.replace('"','')
                if self.__SEASON():
                    self.__response = {'function':'GOALS','command':self.__command}
            else:
                self.__addError('TeamName',token.type)
        else:
            self.__addError('RW_TOTAL | RW_LOCAL | RW_VISITANTE','EOF',token.type)

    def __STANDINGS(self):
        if self.__SEASON():
            self.__flags['-f'] = 'temporada'
            if self.__FLAGS():
                self.__response = {'function':'STANDINGS','command':self.__command,'flags':self.__flags}

    def __MATCHES(self):
        token = self.__popToken()
        if not token:
            self.__addError('TeamName','EOF')
        elif token.type == 'TeamName':
            self.__command['teamName'] = token.lexeme.replace('"','')
            if self.__SEASON():
                self.__flags['-f'] = 'partidos'
                self.__flags['-ji'] = '1'
                self.__flags['-jf'] = '38'
                if self.__FLAGS():
                    self.__response = {'function':'MATCHES','command':self.__command,'flags':self.__flags}
        else:
            self.__addError('TeamName',token.type)

    def __TOP(self):
        token = self.__popToken()
        if not token:
            self.__addError('RW_SUPERIOR | RW_INFERIOR','EOF')
        elif token.type == 'RW_SUPERIOR' or token.type == 'RW_INFERIOR':
            self.__command['condition'] = token.lexeme
            if self.__SEASON():
                self.__flags['-n'] = 5
                if self.__FLAGS():
                    self.__response = {'function':'TOP','command':self.__command,'flags':self.__flags}
        else:
            self.__addError('RW_SUPERIOR | RW_INFERIOR',token.type)

    def __SEASON(self):
        token = self.__popToken()
        if not token:
            self.__addError('RW_TEMPORADA','EOF')
        elif token.type == 'RW_TEMPORADA':
            token = self.__popToken()
            if not token:
                self.__addError('LessThan','EOF')
            elif token.type == 'LessThan':
                token = self.__popToken()
                if not token:
                    self.__addError('Number','EOF')
                elif token.type == 'Number':
                    if len(token.lexeme) == 4:
                        self.__command['year1'] = int(token.lexeme)
                        token = self.__popToken()
                        if not token:
                            self.__addError('Hyphen','EOF')
                        elif token.type == 'Hyphen':
                            token = self.__popToken()
                            if not token:
                                self.__addError('Number','EOF')
                            elif token.type == 'Number':
                                if len(token.lexeme) == 4:
                                    self.__command['year2'] = int(token.lexeme)
                                    token = self.__popToken()
                                    if not token:
                                        self.__addError('MoreThan','EOF')
                                    elif token.type == 'MoreThan':
                                        return True
                                    else:
                                        self.__addError('MoreThan',token.type)
                                else:
                                    self.__addError('4 Digit Number',f'{len(token.lexeme)} Digit Number')
                            else:
                                self.__addError('Number',token.type)
                        else:
                            self.__addError('Hyphen',token.type)
                    else:
                        self.__addError('4 Digit Number',f'{len(token.lexeme)} Digit Number')
                else:
                    self.__addError('Number',token.type)
            else:
                self.__addError('LessThan',token.type)
        else:
            self.__addError('RW_TEMPORADA',token.type)

    def __FLAGS(self) -> bool:
        token = self.__popToken()
        if token:
            if token.type == 'Flag_f':
                return self.__FLAGF()
            if token.type == 'Flag_ji':
                return self.__FLAGJI()
            if token.type == 'Flag_jf':
                return self.__FLAGJF()
            if token.type == 'Flag_n':
                return self.__FLAGN()
        return True

    def __FLAGF(self) -> bool:
        token = self.__popToken()
        if not token:
            self.__addError('String','EOF')
            return False
        if token.type == 'String':
            self.__flags['-f'] = token.lexeme
            return self.__FLAGS()
        self.__addError('String',token.type)
        return False

    def __FLAGJI(self) -> bool:
        token = self.__popToken()
        if not token:
            self.__addError('Number','EOF')
            return False
        if token.type == 'Number':
            self.__flags['-ji'] = int(token.lexeme)
            return self.__FLAGS()
        self.__addError('Number',token.type)
        return False

    def __FLAGJF(self) -> bool:
        token = self.__popToken()
        if not token:
            self.__addError('Number','EOF')
            return False
        elif token.type == 'Number':
            self.__flags['-jf'] = int(token.lexeme)
            return self.__FLAGS()
        self.__addError('Number',token.type)
        return False

    def __FLAGN(self) -> bool:
        token = self.__popToken()
        if not token:
            self.__addError('Number','EOF')
            return False
        elif token.type == 'Number':
            self.__flags['-n'] = int(token.lexeme)
            return self.__FLAGS()
        self.__addError('Number',token.type)
        return False

    def analyze(self,tokens):
        self.__tokens = tokens
        self.__reset()
        self.__INIT()

    def getResponse(self) -> dict:
        return self.__response