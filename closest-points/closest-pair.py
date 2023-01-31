import sys
from math import sqrt, ceil, floor

filename = sys.argv[1]


def closest_pair(unsorted_points):
    px = sorted(unsorted_points, key=lambda point: point[0])
    py = sorted(unsorted_points, key=lambda point: point[1])

    minimum_distance = closest_pair_rec(px, py)
    record_output(len(unsorted_points), minimum_distance)


def record_output(length_of_file, output):
    # Open the file in append & read mode ('a+')
    with open("./output.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(filename + " " + str(length_of_file) + " " + str(output))


def calc_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def brute_force(px, py):
    current_minimal = sys.float_info.max
    for point_index in range(len(px)):
        for next_point_index in range(len(px)):
            if point_index == next_point_index:
                continue
            d = calc_distance(px[point_index], px[next_point_index])
            if d < current_minimal:
                current_minimal = d
    return current_minimal


def closest_pair_rec(px, py):
    if len(px) <= 3:
        return brute_force(px, py)

    left_x, left_y, right_x, right_y = px[:ceil(len(px)/2)], py[:ceil(len(py)/2)], px[floor(len(px)/2):], py[floor(len(py)/2):]

    left_side = closest_pair_rec(left_x, left_y)
    right_side = closest_pair_rec(right_x, right_y)

    minimum_distance = min(left_side, right_side)  # Q

    maximum_x = left_x[-1][0]  # get middle line
    points_near_middle = []

    for point in px:
        if abs(point[0] - maximum_x) < minimum_distance:
            points_near_middle.append(point)

    middle_min_distance = sys.float_info.max
    for point_index in range(len(points_near_middle)):
        for next_point_index in range(point_index + 1, point_index + 15):
            if next_point_index == len(points_near_middle):
                break

            d = calc_distance(points_near_middle[point_index], points_near_middle[next_point_index])
            if d < middle_min_distance:
                middle_min_distance = d

    if middle_min_distance < minimum_distance:
        return middle_min_distance
    elif left_side < right_side:
        return left_side
    else:
        return right_side


def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        skip = 0

        while str.isupper(lines[skip][:2]):
            skip += 1

        lines = list(map(
            str.strip,
            filter(
                lambda x: x.strip() != "EOF" and x.strip() != "",
                lines[skip:]
            )
        ))
        points = []
        for l in lines:
            _, x, y = l.split()
            points.append([float(x), float(y)])
        return points

closest_pair(read_file(filename))
