import csv
from Match import Match
from Place import Place
class DB:
    def __init__(self):
        self.__record = []
        with open('Data/LaLigaBot-LFP.csv',newline = '',encoding = 'utf-8') as data:
            spamreader = csv.DictReader(data)
            for row in spamreader:
                self.__record.append(Match(row['Fecha'],row['Temporada'],int(row['Jornada']),row['Equipo1'],row['Equipo2'],int(row['Goles1']),int(row['Goles2'])))
    
    def getData(self):
        return self.__record

class Request:
    def __init__(self,db : list):
        self.__db = db

    def new(self,response):
        command = response['command']
        if response['function'] == 'SCORE':
            return self.__score(command['teamName1'],command['teamName2'],command['season'])
        elif response['function'] == 'MATCHDAY':
            flags = response['flags']
            return self.__matchday(command['matchday'],command['season'],flags['-f'])
        elif response['function'] == 'GOALS':
            return self.__goals(command['condition'],command['teamName'],command['season'])
        elif response['function'] == 'STANDINGS':
            flags = response['flags']
            return self.__standings(command['season'],flags['-f'])
        elif response['function'] == 'MATCHES':
            flags = response['flags']
            return self.__matches(command['teamName'],command['season'],flags['f'],flags['-ji'],flags['-jf'])
        elif response['function'] == 'TOP':
            flags = response['flags']
            return self.__top(command['condition'],command['season'],flags['-n'])
        elif response['function'] == 'ADIOS':
            return command

    def __score(self,local,visitor,season):
        for match in self.__db:
            if match.getLocal() == local and match.getVisitor() == visitor and match.getSeason() == season:
                return f'El resultado del partido fue: {match.getLocal()} {match.getGoalsL()} - {match.getVisitor()} {match.getGoalsV()}.'
        return 'No encontré nada del partido que buscas :('

    def __matchday(self,number,season,file):
        file += '.html'
        foundT = False
        foundJ = False
        matches = []
        for match in self.__db:
            if match.getSeason() == season:
                foundT = True
                if match.getMatchday() == number:
                    foundJ = True
                    matches.append(match)
        if not foundT:
            return f'No encontré la temporada {season} :('
        if not foundJ:
            return f'No encontré la jornada {number} de la temporada {season} :('
        # Report
        return f'Estoy generando un archivo de resultados de la jornada {number} temporada {season} :)'

    def __goals(self,condition,team,season):
        if condition == 'TOTAL':
            return f'Los goles anotados por el {team} en total en la temporada {season} fueron {self.__goalsL(team,season) + self.__goalsV(team,season)}.'
        elif condition == 'LOCAL':
            return f'Los goles anotados por el {team} de local en la temporada {season} fueron {self.__goalsL(team,season)}'
        elif condition == 'VISITANTE':
            return f'Los goles anotados por el {team} de local en la temporada {season} fueron {self.__goalsV(team,season)}'

    def __goalsL(self,team,season):
        goals = 0
        for match in self.__db:
            if match.getSeason() == season:
                if match.getLocal() == team:
                    goals += match.getGoalsL()
        return goals

    def __goalsV(self,team,season):
        goals = 0
        for match in self.__db:
            if match.getSeason() == season:
                if match.getVisitor() == team:
                    goals += match.getGoalsV()
        return goals

    def __standings(self,season,file):
        file += '.html'
        standings = self.__simulateSeason(season)
        if len(standings) == 0:
            return f'No encontré partidos de la temporada {season} :('
        # Report
        return f'Estoy generando un archivo de clasificación de la temporada {season} :)'

    def __simulateSeason(self,season):
        standings = []
        for match in self.__db:
            if match.getSeason() == season:
                if match.getMatchday() == 1:
                    standings.append(Place(match.getLocal(),0,0,0,0,0,0))
                    standings.append(Place(match.getVisitor(),0,0,0,0,0,0))
                elif match.getMatchday() == 2:
                    break

        for place in standings:
            for match in self.__db:
                if match.getSeason() == season:
                    if match.getLocal() == place.getTeam():
                        if match.getGoalsL() > match.getGoalsV():
                            place.setPG(place.getPG() + 1)
                            place.setPuntos(place.getPoints() + 3)
                        elif match.getGoalsL() == match.getGoalsV():
                            place.setPE(place.getPE() + 1)
                            place.setPuntos(place.getPoints() + 1)
                        elif match.getGoalsL() < match.getGoalsV():
                            place.setPP(place.getPP() + 1)
                        place.setGF(place.getGF() + match.getGoalsL())
                        place.setGC(place.getGC() + match.getGoalsV())
                    elif match.getVisitante() == place.getTeam():
                        if match.getGoalsL() < match.getGoalsV():
                            place.setPG(place.getPG() + 1)
                            place.setPuntos(place.getPoints() + 3)
                        elif match.getGoalsL() == match.getGoalsV():
                            place.setPE(place.getPE() + 1)
                            place.setPuntos(place.getPoints() + 1)
                        elif match.getGoalsL() > match.getGoalsV():
                            place.setPP(place.getPP() + 1)
                        place.setGF(place.getGF() + match.getGoalsV())
                        place.setGC(place.getGC() + match.getGoalsL())

        for i in range(len(standings) - 1):
            for j in range(len(standings) - i - 1):
                if standings[j].getPoints() < standings[j + 1].getPoints():
                    standings[j],standings[j + 1] = standings[j + 1],standings[j]
                elif standings[j].getPoints() == standings[j + 1].getPoints():
                    goalsCurrent = standings[j].getGF() - standings[j].getGC()
                    goalsNext = standings[j + 1].getGF() - standings[j + 1].getGC()
                    if goalsCurrent < goalsNext:
                        standings[j],standings[j + 1] = standings[j + 1],standings[j]

        return standings

    def __matches(self,team,season,file,matchdayI,matchdayF):
        file += '.html'
        foundT = False
        foundE = False
        matches = []
        for match in self.__db:
            if match.getSeason() == season:
                foundT = True
                if match.getMatchday() >= matchdayI and match.getMatchday() <= matchdayF:
                    if match.getLocal() == team:
                        foundE = True
                        matches.append(match)
                    elif match.getVisitor() == team:
                        foundE = True
                        matches.append(match)
        if not foundT:
            return f'No encontré la temporada {season} :('
        if len(matches) == 0:
            return f'No encontré partidos del {team} de la temporada {season} de la jornada {matchdayI} a la {matchdayF} :('
        if not foundE:
            return f'No encontré al equipo {team} en la temporada {season} :('
        # Report
        return f'Estoy generando un archivo de resultados de la temporada {season} del {team} :)'
    
    def __top(self,condition,season,top):
        standings = self.__simulateSeason(season)
        if len(standings) == 0:
            return f'No encontré partidos de la temporada {season} :('
        if condition == 'SUPERIOR':
            inferior = 0
            superior = top
        elif condition == 'INFERIOR':
            inferior = len(standings) - top
            superior = len(standings)
        qualifying = f'Este es el Top {top} de la temporada {season}'
        for i in range(inferior,superior):
            qualifying += f'\n{i + 1}. {standings[i].getTeam()}'
        return qualifying