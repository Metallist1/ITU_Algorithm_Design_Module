import sys
import math


if len(sys.argv) >= 2:
    file_name = sys.argv[1]
else:
    file_name = "./data/rail.txt"


def get_input():
    id_of_node = []
    with open(file_name, 'r') as f:
        # First value
        number_of_nodes = int(f.readline())

        graph = [[0 for _ in range(number_of_nodes)]
                 for _ in range(number_of_nodes)]

        for i in range(number_of_nodes):
            id_of_node.append(f.readline().strip())

        number_of_archs = int(f.readline())

        for i in range(number_of_archs):
            word = [int(x) for x in f.readline().strip().split()]

            # value is infinite or undefined. We change it to infinite.
            if word[2] == -1:
                word[2] = math.inf

            # values are undirected, thus it means they are both sided.
            graph[word[0]][word[1]] = word[2]
            graph[word[1]][word[0]] = word[2]

    return graph, id_of_node.index('ORIGINS'), id_of_node.index('DESTINATIONS')

# We execute a Breadth-first search to find a specific path that matches our criteria
def check_if_path_exists(graph, source, destination):
    # Initialise a path array.
    new_path = [-1 for _ in range(len(graph))]

    # Mark all the nodes as not visited. (We will visit nodes and append them to path P
    traversed = [False for _ in range(len(graph))]

    # We start at the source. Mark source as visited and add it to a queue.
    traversed[source] = True
    queue = [source]

    # While we got some place to visit.
    while queue:

        # Take first element of queue
        current_node = queue.pop(0)

        # Traverse graph
        for index in range(len(graph[current_node])):
            capacity = graph[current_node][index]

            # if the current node is not visited and its capacity is above 0.
            # if capacity is 0 or < 0 , this node is not connected or at peak saturation thus can be ignored.
            # However, some nodes have -1 for data.
            # This is not a problem as we switched -1 to float.inf during the data import. Thus all values are positive
            if not traversed[index] and capacity > 0:
                # We add the currently visited node to the Path.
                # Note, path will not contain the exact path. But will contain the next point to traverse.
                new_path[index] = current_node
                # If we reached our destination. Return true and the path
                if index == destination:
                    return True, new_path

                # For each place we visit. We mark that we visited it. And add it to the queue.
                traversed[index] = True
                queue.append(index)

    # We cant reach the destination. Thus, we stop.
    return False, new_path


# Returns the maximum flow and residual graph from s to t in the given graph
def ford_fulkerson(graph, source, destination):
    # create a residual graph based on the original graph. (Original graph should be preserved for finding out cuts)
    graph_f = [i[:] for i in graph]

    max_flow = 0  # There is no flow initially

    while True:
        # Check if path exists and get path.
        path_exists, path_p = check_if_path_exists(graph_f, source, destination)

        if not path_exists:
            break

        # Given residual graph f, a path and source, destination. Find out the minimum bottleneck.
        # Or in other terms. Find the max flow.
        path_flow = find_max_flow(graph_f, path_p, source, destination)

        # Add to max_flow
        max_flow += path_flow

        # Update graph f by updating residual capacities on edges.
        # This is done by traversing the path from destination to the source and updating as we go along.
        graph_f = update_graph(graph_f, path_p, source, destination, path_flow)


    return max_flow, graph_f



# Depth First Search algorithm.
# We use it to find all reachable nodes from s. We can use BFS for this as well.
def dfs(graph, s, visited):
    visited[s] = True
    for i in range(len(graph)):
        if graph[s][i] > 0 and not visited[i]:
            dfs(graph, i, visited)



def output(x, y, c):
    with open("./data/output.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(str(x) + " " + str(y) + " " + str(c))


def find_max_flow(graph_f, path, source, destination):
    path_flow = float("Inf")
    s = destination

    while s != source:
        path_flow = min(path_flow, graph_f[path[s]][s])
        s = path[s]

    return path_flow


def update_graph(graph_f, path, source, current_point, path_flow):
    while current_point != source:
        next_point = path[current_point]
        graph_f[next_point][current_point] -= path_flow
        graph_f[current_point][next_point] += path_flow
        current_point = path[current_point]

    return graph_f


def get_minimum_cuts(original_graph, graph_f, source):
    minimum_cuts = []
    traversed = [False for _ in range(len(graph_f))]
    dfs(graph_f, source, traversed)

    # print out all saturated nodes that are from a reachable node to non reachable node
    for x in range(len(original_graph)):
        for y in range(len(original_graph[0])):
            if original_graph[x][y] > 0 and graph_f[x][y] == 0 and traversed[x] and not traversed[y]:
                minimum_cuts.append([x, y, original_graph[x][y]])

    return minimum_cuts


def initial_setup():
    graph, source, destination = get_input()

    # Get residual graph and max_flow from ford_fulkerson
    max_path, graph_f = ford_fulkerson(graph, source, destination)
    print("max flow: " + str(max_path))

    # max flow = min flow. We try to find out what cuts do we make to divide the graph into two partitions
    minimum_cuts = get_minimum_cuts(graph, graph_f, source)

    for i in range(len(minimum_cuts)):
        print(minimum_cuts[i][0], minimum_cuts[i][1], minimum_cuts[i][2])
        output(minimum_cuts[i][0], minimum_cuts[i][1], minimum_cuts[i][2])


initial_setup()
