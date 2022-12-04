import csv
from Match import Match
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
    def __init__(self,db : DB):
        self.__db = db

    def new(self,response):
        pass

    def resultado(self,local,visitante,año1,año2):
        temporada = año1 + '-' + año2
        for partido in self.db:
            if partido.getLocal() == local and partido.getVisitante() == visitante and partido.getTemporada() == temporada:
                return f'El resultado del partido fue: {partido.getLocal()} {partido.getGolesL()} - {partido.getVisitante()} {partido.getGolesV()}.'
        return 'No hay resgistro del partido.'
    
    def jornada(self,numero,año1,año2,archivo = 'jornada'):
        archivo += '.html'
        temporada = año1 + '-' + año2
        encontradoT = False
        encontradoJ = False
        partidos = []
        for partido in self.db:
            if partido.getTemporada() == temporada:
                encontradoT = True
                if partido.getJornada() == numero:
                    encontradoJ = True
                    partidos.append(partido)
        if not encontradoT:
            return f'No existe la temporada {temporada} :('
        if not encontradoJ:
            return f'No existe la jornada {numero} de la temporada {temporada} :('
        Reportes().repJornada(archivo,temporada,numero,partidos)
        return f'Generando archivo de resultados jornada {numero} temporada {temporada}.'
    
    def goles(self,condicion,equipo,año1,año2):
        temporada = año1 + '-' + año2
        if condicion == 'TOTAL':
            goles = 0
            for partido in self.db:
                if partido.getTemporada() == temporada:
                    if partido.getLocal() == equipo:
                        goles += partido.getGolesL()
                    elif partido.getVisitante() == equipo:
                        goles += partido.getGolesV()
            return f'Los goles anotados por el {equipo} en total en la temporada {temporada} fueron {goles}.'
        elif condicion == 'LOCAL':
            return self.golesL(equipo,temporada)
        elif condicion == 'VISITANTE':
            return self.golesV(equipo,temporada)
    
    def golesL(self,equipo,temporada):
        goles = 0
        for partido in self.db:
            if partido.getTemporada() == temporada:
                if partido.getLocal() == equipo:
                    goles += partido.getGolesL()
        return f'Los goles anotados por el {equipo} de local en la temporada {temporada} fueron {goles}.'

    def golesV(self,equipo,temporada):
        goles = 0
        for partido in self.db:
            if partido.getTemporada() == temporada:
                if partido.getVisitante() == equipo:
                    goles += partido.getGolesV()
        return f'Los goles anotados por el {equipo} de visitante en la temporada {temporada} fueron {goles}.'
    
    def tabla(self,año1,año2,archivo = 'temporada'):
        archivo += '.html'
        temporada = año1 + '-' + año2
        tabla = self.simularTemporada(temporada)
        if len(tabla) == 0:
            return f'No hay partidos de la temporada {temporada}.'
        Reportes().repTabla(archivo,temporada,tabla)
        return f'Generando archivo de clasificación de temporada {temporada}.'

    def simularTemporada(self,temporada):
        tabla = []
        for partido in self.db:
            if partido.getTemporada() == temporada:
                if partido.getJornada() == 1:
                    tabla.append(Posicion(partido.getLocal(),0,0,0,0,0,0))
                    tabla.append(Posicion(partido.getVisitante(),0,0,0,0,0,0))
                elif partido.getJornada() == 2:
                    break
        
        for posicion in tabla:
            for partido in self.db:
                if partido.getTemporada() == temporada:
                    if partido.getLocal() == posicion.getEquipo():
                        if partido.getGolesL() > partido.getGolesV():
                            posicion.setPG(posicion.getPG() + 1)
                            posicion.setPuntos(posicion.getPuntos() + 3)
                        elif partido.getGolesL() == partido.getGolesV():
                            posicion.setPE(posicion.getPE() + 1)
                            posicion.setPuntos(posicion.getPuntos() + 1)
                        elif partido.getGolesL() < partido.getGolesV():
                            posicion.setPP(posicion.getPP() + 1)
                        posicion.setGF(posicion.getGF() + partido.getGolesL())
                        posicion.setGC(posicion.getGC() + partido.getGolesV())
                    elif partido.getVisitante() == posicion.getEquipo():
                        if partido.getGolesL() < partido.getGolesV():
                            posicion.setPG(posicion.getPG() + 1)
                            posicion.setPuntos(posicion.getPuntos() + 3)
                        elif partido.getGolesL() == partido.getGolesV():
                            posicion.setPE(posicion.getPE() + 1)
                            posicion.setPuntos(posicion.getPuntos() + 1)
                        elif partido.getGolesL() > partido.getGolesV():
                            posicion.setPP(posicion.getPP() + 1)
                        posicion.setGF(posicion.getGF() + partido.getGolesV())
                        posicion.setGC(posicion.getGC() + partido.getGolesL())
        
        for i in range(len(tabla) - 1):
            for j in range(len(tabla) - i - 1):
                if tabla[j].getPuntos() < tabla[j + 1].getPuntos():
                    tabla[j],tabla[j + 1] = tabla[j + 1],tabla[j]
                elif tabla[j].getPuntos() == tabla[j + 1].getPuntos():
                    golesActual = tabla[j].getGF() - tabla[j].getGC()
                    golesSiguiente = tabla[j + 1].getGF() - tabla[j + 1].getGC()
                    if golesActual < golesSiguiente:
                        tabla[j],tabla[j + 1] = tabla[j + 1],tabla[j]

        return tabla

    def partidos(self,equipo,año1,año2,archivo = 'partidos',numJi = 1,numJf = 38):
        archivo += '.html'
        temporada = año1 + '-' + año2
        encontradoT = False
        encontradoE = False
        partidos = []
        for partido in self.db:
            if partido.getTemporada() == temporada:
                encontradoT = True
                if partido.getJornada() >= numJi and partido.getJornada() <= numJf:
                    if partido.getLocal() == equipo:
                        encontradoE = True
                        partidos.append(partido)
                    elif partido.getVisitante() == equipo:
                        encontradoE = True
                        partidos.append(partido)
        if not encontradoT:
            return f'No existe la temporada {temporada} :('
        if len(partidos) == 0:
            return f'No se encontraron partidos del {equipo} de la temporada {temporada} de la jornada {numJi} a la {numJf}.'
        if not encontradoE:
            return f'No existe el equipo {equipo} en la temporada {temporada} :('
        return f'Generando archivo de resultados de la temporada {temporada} del {equipo}.'
    
    def top(self,condicion,año1,año2,top = 5):
        temporada = año1 + '-' + año2
        tabla = self.simularTemporada(temporada)
        if len(tabla) == 0:
            return f'No hay partidos de la temporada {temporada}.'
        if condicion == 'SUPERIOR':
            inferior = 0
            superior = top
        elif condicion == 'INFERIOR':
            inferior = len(tabla) - top
            superior = len(tabla)
        clasificacion = f'Top {top} de la temporada {temporada}'
        for i in range(inferior,superior):
            clasificacion += f'\n{i + 1}. {tabla[i].getEquipo()}'
        return clasificacion