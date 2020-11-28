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
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
import timeit
assert config
import datetime

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


def optionTwo():
    print("\nCargando información....")

    controller.loadTrips(cont)

    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def optionFive():
    critical = controller.criticalStations(cont)
    print("\nLas estaciones Top de llegada: \n")
    iterator = it.newIterator(critical[0])
    while it.hasNext(iterator):
        a = it.next(iterator)
        print("La estación {0} con {1} llegadas.".format(a[0],a[1]))
    
    print("\nLas estaciones Top de salida: \n")
    iterator = it.newIterator(critical[1])
    while it.hasNext(iterator):
        a = it.next(iterator)
        print("La estación {0} con {1} salidas.".format(a[0],a[1]))

    print("\nLas estaciones menos concurridas: \n")
    iterator = it.newIterator(critical[2])
    while it.hasNext(iterator):
        a = it.next(iterator)
        print("La estación {0} con {1} llegadas y salidas.".format(a[0],a[1]))
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    

    else:
        sys.exit(0)
sys.exit(0)