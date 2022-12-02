from Scanner import Scanner
lexical = Scanner()
while True:
    command = input('Ingrese un comando: ')
    lexical.analyze(command)
    lexical.printTokens()
    lexical.printErrors()
    if command == 'ADIOS':
        break