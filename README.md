# Tokens

| Description                               | Standard                                          | Regular Expresion      | Examples                      |
| ----------------------------------------- | ----------------------------------------------- | ---------------------- | ----------------------------- |
| Reserved RESULTADO                       | Word RESULTADO                               | RESULTADO              | RESULTADO                     |
| Reserved TEMPORADA                       | Word TEMPORADA                               | TEMPORADA              | TEMPORADA                     |
| Reserved JORNADA                         | Word JORNADA                                 | JORNADA                | JORNADA                       |
| Reserved GOLES                           | Word GOLES                                   | GOLES                  | GOLES                         |
| Reserved TABLA                           | Word TABLA                                   | TABLA                  | TABLA                         |
| Reserved PARTIDOS                        | Word PARTIDOS                                | PARTIDOS               | PARTIDOS                      |
| Reserved TOP                             | Word TOP                                     | TOP                    | TOP                           |
| Reserved ADIOS                           | Word ADIOS                                   | ADIOS                  | ADIOS                         |
| Reserved VS                              | Word VS                                      | VS                     | VS                            |
| Reserved LOCAL                           | Word LOCAL                                   | LOCAL                  | LOCAL                         |
| Reserved VISITANTE                       | Word VISITANTE                               | VISITANTE              | VISITANTE                     |
| Reserved TOTAL                           | Word TOTAL                                   | TOTAL                  | TOTAL                         |
| Reserved SUPERIOR                        | Word SUPERIOR                                | SUPERIOR               | SUPERIOR                      |
| Reserved INFERIOR                        | Word INFERIOR                                | INFERIOR               | INFERIOR                      |
| Assigned Values                         | Alphanumeric Character Sequence           | "[A-Za-z][0-9a-za-z]\*"| "Real Madrid","Barcelona"     |
| Numerical values                         | Numeric Character Sequence               | [0-9]\*                | 5,13,18,35,22                 |
| Less Than                           | Character '<'                                 | '<'                    | <                             |
| More Than                           | Character '>'                                 | '>'                    | >                             |
| Hyphen                                     | Character '-'                                 | '-'                    | -                             |

# AFD
<image src="Images/AFD_Bot.png" width="70%" height="70%" alt="AFD">

# Context Free Grammar
| Productions                              |
| ----------------------------------------- |
\<INIT\> ::= \<SCORE\> \| \<MATCHDAY\> \| \<GOALS\> \| \<STANDINGS\> \| \<MATCHES\> \| \<TOP\> \| rw_ADIOS
\<SCORE\> ::= rw_RESULTADO teamName rw_VS teamName \<SEASON\>
\<MATCHDAY\> ::= rw_JORNADA number \<SEASON\> \<FLAGS\>
\<GOALS\> ::= rw_GOLES \<TEAMCONDITION\> teamName \<SEASON\>
\<STANDINGS\> ::= rw_TABLA \<SEASON\> \<FLAGS\>
\<MATCHES\> ::= rw_PARTIDOS teamName \<SEASON\> \<FLAGS\>
\<TOP\> ::= rw_TOP \<TOPCONDITION\> \<SEASON\> \<FLAGS\>
\<SEASON\> ::= rw_TEMPORADA lessThan number hyphen number moreThan
\<TEAMCONDITION\> ::= rw_LOCAL \| rw_VISITANTE \| rw_TOTAL
\<TOPCONDITION\> ::= rw_SUPERIOR \| rw_INFERIOR
\<FLAGS\> ::= flag_f string \| flag_n number \| flag_ji number \| flag_jf number \| ϵ \| \<FLAGS\>
\<FLAGS1\> ::= flag_f string \| flag_n number \| flag_ji number \| flag_jf number \| ϵ \| \<FLAGS\>