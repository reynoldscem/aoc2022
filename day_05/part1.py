from argparse import ArgumentParser
from pathlib import Path
import re


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def transpose(matrix):
    return list(zip(*matrix))


def stackify(character_collection):
    return list(''.join(character_collection).replace(' ', ''))


def make_crates(starting_crates_lines):
    character_lists = [
        line[::-1]
        for line in transpose(starting_crates_lines)
    ]

    return {
        int(key): stackify(rest)
        for key, *rest in character_lists
        if key.strip()
    }


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        data = fd.read()

    starting_crates_lines, procedure_lines = [
        string.split('\n')
        for string in data.split('\n\n')
    ]
    crates = make_crates(starting_crates_lines)
    crates


if __name__ == '__main__':
    main()
