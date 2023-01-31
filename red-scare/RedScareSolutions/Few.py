from RedScareSolutions.Helpers.interface import ProblemInterface
from RedScareSolutions.Helpers.input_helper import info_store, graph_type
import heapq


class FewProblem(ProblemInterface):

    def get_result(self):
        # Small optimisation for graphs that have no edges.
        if info_store.get_graph_type() == graph_type.NONE:
            return -1

        r_graph = info_store.get_original_graph()

        # Change weights of nodes
        new_graph = self.change_weights(r_graph)

        # Get shortest path
        dist = self.dijkstra(new_graph, info_store.get_source_id(), info_store.get_destination_id())

        # Add one to dist if source is red
        if (info_store.dictionary_by_id[info_store.get_source_id()][1]):
            dist = dist + 1
        return dist

    def change_weights(self, graph):
        for x in range(len(graph)):
            for y in range(len(graph[x])):
                current_pos = graph[x][y]
                if not info_store.dictionary_by_id[current_pos[0]][1]:
                    current_pos[1] = 0

        return graph

    def dijkstra(self, graph, start, end):
        heap = [(0, start)]
        visited = set()
        while heap:
            (cost, u) = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            if u == end:
                return cost
            for node in graph[u]:
                if node[0] in visited:
                    continue
                next_item = cost + node[1]
                heapq.heappush(heap, (next_item, node[0]))
        return -1
