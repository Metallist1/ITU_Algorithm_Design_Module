from collections import deque

from RedScareSolutions.Helpers.interface import ProblemInterface
from RedScareSolutions.Helpers.input_helper import info_store, graph_type


class AlternativeProblem(ProblemInterface):

    # 1. Given instance of x (P1)
    # 2. Create instance of y (P2)
    # 3. Use algorith to solve y to get solution2 for P2
    # 4. Deduce solution S for P1 = solution 2 for P2
    def get_result(self):
        # Small optimisation for graphs that have no edges.
        if info_store.get_graph_type() == graph_type.NONE:
            return False

        r_graph = info_store.get_original_graph()
        # Create graph y.
        new_graph = self.input_processing(r_graph)
        # We use algorithm to get shortest path (or any path)
        path_exists = self.BFS(new_graph, info_store.get_source_id(), info_store.get_destination_id())

        return path_exists

    def input_processing(self, graph):
        # print out all saturated nodes that are from a reachable node to non reachable node
        for x in range(len(graph)):
            for y in range(len(graph[x])):
                current_pos = graph[x][y]
                if current_pos[1] != 0 and info_store.compare_type_by_id(x, current_pos[0]):
                    current_pos[1] = 0
                    if info_store.get_graph_type() == graph_type.UNDIRECTED:
                        id_of_y = current_pos[0]
                        graph[id_of_y][info_store.get_node_position(x, current_pos[0])][1] = 0
        return graph

    # We execute a Breadth-first search to find a specific path that matches our criteria
    def BFS(self, graph, source, destination):
        # Mark all the nodes as not visited. (We will visit nodes and append them to path P
        traversed = [False for _ in range(len(graph))]

        # We start at the source. Mark source as visited and add it to a queue.
        traversed[source] = True
        queue = deque([source])

        # While we got some place to visit.
        while queue:

            # Take first element of queue
            current_node = queue.popleft()
            # Traverse graph
            for index in range(len(graph[current_node])):
                capacity = graph[current_node][index][1]

                if not traversed[graph[current_node][index][0]] and capacity > 0:
                    if graph[current_node][index][0] == destination:
                        return True

                    traversed[graph[current_node][index][0]] = True
                    queue.append(graph[current_node][index][0])

        # We cant reach the destination. Thus, we stop.
        return False
