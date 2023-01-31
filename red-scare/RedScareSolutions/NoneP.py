import heapq
from RedScareSolutions.Helpers.interface import ProblemInterface
from RedScareSolutions.Helpers.input_helper import info_store, graph_type


class NoneProblem(ProblemInterface):

    # This method initialises the problem and should return the result to the problem.
    def get_result(self):
        # Small optimisation for graphs that have no edges.
        if info_store.get_graph_type() == graph_type.NONE:
            return -1

        graph = info_store.get_original_graph()
        dict = info_store.dictionary_by_name
        # remove red vertices
        graph = self.remove_red(graph, dict)
        # find shortest path from s to t
        dist = self.shortest_path(graph, info_store.get_source_id(), info_store.get_destination_id())
        return dist

    def remove_red(self, graph, dict):
        # list of red vertices to delete
        delete = [dict[vertex][0] for vertex in dict if dict[vertex][1]]
        # print(delete)
        # remove them from graph
        for j in reversed(range(len(graph))):
            for i in reversed(range(len(delete))):
                
                # remove this vertex from graph
                if j == delete[i]:
                    graph[j].clear()
                    continue

                # remove its connections (if any)
                for k in reversed(range(len(graph[j]))):
                    if delete[i] == graph[j][k][0]:
                        graph[j].pop(k)

        return graph

    def shortest_path(self, graph, start, end):
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
