from Scanner import Scanner
from Parser import Parser
lexical = Scanner()
syntax = Parser()
while True:
    command = input('Ingrese un comando: ')
    lexical.analyze(command)
    syntax.analyze(lexical.getTokens())
    if command == 'ADIOS':
        break