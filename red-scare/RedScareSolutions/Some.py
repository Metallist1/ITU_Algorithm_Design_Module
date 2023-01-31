import maxflow
from RedScareSolutions.Helpers.interface import ProblemInterface
from RedScareSolutions.Helpers.input_helper import info_store, graph_type


class SomeProblem(ProblemInterface):
    def __init__(self):
        self.RED_WEIGHT = 2

    def get_result(self):
        if info_store.get_graph_type() == graph_type.NONE:
            return False

        if info_store.is_cyclic():
            return False

        return self.has_red_in_path()

    def input_processing(self):
        residual_graph = info_store.get_original_graph()

        amount_of_nodes = len(residual_graph)

        residual_graph = self._add_weights(residual_graph)

        return residual_graph, amount_of_nodes

    def has_red_in_path(self):
        residual_graph, amount_of_nodes = self.input_processing()
        t = info_store.get_destination_id()
        red_nodes = self._get_all_red_nodes(residual_graph)

        # Creates a new mf graph where red is the new source
        # and creates a new super sink between the original soure and the target.
        for red_node in red_nodes:
            # The library does not support deepcopy
            node_ids, mf_graph = self._create_default_mf_graph(residual_graph, amount_of_nodes)
            s = node_ids[info_store.get_source_id()]

            # Add red as new s
            mf_graph.add_tedge(red_node, 2, 0)

            # Connect s and t to new t'
            mf_graph.add_tedge(s, 0, 1)
            mf_graph.add_tedge(t, 0, 1)

            flow = mf_graph.maxflow()
            if flow == self.RED_WEIGHT:
                return True

        return False

    def _create_default_mf_graph(self, graph, amount_of_nodes):
        mf_graph = maxflow.Graph[float]()
        node_ids = mf_graph.add_nodes(amount_of_nodes)

        s = node_ids[info_store.get_source_id()]

        for id_row, row in enumerate(graph):
            for id_column, column in enumerate(row):
                if column[1] > 0:
                    id_of_y = column[0]
                    opposite_edge = 0
                    if info_store.get_graph_type() == graph_type.UNDIRECTED:
                        opposite_edge = graph[id_of_y][info_store.get_node_position(id_row, column[0])][1]

                    mf_graph.add_edge(id_row, id_of_y, column[1], opposite_edge)

        mf_graph.add_edge(s, 1, 0, 0)

        return node_ids, mf_graph

    def _add_weights(self, residual_graph):
        weights = [i[:] for i in residual_graph]
        for row_id, row in enumerate(residual_graph):
            for column_id, column in enumerate(row):
                isRed = info_store.get_type_by_id(column[0])
                if isRed:
                    weights[row_id][column_id][1] = self.RED_WEIGHT
        return weights

    def _get_all_red_nodes(self, graph):
        red_nodes = []
        for row_id, row in enumerate(graph):
            for column_id, column in enumerate(row):
                is_red = info_store.get_type_by_id(column[0])
                if is_red:
                    red_nodes.append(row_id)
        return red_nodes
