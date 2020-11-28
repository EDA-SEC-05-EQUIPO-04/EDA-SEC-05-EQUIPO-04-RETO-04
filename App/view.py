"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
from typing import Iterator
import config
from App import controller
from DISClib.ADT import stack
from DISClib.DataStructures import listiterator as it
from DISClib.ADT.graph import gr
import timeit
import numpy as np
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


initialStation = None
recursionLimit = 20000
# ___________________________________________________
#  Menu principal
# ___________________________________________________

def optionLoad():
    print("\nCargando información de bicicletas...")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def optionOne():
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))
    station1=input("Id estación 1 a comparar:\n")
    station2=input("Id estación 2 a comparar:\n")
    if controller.sameCC(cont,station1,station2):
        res="SI"
    else:
        res="NO"

    print('La estación {} y la estación {} {} pertencen al mismo cluster.'.format(station1,station2,res))

def optionFour():
    station=input("Id de la estación que se encuentra:\n")
    resistenciamin=input("¿Cuanto quieres pedalear minimo?: \n")
    resistencia=input("¿Que tanto puedes pedalear? (minutos):\n")
    res=controller.fourthRequirement(cont,station,resistencia,resistenciamin)
    if res==None:
        print('No alcanzas a llegar a ningun estación :( . Mejora tu resistencia!')
    else:
        print('La ruta es la siguiente:')
        iterator=it.newIterator(res)
        while it.hasNext(iterator):
            element=it.next(iterator)
            iterator2=it.newIterator(element)
            ruta=station
            distancia=0
            estacion2=""
            while it.hasNext(iterator2):
                element2=it.next(iterator2)
                estacion2=element2['vertexB']
                ruta+="-"+estacion2
                distancia+=int(element2['weight'])
            print("Estación inicial: {}, estación final: {} duración de viaje: {}, ruta: {}".format(station,estacion2,distancia, ruta))

def optionFifth():
    rango=int(np.floor(int(input("Digite su edad:\n"))/10))
    res=controller.fifthRequirement(cont,rango)
    
def optionSixth():
    latitud= np.radians(float(input("Latitud posición actual:\n")))
    longitud= np.radians(float(input("Longitud posición actual:\n")))
    latitud2= np.radians(float(input("Latitud posición NYC:\n")))
    longitud2= np.radians(float(input("Longitud posición NYC:\n")))
    dict=controller.sixthRequirement(cont,latitud,longitud,latitud2,longitud2)    
    iterator=it.newIterator(dict['ruta'])
    ruta=dict['origen']
    while it.hasNext(iterator):
        element=it.next(iterator)
        estacion2=element['vertexB']
        ruta+="-"+estacion2
        
    print("Estación inicial: {}, estación final: {} duración de viaje: {}, ruta: {}".format(dict['origen'],dict['destino'],dict['duracion'], ruta))

def optionSeventh():
    rango=int(np.floor(int(input("Digite su edad:\n"))/10))
    res=controller.seventhRequirement(cont,rango)
    print("Las parejas adjacentes mas frecuentadas por el grupo de edad {}'s son: {}-{} con una frecuencia de {}".format(int(rango)*10,res['vertexA'],res['vertexB'],res['weight']))

def optionEighth():
    id=int(input("Digite el indicador de bicicleta:\n"))
    fecha=input("Digite la fecha a buscar:\n")
    res=controller.eighthRequirement(cont,id,fecha)

def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def optionTwo(cont):
    time1 = int(input("Ingrese su tiempo inicial: "))
    time2 = int(input("Ingrese su tiempo final:"))
    stationid = (input("Ingrese su estacion de inicio:"))
    ret = controller.Function2(cont, time1, time2, stationid)
    print(ret)
    
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("R1- Requerimiento 1")
    print("R2- Requerimiento 2")
    print("R3- Requerimiento 3")
    print("R4- Requerimiento 4")
    print("R5- Requerimiento 5")
    print("R6- Requerimiento 6")
    print("0- Salir")
    print("*******************************************")

def printRespuesta():
    print("---------------------------------------------------")
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if  inputs[0] == "1":
        printRespuesta()
        
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
       
        printRespuesta()
    
    elif inputs[0] == "2":
        printRespuesta()
        executiontime = timeit.timeit(optionLoad, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        printRespuesta()

    elif inputs == "R1":
        printRespuesta()
        executiontime = timeit.timeit(optionOne, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        printRespuesta()
    
    elif inputs == "R2":
        optionTwo(cont)

    elif inputs == "R3":
        None
    
    elif inputs == "R4":
        printRespuesta()
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        printRespuesta()

    elif inputs == "R5":
        printRespuesta()
        executiontime = timeit.timeit(optionFifth, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        printRespuesta()
    
    elif inputs == "R6":
        printRespuesta()
        executiontime = timeit.timeit(optionSixth, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        printRespuesta()
    
    elif inputs == "R7":
        printRespuesta()
        executiontime = timeit.timeit(optionSeventh, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        printRespuesta()

    elif inputs == "R8":
        printRespuesta()
        executiontime = timeit.timeit(optionEighth, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
        printRespuesta()
        



    else:
        sys.exit(0)
