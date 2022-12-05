class Place:
    def __init__(self,team,pG,pE,pP,gF,gC,points):
        self.setTeam(team)
        self.setPG(pG)
        self.setPE(pE)
        self.setPP(pP)
        self.setGF(gF)
        self.setGC(gC)
        self.setPoints(points)

    def getTeam(self):
        return self.__team
    
    def setTeam(self,team):
        self.__team = team
    
    def getPG(self):
        return self.__pG

    def setPG(self,pG):
        self.__pG = pG

    def getPE(self):
        return self.__pE

    def setPE(self,pE):
        self.__pE = pE

    def getPP(self):
        return self.__pP

    def setPP(self,pP):
        self.__pP = pP

    def getGF(self):
        return self.__gF
    
    def setGF(self,gF):
        self.__gF = gF

    def getGC(self):
        return self.__gC
    
    def setGC(self,gC):
        self.__gC = gC

    def getPoints(self):
        return self.__puntos

    def setPoints(self,puntos):
        self.__puntos = puntos