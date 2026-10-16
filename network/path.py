from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide 
      your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        
        # Feel free to add anything else needed here.
        
        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use Dijkstra's algorithm to find the shortest path from
        start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, 
        e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: 
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        # TODO: Complete this method
        try:
            # Find the corresponsing ids for start station and end station
            start_station_id = None
            end_station_id = None
            for id, station in self.tubemap.stations.items():
                if station.name == start_station_name:
                    start_station_id = id
                if station.name == end_station_name:
                    end_station_id = id
                if (start_station_id is not None) and (end_station_id is not None):
                    break
            
            # start_station_name or end_station_name does not exist
            if (start_station_id is None) or (end_station_id is None):
                return None
            
            # start_station_name and end_station_name are the same
            if start_station_id == end_station_id:
                return [self.tubemap.stations[start_station_id]]
            
            # Initialise the Dijkstra's algorithm
            import heapq
            dist = {station_id:float("inf") for station_id in self.tubemap.stations}
            dist[start_station_id] = 0
            predecessor_dict = {station_id: None for station_id in self.tubemap.stations}
            priority_queue = [(0, start_station_id)]
            
            while priority_queue:
                current_time, station_id = heapq.heappop(priority_queue)
                # Skip if we already finalised this station
                if current_time>dist[station_id]:
                    continue
                # Early exit when we reach the destination
                if station_id == end_station_id:
                    break
                
                # Explore the neighbour
                for neighbour_station_id in self.graph[station_id]:
                    connections = self.graph[station_id][neighbour_station_id]
                    
                    # Get the fastest connection
                    connection = min(connections, key=lambda connection: connection.time)
                    new_time = current_time + connection.time
                    
                    if new_time<dist[neighbour_station_id]:
                        dist[neighbour_station_id] = new_time
                        predecessor_dict[neighbour_station_id] = station_id
                        heapq.heappush(priority_queue, (new_time, neighbour_station_id))
            
            if dist[end_station_id] == float("inf"):
                return f"There is no path from {start_station_name} to {end_station_name}."
            
            # Make list of Station objects corresponding to shortest path
            # from end_station_name to start_station_name by tracking predecessor_dict.
            path = []
            current_id = end_station_id
            while current_id is not None:
                path.append(self.tubemap.stations[current_id])
                current_id = predecessor_dict[current_id]
            
            # Reverse the list
            path = path[::-1]
            
            return path
            
        except KeyError:
            return None


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
   
    assert stations is not None

    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected


if __name__ == "__main__":
    test_shortest_path()
