class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id 
      (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id 
      (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap 
      (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` 
        attributes should be populated afresh with data from the JSON file. 
        Attribute values from previous imports should not be retained.

        You can use the `json` python package to easily load the JSON file at 
        `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If the file does not exist, no attribute should be 
                populated and no error should be raised.

        Returns:
            None
        """
        # TODO: Complete this method
        import json
        from math import floor, ceil
        from tube.components import Station, Line, Connection
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances
        
        try:
            # Initialise data
            with open(filepath, "r") as jsonfile:
                tube_data = json.load(jsonfile)
                stations_info = tube_data["stations"]
                lines_info = tube_data["lines"]
                connections_info = tube_data["connections"]
                
                for station in stations_info:
                    id, name, zones = station["id"], station["name"], float(station["zone"])
                    floored_zone = floor(zones)  # Transfer the non-integer zones
                    ceiled_zone = ceil(zones)
                    if floored_zone != ceiled_zone:
                        zones = {floored_zone, ceiled_zone}
                    else:
                        zones = {floored_zone}
                    station_instance = Station(id, name, zones)
                    self.stations[f"{id}"] = station_instance
                
                for line in lines_info:
                    id, name = line["line"], line["name"]
                    line_instance = Line(id, name)
                    self.lines[f"{id}"] = line_instance
                
                for connection in connections_info:
                    station1 = self.stations[connection["station1"]]
                    station2 = self.stations[connection["station2"]]
                    stations = {station1, station2}
                    line = self.lines[connection["line"]]
                    time = int(connection["time"])
                    connection_instance = Connection(stations, line, time)
                    self.connections.append(connection_instance)
                
        except FileNotFoundError:
            print("Target file is not found. Please try again.")
            return None


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
