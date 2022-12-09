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


def get_scenic_score(sequence):
    scenic_score = [0] * len(sequence)
    for index, element in enumerate(sequence):
        left, right = sequence[:index], sequence[index + 1:]
        left = left[::-1]
        edge = not left or not right
        if edge:
            continue

        score_left = next(
            (
                index for index, comparison_value in enumerate(left, 1)
                if comparison_value >= element
            ), len(left)
        )
        score_right = next(
            (
                index for index, comparison_value in enumerate(right, 1)
                if comparison_value >= element
            ), len(right)
        )

        scenic_score[index] = score_left * score_right
    return scenic_score


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

    row_scenic_score = [
        get_scenic_score(row)
        for row in grid
    ]

    column_scenic_score = transpose([
        get_scenic_score(column)
        for column in transpose(grid)
    ])

    total_scenic_score = deepcopy(row_scenic_score)
    for row_index in range(len(column_scenic_score)):
        for col_index in range(len(column_scenic_score)):
            total_scenic_score[row_index][col_index] = (
                row_scenic_score[row_index][col_index] *
                column_scenic_score[row_index][col_index]
            )
    print(max(max(row) for row in total_scenic_score))


if __name__ == '__main__':
    main()
