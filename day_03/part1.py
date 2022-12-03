from argparse import ArgumentParser
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def priority(character):
    if character.islower():
        return ord(character) - 96
    else:
        return ord(character) - 64 + 26


def common_item(string):
    midpoint = len(string) // 2
    intersection = set(string[:midpoint]).intersection(string[midpoint:])

    return intersection.pop()


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        lines = fd.read().splitlines()

    print(sum(priority(common_item(line)) for line in lines))


if __name__ == '__main__':
    main()
