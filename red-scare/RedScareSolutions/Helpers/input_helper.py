from collections import deque

from RedScareSolutions.Helpers.singleton import Singleton
from enum import Enum
import copy


class graph_type(Enum):
    NONE = -1
    UNDIRECTED = 1
    DIRECTED = 2
    MIXED = 3


class InputHelper(metaclass=Singleton):
    def __init__(self):
        self.start_location = "Not Initialised"
        self.end_location = "Not Initialised"
        self.original_graph = []
        self.dictionary_by_name = {}
        self.dictionary_by_id = {}
        self.graph_type = graph_type.NONE

    def initialise_values(self, start_location, end_location, original_graph, graph_type, dictionary_by_name,
                          dictionary_by_id):
        self.start_location = start_location
        self.end_location = end_location
        self.original_graph = original_graph
        self.dictionary_by_name = dictionary_by_name
        self.dictionary_by_id = dictionary_by_id
        self.graph_type = graph_type

    def _getId(self, specified_dict, val, val2):
        if val2 is not None:
            return specified_dict[val][0], specified_dict[val2][0]

        return specified_dict[val][0]

    def _getType(self, specified_dict, val, val2):
        if val2 is not None:
            return specified_dict[val][1], specified_dict[val2][1]

        return specified_dict[val][1]

    def _checkType(self, specified_dict, val, val2):
        return specified_dict[val][1] == specified_dict[val2][1]

    def get_source(self):
        return self.start_location

    def get_source_id(self):
        return self.get_id_by_name(self.start_location)

    def get_destination(self):
        return self.end_location

    def get_destination_id(self):
        return self.get_id_by_name(self.end_location)

    def get_graph_type(self):
        return self.graph_type

    def get_node_position(self, value_to_find, position_in_graph):
        pos = self.original_graph[position_in_graph]
        for vl in range(len(pos)):
            if pos[vl][0] == value_to_find:
                return vl
        return -1

    def is_cyclic(self):
        graph = self.original_graph
        source = self.get_source_id()
        end = self.get_destination_id()

        traverse_initial = [False for _ in range(len(graph))]

        # We start at the source. Mark source as visited and add it to a queue.
        traverse_initial[source] = True

        queue = deque([(source, traverse_initial, source)])

        while queue:

            current_node, traversed, parent = queue.popleft()

            for index in range(len(graph[current_node])):

                if not traversed[graph[current_node][index][0]] and graph[current_node][index][0] != end:
                    traversed[graph[current_node][index][0]] = True

                    queue.append((graph[current_node][index][0], traversed, current_node))
                elif parent != graph[current_node][index][0] and graph[current_node][index][0] != source and \
                        graph[current_node][index][0] != end:
                    return True

        return False

    def get_original_graph(self):
        # create a residual graph based on the original graph. (Original graph should be preserved)
        return copy.deepcopy(self.original_graph)

    def get_id_by_name(self, name, second_name=None):
        if second_name is not None:
            second_name = str(second_name)

        return self._getId(self.dictionary_by_name, str(name), second_name)

    def get_type_by_name(self, name, second_name=None):
        if second_name is not None:
            second_name = str(second_name)

        return self._getType(self.dictionary_by_name, str(name), second_name)

    def compare_type_by_name(self, name, second_name):
        return self._checkType(self.dictionary_by_name, str(name), str(second_name))

    def get_name_by_id(self, first_id, second_id=None):
        if second_id is not None:
            second_id = int(second_id)

        return self._getId(self.dictionary_by_id, int(first_id), second_id)

    def get_type_by_id(self, first_id, second_id=None):
        if second_id is not None:
            second_id = int(second_id)

        return self._getType(self.dictionary_by_id, int(first_id), second_id)

    def compare_type_by_id(self, first_id, second_id):
        return self._checkType(self.dictionary_by_id, int(first_id), int(second_id))

    def __str__(self):
        print('dictionary_by_name :', self.dictionary_by_name)
        print('dictionary_by_id :', self.dictionary_by_id)
        print('original_graph :', self.original_graph)
        return "source: " + str(self.start_location) + \
               " destination: " + self.end_location + \
               " graph type: " + self.graph_type.name


info_store = InputHelper()
