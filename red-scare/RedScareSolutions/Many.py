from collections import deque
from RedScareSolutions.Helpers.interface import ProblemInterface
from RedScareSolutions.Helpers.input_helper import info_store, graph_type

class ManyProblem(ProblemInterface):

    def get_result(self):
        # Small optimisation for graphs that have no edges.
        if info_store.get_graph_type() == graph_type.NONE:
            return -1

        org_graph = info_store.get_original_graph()
        start = info_store.get_source_id()
        end = info_store.get_destination_id()

        result = self.BFS_longest_path(org_graph, start, end)

        return result

    # Algorithm for undirected graph
    def bfs(self, graph, source, end):

        traverse_initial = [False for _ in range(len(graph))]

        # We start at the source. Mark source as visited and add it to a queue.
        traverse_initial[source] = True

        max_cost = -1
        queue = deque([(source, 0, traverse_initial, source)])

        while queue:

            current_node, cost, traversed, parent = queue.popleft()
            # Check if current node is red.
            if info_store.dictionary_by_id[current_node][1]:
                new_cost = cost + 1
            else:
                new_cost = cost

            for index in range(len(graph[current_node])):
                # Check if we reached destination, if we have -> check if red node is red and then get max
                if graph[current_node][index][0] == end:

                    if info_store.dictionary_by_id[end][1]:
                        new_cost = new_cost + 1

                    max_cost = max(max_cost, new_cost)
                # If we have not reached the destination, and we have not traversed the node. We add the node to queue.
                if not traversed[graph[current_node][index][0]] and graph[current_node][index][0] != end:
                    traversed[graph[current_node][index][0]] = True

                    queue.append((graph[current_node][index][0], new_cost, traversed, current_node))
                elif parent != graph[current_node][index][0] and graph[current_node][index][0] != source and graph[current_node][index][0] != end:
                    print("Graph is cyclic. Skipping for many and some.")
                    return -1
        return max_cost

    def BFS_longest_path(self, graph, start, end):

        distance = self.bfs(graph, start, end)  # type: ignore

        #print('Maximum Red nodes from node', info_store.get_source(), 'to node', info_store.get_destination(), 'is',
         #     distance)
        return distance
