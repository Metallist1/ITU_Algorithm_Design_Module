import sys
import asyncio
from RedScareSolutions.Helpers.input_helper import info_store, graph_type
from RedScareSolutions.Alternative import AlternativeProblem
from RedScareSolutions.Few import FewProblem
from RedScareSolutions.Some import SomeProblem
from RedScareSolutions.Many import ManyProblem
from RedScareSolutions.NoneP import NoneProblem

# Uncomment incase recursion error
sys.setrecursionlimit(150000)

if len(sys.argv) >= 2:
    file_name = sys.argv[1]
else:
    file_name = "./data/G-ex.txt"

if len(sys.argv) >= 3:
    current_problem = int(sys.argv[2])
else:
    current_problem = -1

if len(sys.argv) >= 4:
    output_to_file = bool(sys.argv[3])
else:
    output_to_file = False


# Note: Each graph is created by ID's and not Names.
# Thus, you should use dictionary_on_id when retrieving values
async def get_input():
    dictionary_on_name = {}
    dictionary_on_id = {}
    with open(file_name, 'r') as f:
        # # First value nodes / paths / reds
        first_line = f.readline().strip().split()
        number_of_vertex = int(first_line[0])
        number_of_edges = int(first_line[1])
        number_of_red = int(first_line[2])
        # Second value start , end
        second_line = f.readline().strip().split()
        start = second_line[0]
        end = second_line[1]

        graph = [[] for _ in range(number_of_vertex)]

        for i in range(number_of_vertex):
            vertex = f.readline().strip().split()
            if len(vertex) > 1:
                dictionary_on_name[vertex[0]] = [i, True]
                dictionary_on_id[i] = [vertex[0], True]
            else:
                dictionary_on_name[vertex[0]] = [i, False]
                dictionary_on_id[i] = [vertex[0], False]

        g_type = graph_type.NONE
        for i in range(number_of_edges):
            edge = f.readline().strip().split()

            if edge[1] == "->":
                if g_type == graph_type.UNDIRECTED:
                    g_type = graph_type.MIXED
                elif g_type == graph_type.NONE:
                    g_type = graph_type.DIRECTED
                graph[dictionary_on_name[edge[0]][0]].append([dictionary_on_name[edge[2]][0], 1])
            else:
                if g_type == graph_type.DIRECTED:
                    g_type = graph_type.MIXED
                elif g_type == graph_type.NONE:
                    g_type = graph_type.UNDIRECTED

                graph[dictionary_on_name[edge[0]][0]].append([dictionary_on_name[edge[2]][0], 1])
                graph[dictionary_on_name[edge[2]][0]].append([dictionary_on_name[edge[0]][0], 1])
        if len(graph[dictionary_on_name[start][0]]) < 1:
            g_type = graph_type.NONE
            print("No edges between start and end")
        info_store.initialise_values(start, end, graph, g_type, dictionary_on_name, dictionary_on_id)


def output(problem_type, result):
    output_file_name = "./output.txt"
    if './data/' not in file_name:
        output_file_name = "../output.txt"

    if current_problem != -1:
        output_file_name = output_file_name.replace(".txt", '-' + problem_type + '.txt')

    with open(output_file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        final_name = file_name.replace('./data/', '').replace('.txt', '')
        file_object.write("File name: " + str(final_name) +
                          ", Problem: " + str(problem_type) +
                          ", Answer: " + str(result))


async def initial_setup():
    await get_input()

    _alternative = AlternativeProblem()
    _some = SomeProblem()
    _few = FewProblem()
    _none = NoneProblem()
    _many = ManyProblem()
    # this switch is for testing individual problems without output. Change current_problem to get different problems
    match current_problem:
        case 1:
            result = _none.get_result()
            print(result)
            if output_to_file:
                output("None", result)
        case 2:
            result = _some.get_result()
            print(result)
            if output_to_file:
                output("Some", result)
        case 3:
            result = _many.get_result()
            print(result)
            if output_to_file:
                output("Many", result)
        case 4:
            result = _few.get_result()
            print(result)
            if output_to_file:
                output("Few", result)
        case 5:
            result = _alternative.get_result()
            print(result)
            if output_to_file:
                output("Alternative", result)
        case _:
            output("None", _none.get_result())
            output("Some", _some.get_result())
            output("Many", _many.get_result())
            output("Few", _few.get_result())
            output("Alternative", _alternative.get_result())


async def main():
    await initial_setup()


if __name__ == '__main__':
    asyncio.run(main())
