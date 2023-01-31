import sys

if len(sys.argv) >= 3:
    file_name = sys.argv[1]
    second_file_name = sys.argv[2]
else:
    file_name = "./data/HbB_FASTAs-in.txt"
    second_file_name = "./data/BLOSUM62.txt"


def get_dict_of_all_species():
    with open(file_name, 'r') as f:
        lines = f.readlines()
        animal_dict = {}
        current_species_name = ""

        for line in lines:
            clean_line = line.strip()
            if line[0] == ">":
                current_species_name = line[1:].strip().split()[0]
                animal_dict[current_species_name] = []
                continue

            animal_dict[current_species_name] = animal_dict[current_species_name] + list(clean_line)

    return animal_dict


def get_matrix(input_file_name):
    with open(input_file_name, 'r') as f:
        lines = f.readlines()
        index_dict = {}
        first_time = True
        cost_matrix = []
        for line in lines:
            if line[0] == "#":
                continue

            word = line.strip().split()

            if first_time:
                first_time = False
                for letter in range(len(word)):
                    index_dict[word[letter]] = letter

                cost_matrix = [[0 for _ in range(len(index_dict))]
                               for _ in range(len(index_dict))]

            else:
                current_index = index_dict[word.pop(0)]
                word = [int(x) for x in word]

                for cost_of_value in range(len(word)):
                    cost_matrix[current_index][cost_of_value] = word[cost_of_value]

    return index_dict, cost_matrix


def array_contains_keys(array_to_check, key, key2):
    combo1 = key + "--" + key2
    combo2 = key2 + "--" + key
    return not any(x in combo1 for x in array_to_check) and not any(x in combo2 for x in array_to_check)


def get_cost(x, y):
    return matrix[character_index_dict[x]][character_index_dict[y]]


def sequence_alignment(x, y):
    m, n = len(x), len(y)

    # Gap penalties are same price. Thus, we only need to specify that we get gap.
    gap_penalty = get_cost("*", "A")

    grid = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Populate first column and first row of the grid
    for i in range(1, m + 1):
        grid[i][0] = i * gap_penalty

    for j in range(1, n + 1):
        grid[0][j] = j * gap_penalty

    # Find the minimum penalty
    populated_grid = find_minimum_penalty(x, y, gap_penalty, grid)

    # Reconstructing the sequence
    x_answer, y_answer = reconstruct_sequence(x, y, gap_penalty, populated_grid)

    return populated_grid[m][n], "".join(x_answer), "".join(y_answer)


def find_minimum_penalty(x, y, gap_penalty, grid_to_populate):

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            # Initialise moves in the grid and how much each move costs.
            diag = grid_to_populate[i - 1][j - 1] + get_cost(x[i - 1], y[j - 1])

            left = grid_to_populate[i][j - 1] + gap_penalty

            up = grid_to_populate[i - 1][j] + gap_penalty
            # Pick the least expensive move (cost values are switched. Thus, we must switch from min to max)
            grid_to_populate[i][j] = max(diag, up, left)

    return grid_to_populate


def reconstruct_sequence(x, y, gap_penalty, populated_grid):
    # Reconstructing the sequence
    i, j = len(x), len(y)

    x_answer, y_answer = [], []

    while i > 0 or j > 0:

        if x[i - 1] == y[j - 1] and j > 0 and i > 0:
            x_answer.append(x[i - 1])
            y_answer.append(y[j - 1])
            i -= 1
            j -= 1

        elif (populated_grid[i - 1][j - 1] + get_cost(x[i - 1], y[j - 1])) == populated_grid[i][j]:
            x_answer.append(x[i - 1])
            y_answer.append(y[j - 1])
            i -= 1
            j -= 1

        # Append gap to y
        elif (populated_grid[i - 1][j] + gap_penalty) == populated_grid[i][j]:
            x_answer.append(x[i - 1])
            y_answer.append('-')
            i -= 1
        # Append gap to x
        elif (populated_grid[i][j - 1] + gap_penalty) == populated_grid[i][j]:
            x_answer.append('-')
            y_answer.append(y[j - 1])
            j -= 1

    # Sequences are rebuilt inverse. We need to reverse them before it make sense.
    x_answer.reverse(), y_answer.reverse()

    return x_answer, y_answer


def output(combo_name, min_genes, x_answer, y_answer):
    print(combo_name)
    print(f"Minimum Penalty in aligning the genes = {min_genes}")
    print("The aligned genes are:")
    print(f"X sequence: {x_answer}")
    print(f"Y sequence: {y_answer}")
    # Open the file in append & read mode ('a+')
    with open(file_name.replace('-in.txt', '-test.out.txt'), "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(combo_name + ": " + str(min_genes))
        file_object.write("\n")
        file_object.write(x_answer)
        file_object.write("\n")
        file_object.write(y_answer)


def initial_setup():
    species_dict = get_dict_of_all_species()
    checked = []

    for key in species_dict.keys():
        animal_to_compare_1 = species_dict[key]
        for second_key in species_dict.keys():
            if key == second_key:
                continue

            if array_contains_keys(checked, key, second_key):
                animal_to_compare_2 = species_dict[second_key]
                combo1 = key + "--" + second_key

                checked.append(combo1)

                minimum_penalty, x_sequence, y_sequence = sequence_alignment(animal_to_compare_1, animal_to_compare_2)

                output(combo1, minimum_penalty, x_sequence, y_sequence)


character_index_dict, matrix = get_matrix(second_file_name)
initial_setup()
