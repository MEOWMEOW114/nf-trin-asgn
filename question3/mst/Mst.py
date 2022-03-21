import sys

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices


        # initialize adjacency matrix with zeros

        # |   | A | B | C | D | E |
        # | ----------------------|
        # | A | 0 | 0 | 0 | 0 | 0 |
        # | ----------------------|
        # | B | 0 | 0 | 0 | 0 | 0 |
        # | ----------------------|
        # | C | 0 | 0 | 0 | 0 | 0 |
        # | ----------------------|
        # | D | 0 | 0 | 0 | 0 | 0 |
        # | ----------------------|
        # | E | 0 | 0 | 0 | 0 | 0 |
        self.adj_matrix = [[0 for column in range(vertices)] 
            for row in range(vertices)]

    def add_edge(self, node1, node2, weight):
        self.adj_matrix[node1][node2] = weight
        self.adj_matrix[node2][node1] = weight



def prims_mst(graph: Graph):
    vertices = graph.vertices

    selected_nodes = [False for _ in range(vertices)]

    result = [[0 for column in range(vertices)] 
                for row in range(vertices)]
    
    for i in range(vertices):
        print(graph.adj_matrix[i])
    
    print(selected_nodes)

    break_count = 0
    # While there are vertics not included in the MST, keep looping:
    while(False in selected_nodes):
        break_count = break_count + 1
        # Initialize min value
        minimum = sys.maxsize

        # The starting vertic
        start = 0

        # The ending vertic
        end = 0

        for i in range(vertices):
            # If the node is part of the MST, look its relationships
            if selected_nodes[i]:
                for j in range(vertices):
                  
                    # If the vertic have a path to the ending node AND its not included in the MST (to avoid cycles)
                    # If the weight path analized is less than the minimum of the MST
                    vertic_has_path_to_ending_node = selected_nodes[j]  == False
                    path_exist_to_ending_vertic = graph.adj_matrix[i][j] > 0
                    weigh_path_less_than_min =  graph.adj_matrix[i][j] < minimum

                    if ( vertic_has_path_to_ending_node and path_exist_to_ending_vertic and weigh_path_less_than_min ):  
                        if graph.adj_matrix[i][j] < minimum:
                            # Defines the new minimum weight, the starting vertex and the ending vertex
                            minimum = graph.adj_matrix[i][j]
                            start, end = i, j
        
        if break_count > vertices * vertices:
            # means no solution
            return -1

    
    # selected becase we added the ending vertex to the MST
        selected_nodes[end] = True

        result[start][end] = minimum
        
        if minimum ==  sys.maxsize:
            result[start][end] = 0

        print("Edge: %d - %d, Weight: %d" % ( start, end, result[start][end]))
        
        result[end][start] = result[start][end]

    # Print the resulting MST
    # for node1, node2, weight in result:

    sum = 0
    for i in range(len(result)):
        for j in range(0+i, len(result)):
            if result[i][j] != 0:
                sum = sum + result[i][j]
                print("%d - %d: %d" % (i, j, result[i][j]))
    return sum


if __name__ == "__main__":
    example_graph = Graph(9)

    example_graph.add_edge(0, 1, 4)
    example_graph.add_edge(0, 2, 7)
    example_graph.add_edge(1, 2, 11)
    example_graph.add_edge(1, 3, 9)
    example_graph.add_edge(1, 5, 20)
    example_graph.add_edge(2, 5, 1)
    example_graph.add_edge(3, 6, 6)
    example_graph.add_edge(3, 4, 2)
    example_graph.add_edge(4, 6, 10)
    example_graph.add_edge(4, 8, 15)
    example_graph.add_edge(4, 7, 5)
    example_graph.add_edge(4, 5, 1)
    example_graph.add_edge(5, 7, 3)
    example_graph.add_edge(6, 8, 5)
    example_graph.add_edge(7, 8, 12)
    prims_mst(example_graph)