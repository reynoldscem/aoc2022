from argparse import ArgumentParser
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        data = fd.read()

    lines = data.splitlines()
    line = lines[0]

    sequence = list(map(int, line))
    visible = [False] * len * sequence
    for index, element in enumerate(sequence):
        left, right = sequence[:index], sequence[index + 1:]
        edge = not left or not right
        taller_than_tallest_on_atleast_one_side = (
            element > min(max(left), max(right))
        )
        visible[index] = edge or taller_than_tallest_on_atleast_one_side
