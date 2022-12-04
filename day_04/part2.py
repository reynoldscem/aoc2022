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


def set_from_exclusive_endpoints(start, end):
    return set(range(start, end + 1))


def line_to_set_pair(line):
    match_object = re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line)
    match_ints = map(int, match_object.groups())
    first_start, first_end, second_start, second_end = match_ints

    return (
        set_from_exclusive_endpoints(first_start, first_end),
        set_from_exclusive_endpoints(second_start, second_end)
    )


def overlap(first, second):
    return len(first.intersection(second)) > 0


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        lines = fd.read().splitlines()

    print(sum(overlap(*line_to_set_pair(line)) for line in lines))


if __name__ == '__main__':
    main()
