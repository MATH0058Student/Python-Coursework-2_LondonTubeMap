from tube.map import TubeMap
from network.graph import NeighbourGraphBuilder
from network.path import PathFinder

def test():
    test_tube_map = TubeMap()
    test_tube_map.import_from_json("data/london.json")
    
    test_graph_builder_1 = NeighbourGraphBuilder()
    test_graph1 = test_graph_builder_1.build(test_tube_map)
    print(test_graph1["18"]["186"])
    print(test_graph1["186"])
    
    test_path_finder = PathFinder(test_tube_map)
    test_path = test_path_finder.get_shortest_path(None, None)
    print(test_path)
    test_path = test_path_finder.get_shortest_path("Covent Garden", "Covent Garden")
    print(test_path)
    test_path = test_path_finder.get_shortest_path("Holloway Road", "Uxbridge")
    print(test_path)

if __name__ == "__main__":
    test()