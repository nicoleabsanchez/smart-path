"""
Módulo de algoritmos de grafos para el sistema SmartPath+
Implementa BFS y Dijkstra para optimización de rutas ferroviarias
"""

import heapq
from collections import deque, defaultdict
from typing import Dict, List, Tuple, Optional


class RailwayGraph:
    """
    Clase que representa el grafo de la red ferroviaria del Reino Unido
    """
    
    def __init__(self):
        """Inicializa el grafo con estructuras de datos necesarias"""
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.stations: Dict[str, Dict] = {}
        self.edges_count = 0
        
    def add_station(self, code: str, name: str, city: str, lat: float, lon: float):
        """
        Añade una estación al grafo
        
        Args:
            code: Código único de la estación
            name: Nombre de la estación
            city: Ciudad donde se ubica
            lat: Latitud
            lon: Longitud
        """
        self.stations[code] = {
            'name': name,
            'city': city,
            'lat': lat,
            'lon': lon
        }
    
    def add_edge(self, source: str, target: str, distance: float):
        """
        Añade una arista al grafo (conexión entre estaciones)
        
        Args:
            source: Código de estación origen
            target: Código de estación destino
            distance: Distancia en kilómetros
        """
        self.adjacency_list[source].append((target, distance))
        self.edges_count += 1
    
    def get_station_info(self, code: str) -> Optional[Dict]:
        """Obtiene información de una estación por su código"""
        return self.stations.get(code)
    
    def get_cities(self) -> List[str]:
        """Obtiene lista única de ciudades ordenadas alfabéticamente"""
        cities = set(station['city'] for station in self.stations.values())
        return sorted(list(cities))
    
    def get_stations_by_city(self, city: str) -> List[Tuple[str, str]]:
        """
        Obtiene todas las estaciones de una ciudad
        
        Returns:
            Lista de tuplas (código, nombre)
        """
        stations = [(code, info['name']) 
                   for code, info in self.stations.items() 
                   if info['city'] == city]
        return sorted(stations, key=lambda x: x[1])
    
    def bfs_shortest_path(self, start: str, end: str) -> Tuple[List[str], int]:
        """
        Algoritmo BFS para encontrar el camino con menor número de paradas
        
        Args:
            start: Código de estación origen
            end: Código de estación destino
            
        Returns:
            Tupla (camino, número_de_paradas)
            camino: Lista de códigos de estaciones
            número_de_paradas: Cantidad de estaciones intermedias
        """
        if start not in self.adjacency_list or end not in self.stations:
            return [], 0
        
        if start == end:
            return [start], 0
        
        # Cola para BFS: (nodo_actual, camino_hasta_ahora)
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            # Explorar vecinos
            for neighbor, _ in self.adjacency_list[current]:
                if neighbor in visited:
                    continue
                
                new_path = path + [neighbor]
                
                # Si llegamos al destino, retornamos
                if neighbor == end:
                    return new_path, len(new_path) - 1
                
                visited.add(neighbor)
                queue.append((neighbor, new_path))
        
        # No se encontró camino
        return [], 0
    
    def dijkstra_shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """
        Algoritmo de Dijkstra para encontrar el camino más corto por distancia
        
        Args:
            start: Código de estación origen
            end: Código de estación destino
            
        Returns:
            Tupla (camino, distancia_total)
            camino: Lista de códigos de estaciones
            distancia_total: Distancia en kilómetros
        """
        if start not in self.adjacency_list or end not in self.stations:
            return [], 0.0
        
        if start == end:
            return [start], 0.0
        
        # Distancias iniciales (infinito para todos excepto inicio)
        distances = {station: float('inf') for station in self.stations}
        distances[start] = 0.0
        
        # Para reconstruir el camino
        previous = {}
        
        # Cola de prioridad: (distancia, nodo)
        priority_queue = [(0.0, start)]
        visited = set()
        
        while priority_queue:
            current_distance, current = heapq.heappop(priority_queue)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Si llegamos al destino, reconstruimos el camino
            if current == end:
                path = []
                while current in previous:
                    path.append(current)
                    current = previous[current]
                path.append(start)
                path.reverse()
                return path, distances[end]
            
            # Si la distancia actual es mayor que la registrada, continuar
            if current_distance > distances[current]:
                continue
            
            # Explorar vecinos
            for neighbor, weight in self.adjacency_list[current]:
                distance = current_distance + weight
                
                # Si encontramos un camino más corto
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # No se encontró camino
        return [], 0.0
    
    def find_best_route_between_cities(self, origin_city: str, destination_city: str, 
                                       algorithm: str = 'dijkstra') -> Dict:
        """
        Encuentra la mejor ruta entre dos ciudades considerando todas las combinaciones
        de estaciones posibles
        
        Args:
            origin_city: Ciudad de origen
            destination_city: Ciudad de destino
            algorithm: 'dijkstra' para menor distancia, 'bfs' para menos paradas
            
        Returns:
            Diccionario con información de la mejor ruta encontrada
        """
        origin_stations = self.get_stations_by_city(origin_city)
        destination_stations = self.get_stations_by_city(destination_city)
        
        if not origin_stations or not destination_stations:
            return {
                'found': False,
                'message': 'No se encontraron estaciones en una o ambas ciudades'
            }
        
        best_route = None
        best_metric = float('inf')
        
        # Probar todas las combinaciones de estaciones
        for origin_code, origin_name in origin_stations:
            for dest_code, dest_name in destination_stations:
                if algorithm == 'bfs':
                    path, stops = self.bfs_shortest_path(origin_code, dest_code)
                    metric = stops
                else:  # dijkstra
                    path, distance = self.dijkstra_shortest_path(origin_code, dest_code)
                    metric = distance
                
                # Si encontramos una ruta y es mejor que la actual
                if path and metric < best_metric:
                    best_metric = metric
                    best_route = {
                        'found': True,
                        'origin_station': {'code': origin_code, 'name': origin_name},
                        'destination_station': {'code': dest_code, 'name': dest_name},
                        'path': path,
                        'metric': metric,
                        'algorithm': algorithm
                    }
        
        if best_route is None:
            return {
                'found': False,
                'message': 'No se encontró ninguna ruta entre las ciudades'
            }
        
        return best_route
    
    def get_route_details(self, path: List[str]) -> List[Dict]:
        """
        Obtiene detalles completos de cada estación en una ruta
        
        Args:
            path: Lista de códigos de estaciones
            
        Returns:
            Lista de diccionarios con información de cada estación
        """
        details = []
        for i, code in enumerate(path):
            station_info = self.get_station_info(code)
            if station_info:
                detail = {
                    'step': i + 1,
                    'code': code,
                    'name': station_info['name'],
                    'city': station_info['city']
                }
                
                # Añadir distancia al siguiente nodo si existe
                if i < len(path) - 1:
                    next_code = path[i + 1]
                    # Buscar la distancia en la lista de adyacencia
                    for neighbor, distance in self.adjacency_list[code]:
                        if neighbor == next_code:
                            detail['distance_to_next'] = distance
                            break
                
                details.append(detail)
        
        return details
    
    def calculate_price(self, distance: float) -> float:
        """"
        Calcula el precio estimado del viaje basado en la distancia
        Fórmula: Precio base + (distancia * tarifa por km)
        Precios basados en tarifas promedio de UK rail
        
        Args:
            distance: Distancia en kilómetros
            
        Returns:
            Precio estimado en libras esterlinas (£)
        """
        base_fare = 5.0  # Tarifa base en £
        rate_per_km = 0.15  # £ por kilómetro
        return round(base_fare + (distance * rate_per_km), 2)
    
    def calculate_time(self, distance: float, num_stops: int) -> float:
        """
        Calcula el tiempo estimado del viaje
        Fórmula: (distancia / velocidad promedio) + (paradas * tiempo por parada)
        
        Args:
            distance: Distancia en kilómetros
            num_stops: Número de paradas intermedias
            
        Returns:
            Tiempo estimado en horas
        """
        avg_speed = 80.0  # Velocidad promedio en km/h
        stop_time = 0.05  # 3 minutos por parada en horas
        travel_time = distance / avg_speed
        stop_time_total = (num_stops - 1) * stop_time if num_stops > 1 else 0
        return round(travel_time + stop_time_total, 2)
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del grafo"""
        return {
            'total_stations': len(self.stations),
            'total_connections': self.edges_count,
            'total_cities': len(self.get_cities()),
            'avg_connections_per_station': round(self.edges_count / len(self.stations), 2) if self.stations else 0
        }
