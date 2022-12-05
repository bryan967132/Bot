class Match:
    def __init__(self,date,season,matchday,local,visitor,goalsL,goalsV):
        self.setDate(date)
        self.setSeason(season)
        self.setMatchday(matchday)
        self.setLocal(local)
        self.setVisitante(visitor)
        self.setGoalsL(goalsL)
        self.setGoalsV(goalsV)

    def getDate(self):
        return self.__date
    
    def setDate(self,date):
        self.__date = date

    def getSeason(self):
        return self.__season
    
    def setSeason(self,season):
        self.__season = season

    def getMatchday(self):
        return self.__matchday
    
    def setMatchday(self,matchday):
        self.__matchday = matchday

    def getLocal(self):
        return self.__local

    def setLocal(self,local):
        self.__local = local
    
    def getVisitor(self):
        return self.__visitor

    def setVisitante(self,visitor):
        self.__visitor = visitor
    
    def getGoalsL(self):
        return self.__goalsL
    
    def setGoalsL(self,goalsL):
        self.__goalsL = goalsL

    def getGoalsV(self):
        return self.__goalsV
    
    def setGoalsV(self,goalsV):
        self.__goalsV = goalsV