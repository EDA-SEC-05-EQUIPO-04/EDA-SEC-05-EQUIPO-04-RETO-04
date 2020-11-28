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
from DISClib.ADT import stack
import config
from DISClib.DataStructures import edge as ed
from DISClib.ADT import stack as st
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.ADT import minpq as mq
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfo
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import datetime
from math import radians, cos, sin, asin, sqrt 
assert config

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def newAnalyzer():

    try:
        analyzer = {
                    'connections': None,
                    'paths': None,
                    'location':None,
                    'stations':None,
                    }


        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=768,
                                              comparefunction=compareStopIds)
        analyzer['stations']=m.newMap(numelements=1536,
                                      maptype = "PROBING",
                                      loadfactor=0.5,
                                      comparefunction=compareStopIds)

        analyzer['location'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def seeTime(timeDate1, timeDate2):
    hour1 = int(timeDate1[0:2])
    hour2 = int(timeDate2[0:2])
    minutes1 = int(timeDate1[3:6]) +hour1*60
    minutes2 = int(timeDate2[3:6])+hour2*60
    return minutes2-minutes1

def addTrip(citibike, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
        
def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    
    if not gr.containsVertex(citibike['connections'], stationid):
        gr.insertVertex(citibike['connections'], stationid)
    return citibike

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    
    if origin != destination:
        edge = gr.getEdge(citibike ["connections"], origin, destination)

        if edge is None:
            if m.get(citibike["stations"], origin) is None:
                repetitions = m.newMap(numelements=1536,
                                    maptype="PROBING", 
                                    loadfactor=0.5, 
                                    comparefunction=compareStopIds)
                m.put(citibike["stations"],origin, repetitions)
            repetitions = me.getValue(m.get(citibike["stations"], origin))
            m.put(repetitions,destination, [duration, 1])
            gr.addEdge(citibike["connections"], origin, destination, duration)
        else:
            one_rep = m.get(citibike["stations"],origin)
            repetitions = me.getValue(one_rep)
            two_rep = m.get(repetitions, destination)
            repetitions_destination = me.getValue(two_rep)
            repetitions_destination[0]+=duration
            repetitions_destination[1]+=1
            duration = repetitions_destination[0]/repetitions_destination[1]
            ed.weight(edge)
    return citibike


def addComponents(citibike):
    citibike['components'] = scc.KosarajuSCC(citibike['connections'])

# ==============================
# Funciones de consulta
# ==============================

def getElement(entry):
    try:
        return me.getValue(entry)
    except:
        return None


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def criticalStations(analyzer):
    vertexs = gr.vertices(analyzer["connections"])
    indegree = mq.newMinPQ(compareinverted)
    outdegree = mq.newMinPQ(compareinverted)
    degree = mq.newMinPQ(comparenormal)
    iterator = it.newIterator(vertexs)
    res1 = lt.newList()
    res2 = lt.newList()
    res3 = lt.newList()
    while it.hasNext(iterator):
        element = it.next(iterator)
        ins = (element,int(gr.indegree(analyzer["connections"],element)))
        out = (element,int(gr.outdegree(analyzer["connections"],element)))
        deg = (element,int(gr.indegree(analyzer["connections"],element))+int(gr.outdegree(analyzer["connections"],element)))
        mq.insert(indegree,ins)
        mq.insert(outdegree,out)
        mq.insert(degree,deg)

    for a in range(1,4):
        lt.addLast(res1,mq.delMin(indegree))
        lt.addLast(res2,mq.delMin(outdegree))
        lt.addLast(res3,mq.delMin(degree)) 
        
    return (res1,res2,res3)

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    
    try:
        addTrip(stop, keyvaluestop)
    except:
        print("error")

def compareStopIds(stop, keyvaluestop):
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

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def comparenormal(tup1, tup2):
    num1 = tup1[1]
    num2 = tup2[1]
    if (num1 == num2):
        return 0
    elif (num1 > num2):
        return 1
    else:
        return -1
        
def compareinverted(tup1, tup2):
    num1 = tup1[1]
    num2 = tup2[1]
    if (num1 == num2):
        return 0
    elif (num1 > num2):
        return -1
    else:
        return 1