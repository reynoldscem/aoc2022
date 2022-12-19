from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def parse_line(line):
    from re import findall

    return tuple(map(int, findall(r'(-?\d+)', line)))


def vector3_add(first, second):
    return tuple(
        first_entry + second_entry
        for first_entry, second_entry in zip(first, second)
    )


def neighbours(coordinate):
    offsets = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)
    ]

    for offset in offsets:
        yield vector3_add(coordinate, offset)


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        lines = fd.read().strip().splitlines()

    coordinates = [
        parse_line(line)
        for line in lines
    ]
    mins = tuple(map(min, zip(*coordinates)))
    min_x, min_y, min_z = (entry - 1 for entry in mins)

    maxes = tuple(map(max, zip(*coordinates)))
    max_x, max_y, max_z = (entry + 1 for entry in maxes)

    def out_of_bounds(voxel):
        x, y, z = voxel
        if x < min_x or x > max_x:
            return True

        if y < min_y or y > max_y:
            return True

        if z < min_z or z > max_z:
            return True

        return False

    start_point = mins
    q = [start_point]
    visited = {start_point}

    surface_area = 0
    while q:
        voxel = q.pop()
        for neighbour in neighbours(voxel):
            if neighbour in visited or out_of_bounds(neighbour):
                continue
            elif neighbour in coordinates:
                surface_area += 1
            else:
                visited.add(neighbour)
                q.append(neighbour)
    print(surface_area)


if __name__ == '__main__':
    main()
