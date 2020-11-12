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
import config
from App import controller
from DISClib.ADT import stack
import timeit
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
    else:
        sys.exit(0)
