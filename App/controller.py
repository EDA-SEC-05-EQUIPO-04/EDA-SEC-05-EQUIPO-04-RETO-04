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

from App.model import newAnalyzer
import config as cf
from App import model
import csv
import os


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(citybike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(citybike, filename)
    return citybike

def loadFile(citybike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citybike, trip)
    return citybike



# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)

def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)

def sameCC(analyzer,station1,station2):
    """
    """
    return model.sameCC(analyzer['components'],station1,station2)

def fourthRequirement(analyzer,station,resistencia, resistenciamin):
    """
    Numero de componentes fuertemente conectados
    """
    return model.fourthRequirement(analyzer,station,resistencia,resistenciamin)

def fifthRequirement(cont,rango):
    return model.fifthRequirement(cont,rango)

def sixthRequirement(cont,latitud,longitud,latitud2,longitud2):

    return model.sixthRequirement(cont,latitud,longitud,latitud2,longitud2)

def seventhRequirement(cont,rango):
    return model.seventhRequirement(cont,rango)

def eighthRequirement(cont,id,fecha):
    return model.eighthRequirement(cont,id,fecha)
def Function2(analyzer, time1, time2, stationid):
    return model.Function2(analyzer, time1, time2, stationid)
