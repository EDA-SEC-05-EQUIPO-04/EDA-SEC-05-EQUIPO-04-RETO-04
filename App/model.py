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
from DISClib.ADT.map import newMap
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs
from DISClib.Utils import error as error
from math import floor
import numpy as np
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""
anoactual=2020
# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador
   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        citybike = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    'graph':None,
                    'distance':None,
                    'ages1':None,
                    'ages2':None,
                    'adjacente1':None,
                    'adjacente2':None
                    }

        citybike['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        citybike['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        citybike['graph']=gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=1000,
             comparefunction=compareStations
        
             )       
        citybike['distance']=m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds) 
        citybike['ages1']=gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=10,
             comparefunction=compareStopIds
        
             )       
        citybike['ages2']=gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=10,
             comparefunction=compareStopIds
        
             )      
        citybike['adjacente1']=gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=1000,
             comparefunction=compareStopIds
        
             )  
        citybike['adjacente2']=gr.newGraph(datastructure="ADJ_LIST",
             directed=True,
             size=1000,
             comparefunction=compareStopIds
        
             )     
        for i in range(0,7):
                gr.insertVertex(citybike['ages1'],str(i))
                gr.insertVertex(citybike['ages2'],str(i))
        gr.insertVertex(citybike['ages2'],"salida") 
        gr.insertVertex(citybike['ages1'],"salida")   

        for i in range(0,7):
                gr.insertVertex(citybike['adjacente1'],str(i))
                gr.insertVertex(citybike['adjacente2'],str(i))
        gr.insertVertex(citybike['adjacente2'],"salida") 
        gr.insertVertex(citybike['adjacente1'],"salida")       
                                             
        return citybike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo
def addTrip(citibike, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    latitude=trip['start station latitude']
    longitude=trip['start station longitude']
    latitude2=trip['end station latitude']
    longitude2=trip['end station longitude']
    tipousuario=trip['usertype']
    edad=anoactual-int(trip['birth year'])
    edad=int(np.floor(edad/10))
    if edad >6:
        edad =6
    if tipousuario=="Customer":
        addAdjacent(citibike,edad,origin)
        addAdjacent2(citibike,edad,origin)

    addStation(citibike, origin)
    addStation(citibike, destination)
    addAge(citibike,edad,origin)
    addAge2(citibike,edad,destination)
    addConnection(citibike, origin, destination, duration)
    addDistance(citibike,origin,latitude,longitude)
    addDistance2(citibike,destination,latitude2,longitude2)

def addAdjacent(citibike,edad,station):
    if not gr.containsVertex(citibike['adjacente1'], station):
            gr.insertVertex(citibike['adjacente1'], station)
            gr.addEdge(citibike['adjacente1'],station,"salida",0)
    else:
        edge = gr.getEdge(citibike['adjacente1'], str(edad),station)
        if edge is None:
            gr.addEdge(citibike['adjacente1'],str(edad),station,1)
            gr.addEdge(citibike['adjacente1'],station,"salida",0)
        else:    
            peso=edge['weight']
            if peso!=0:
                gr.removeVertex(citibike['adjacente1'],station)
                gr.removeVertex(citibike['adjacente1'],str(edad))
                gr.insertVertex(citibike['adjacente1'], station)
                gr.insertVertex(citibike['adjacente1'], str(edad))
                gr.addEdge(citibike['adjacente1'],station,"salida",0)
                gr.addEdge(citibike['adjacente1'], str(edad), station, 1/(1+1/peso))
            else:
                print("El peso es 0")

def addAdjacent2(citibike,edad,station):
    if not gr.containsVertex(citibike['adjacente2'], station):
            gr.insertVertex(citibike['adjacente2'], station)
            gr.addEdge(citibike['adjacente2'],station,"salida",0)
    else:
        edge = gr.getEdge(citibike['adjacente2'], str(edad),station)
        if edge is None:
            gr.addEdge(citibike['adjacente2'],str(edad),station,1)
            gr.addEdge(citibike['adjacente2'],station,"salida",0)
        else:    
            peso=edge['weight']
            if peso!=0:
                gr.removeVertex(citibike['adjacente2'],station)
                gr.removeVertex(citibike['adjacente2'],str(edad))
                gr.insertVertex(citibike['adjacente2'], station)
                gr.insertVertex(citibike['adjacente2'], str(edad))
                gr.addEdge(citibike['adjacente2'],station,"salida",0)
                gr.addEdge(citibike['adjacente2'], str(edad), station, 1/(1+1/peso))
            else:
                print("El peso es 0")
       
def addAge(citibike,edad,station):
    if not gr.containsVertex(citibike['ages1'], station):
            gr.insertVertex(citibike['ages1'], station)
            gr.addEdge(citibike['ages1'],station,"salida",0)
    else:
        edge = gr.getEdge(citibike['ages1'], str(edad),station)
        if edge is None:
            gr.addEdge(citibike['ages1'],str(edad),station,1)
            gr.addEdge(citibike['ages1'],station,"salida",0)
        else:    
            peso=edge['weight']
            if peso!=0:
                gr.removeVertex(citibike['ages1'],station)
                gr.removeVertex(citibike['ages1'],str(edad))
                gr.insertVertex(citibike['ages1'], station)
                gr.insertVertex(citibike['ages1'], str(edad))
                gr.addEdge(citibike['ages1'],station,"salida",0)
                gr.addEdge(citibike['ages1'], str(edad), station, 1/(1+1/peso))
            else:
                print("El peso es 0")
            
def addAge2(citibike,edad,station):
    if not gr.containsVertex(citibike['ages2'], station):
            gr.insertVertex(citibike['ages2'], station)
            gr.addEdge(citibike['ages2'],station,"salida",0)
    else:
        edge = gr.getEdge(citibike['ages2'], str(edad),station)
        if edge is None:
            gr.addEdge(citibike['ages2'],str(edad),station,1)
            gr.addEdge(citibike['ages2'],station,"salida",0)
        else:    
            peso=edge['weight']
            if peso!=0:
                gr.removeVertex(citibike['ages2'],station)
                gr.removeVertex(citibike['ages2'],str(edad))
                gr.insertVertex(citibike['ages2'], station)
                gr.insertVertex(citibike['ages2'], str(edad))
                gr.addEdge(citibike['ages2'],station,"salida",0)
                gr.addEdge(citibike['ages2'], str(edad), station, 1/(1+1/peso))
            else:
                print("El peso es 0")

def addDistance(citibike,station,latitude,longitude):
    coordinates={'latitud':latitude,'longitud':longitude}
    m.put( citibike['distance'],station,coordinates)

def addDistance2(citibike,station,latitude,longitude):
    coordinates={'latitud':latitude,'longitud':longitude}
    m.put( citibike['distance'],station,coordinates)

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike['graph'], stationid):
            gr.insertVertex(citibike['graph'], stationid)
    return citibike

def addConnection(citybike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citybike['graph'], origin, destination)
    if edge is None:
        gr.addEdge(citybike['graph'], origin, destination, duration)
    return citybike

# ==============================
# Funciones de consulta
# ==============================
def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(sc, station1, station2):
    return scc.stronglyConnected(sc, station1, station2)

def fourthRequirement(analyzer,station,resistencia,resistenciamin):
    #Se recorren todos los nodos del grafo.
    grafo=analyzer['graph']
    recorrido=m.keySet(dfs.DepthFirstSearch(grafo,station)['visited'])
    iterator=it.newIterator(recorrido)
    rutas=lt.newList()
    while it.hasNext(iterator):
        element=it.next(iterator)
        mpa=djk.Dijkstra(grafo,station)
        if djk.hasPathTo(mpa,element):
            distance=djk.distTo(mpa,element)
            if int(distance)<=int(resistencia) and int(distance)>=int(resistenciamin)  :
                lt.addLast(rutas, djk.pathTo(mpa,element))
            else:
                a=1
    if lt.isEmpty(rutas):
        return None
    return rutas
    """
    distancia=djk.distTo(station,station2)
    if distancia <= resistencia:
        add....
    """
    return None

def fifthRequirement(analyzer,edad):
    grafo1=analyzer['ages1']
    grafo2=analyzer['ages2']
    mpa1=djk.Dijkstra(grafo1,str(edad))
    mpa2=djk.Dijkstra(grafo2,str(edad))
    res1=lt.firstElement(djk.pathTo(mpa1,"salida"))['vertexB']
    res2=lt.firstElement(djk.pathTo(mpa2,"salida"))['vertexB']
    mpa1=djk.Dijkstra(analyzer['graph'],res1)
    ruta=djk.pathTo(mpa1,res2)
    iterator=it.newIterator(ruta)
    ruta=res1
    while it.hasNext(iterator):
            element=it.next(iterator)
            estacion=element['vertexB']
            ruta+="-"+estacion    
    print("Los usuarios con edad en los {}'s les gusta iniciar en la estación {} y terminar en la estación {}. Se recomienda la ruta siguiente: {}".format(int(edad)*10,res1,res2,ruta))

    return None

def sixthRequirement(analyzer,latitud,longitud,latitud2,longitud2):
    grafo=analyzer['graph']
    station1=getCloserStation(analyzer,latitud,longitud)
    station2=getCloserStation(analyzer,latitud2,longitud2)
    mpa=djk.Dijkstra(grafo,station1)
    ruta=None
    distance=-1
    if djk.hasPathTo(mpa,station2):
        distance=djk.distTo(mpa,station2)
        ruta=djk.pathTo(mpa,station2)
    dict={"ruta":ruta,"origen":station1,"destino":station2,"duracion":distance}
    return dict

def seventhRequirement(analyzer,edad):
    grafo1=analyzer['adjacente1']
    grafo2=analyzer['adjacente2']
    mpa1=djk.Dijkstra(grafo1,str(edad))
    mpa2=djk.Dijkstra(grafo2,str(edad))
    res1=lt.firstElement(djk.pathTo(mpa1,"salida"))['vertexB']
    res2=lt.firstElement(djk.pathTo(mpa2,"salida"))['vertexB']
    lista1=gr.adjacents(analyzer['graph'],res1)
    iterator=it.newIterator(lista1)
    while it.hasNext(iterator):
        element=it.next(iterator)
        if gr.containsVertex(grafo2,element):
            peso=min(djk.distTo(mpa2,res2),djk.distTo(mpa1,res1))
            return {'vertexA':res1,'vertexB':element,'weight':peso}
        
    return None



    print("Los usuarios con edad en los {}'s les gusta iniciar en la estación {} y terminar en la estación {}. Se recomienda la ruta siguiente: {}".format(int(edad)*10,res1,res2,ruta))

    return None

def eighthRequirement(cont,id,fecha):
    datos=buscadorId(cont,id)

    return None

# ==============================
# Funciones Helper
# ==============================
def getCloserStation(analyzer,latitud,longitud):
    grafo=analyzer['graph']
    vertice=str(72)
    recorrido=m.keySet(dfs.DepthFirstSearch(grafo,vertice)['visited'])
    iterator=it.newIterator(recorrido)
    distance=float('inf') 
    closer=0
    while it.hasNext(iterator):
        element=it.next(iterator)
        coordinates=m.get(analyzer['distance'],element)['value']
        if coordinates==None:
            a=1
        else:
            distancia=dinstancefunction(np.radians(float(coordinates['latitud'])),np.radians(float(coordinates['longitud'])),float(latitud),float(longitud))
            if distance>=distancia:
                distance=distancia
                closer=element
    return closer

def buscadorId(cont,id):
    return None
# ==============================
# Funciones de Comparacion
# ==============================
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

def compareStopIds2(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop < stopcode):
        return 1
    else:
        return -1

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

def dinstancefunction(lat1,lon1,lat2,lon2):
    R=3958.8
    return np.arccos(np.sin(lat1)*np.sin(lat2)+np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2))*R

