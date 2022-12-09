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


def distance_metric(first, second):
    return max(
        abs(first[0] - second[0]),
        abs(first[1] - second[1])
    )


def touching(first, second):
    return distance_metric(first, second) < 2


def colinear(first, second):
    return first[0] == second[0] or first[1] == second[1]


def diagonal(first, second):
    return not colinear(first, second)


def get_direction(vector):
    from math import copysign
    return (
        (vector[0] != 0) * int(copysign(1, vector[0])),
        (vector[1] != 0) * int(copysign(1, vector[1]))
    )


def simulate_updates(head_changes):
    head = (0, 0)
    tail = (0, 0)

    tail_positions = set()
    tail_positions.add(tail)
    # print(tail)

    tail_changes = []

    for change in head_changes:
        head = vector_add(head, change)
        difference = vector_sub(head, tail)

        if distance_metric(head, tail) > 1:
            difference = vector_sub(head, tail)
            change = get_direction(difference)
            tail = vector_add(tail, change)
        else:
            change = (0, 0)

        tail_changes.append(change)

        # print(f'Head: {head}, Tail: {tail}')
        # print()

        tail_positions.add(tail)

    return tail_changes, tail_positions


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

    head_changes = [
        directions[instruction]
        for instruction in instructions
    ]

    tail_changes = head_changes
    for _ in range(9):
        tail_changes, tail_positions = simulate_updates(
            tail_changes
        )
    print(len(tail_positions))


if __name__ == '__main__':
    main()
