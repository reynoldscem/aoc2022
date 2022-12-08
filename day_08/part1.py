from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def string_to_integer_list(string):
    return list(map(int, string))


def get_visibility(sequence):
    visible = [False] * len(sequence)
    for index, element in enumerate(sequence):
        left, right = sequence[:index], sequence[index + 1:]
        edge = not left or not right
        if edge:
            visible[index] = True
            continue

        taller_than_tallest_on_atleast_one_side = (
            element > min(max(left), max(right))
        )
        visible[index] = edge or taller_than_tallest_on_atleast_one_side
    return visible


def transpose(matrix):
    return list(zip(*matrix))


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        data = fd.read()

    lines = data.splitlines()

    grid = [
        string_to_integer_list(line)
        for line in lines
    ]

    row_visibility = [
        get_visibility(row)
        for row in grid
    ]

    column_visibility = transpose([
        get_visibility(column)
        for column in transpose(grid)
    ])

    total_visibility = deepcopy(row_visibility)
    for row_index in range(len(column_visibility)):
        for col_index in range(len(column_visibility)):
            total_visibility[row_index][col_index] = (
                row_visibility[row_index][col_index] or
                column_visibility[row_index][col_index]
            )
    print(sum(sum(row) for row in total_visibility))


if __name__ == '__main__':
    main()
