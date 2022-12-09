from argparse import ArgumentParser
from pathlib import Path


directions = {
    'U': (1, 0),
    'D': (-1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def vector_add(first, second):
    return (
        first[0] + second[0],
        first[1] + second[1]
    )


def vector_sub(first, second):
    return (
        first[0] - second[0],
        first[1] - second[1]
    )


def manhattan(first, second):
    return (
        abs(first[0] - second[0]) +
        abs(first[1] - second[1])
    )


def touching(first, second):
    return manhattan(first, second) < 2


def colinear(first, second):
    return first[0] == second[0] or first[1] == second[1]


def diagonal(first, second):
    return not colinear(first, second)


def get_direction(vector):
    from math import copysign
    return (
        copysign(1, vector[0]),
        copysign(1, vector[1])
    )


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        data = fd.read()

    lines = data.splitlines()

    instructions = []
    for line in lines:
        direction, count_string = line.split()
        count = int(count_string)
        instructions += [direction] * count

    head = (0, 0)
    tail = (0, 0)

    tail_positions = set()
    tail_positions.add(tail)

    for instruction in instructions:
        change = directions[instruction]
        head = vector_add(head, change)
        if touching(head, tail):
            continue

        if colinear(head, tail):
            tail = vector_add(tail, change)
        elif manhattan(head, tail) > 2:
            difference = vector_sub(head, tail)
            update = get_direction(difference)
            tail = vector_add(tail, update)

        tail_positions.add(tail)

    print(len(tail_positions))


if __name__ == '__main__':
    main()
