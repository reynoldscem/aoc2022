from argparse import ArgumentParser
from itertools import count
from pathlib import Path
import json

from enum import Enum


class Comparison(Enum):
    LESSER = 1
    EQUAL = 2
    GREATER = 3


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def parse_string_to_pair(string):
    return tuple(
        json.loads(string_part)
        for string_part in string.split('\n')
    )


def ordered(left, right):
    return compare(left, right, level=0) == Comparison.LESSER


def compare(left, right, level=0):
    if isinstance(left, int) and isinstance(right, int):
        print('  ' * level, end='')
        print(f'- Compare {left} vs {right}')
        if left == right:
            return Comparison.EQUAL
        elif left < right:
            print('  ' * (level + 1), end='')
            print('- Left side is smaller, so inputs are in the right order')
            return Comparison.LESSER
        elif left > right:
            print('  ' * (level + 1), end='')
            print(
                '- Right side is smaller, '
                'so inputs are not in the right order'
            )
            return Comparison.GREATER

    if isinstance(left, list) and isinstance(right, int):
        print('  ' * (level), end='')
        print(
            f'- Mixed types; convert right to [{right}] and retry comparison'
        )
        right = [right]
    elif isinstance(left, int) and isinstance(right, list):
        print('  ' * (level), end='')
        print(
            f'- Mixed types; convert left to [{left}] and retry comparison'
        )
        left = [left]

    print(f'- Compare {left} vs {right}')
    for a, b in zip(left, right):
        comparison = compare(a, b, level=level + 1)
        if comparison == Comparison.EQUAL:
            pass
        elif comparison in (Comparison.LESSER, Comparison.GREATER):
            return comparison
        else:
            raise RuntimeError("Invalid comparison")

    if len(left) < len(right):
        print('  ' * level, end='')
        print(
            '- Left side ran out of items, so inputs are in the right order'
        )
        return Comparison.LESSER
    elif len(left) == len(right):
        return Comparison.EQUAL
    else:
        print('  ' * level, end='')
        print(
            '- Right side ran out of items, '
            'so inputs are not in the right order'
        )
        return Comparison.GREATER


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        data = fd.read().strip()

    pair_strings = data.split('\n\n')
    pairs = [parse_string_to_pair(string) for string in pair_strings]

    pairs_with_indices = list(zip(count(1), pairs))

    indices_of_pairs_in_order = [
        index
        for index, (first, second) in pairs_with_indices
        if ordered(first, second)
    ]

    print(sum(indices_of_pairs_in_order))

    # for index, (first, second) in pairs_with_indices:
    #     print(f'== Pair {index} ==')
    #     try:
    #         ordered(first, second)
    #     except Exception as e:
    #         print('This case failed')
    #         print(e)
    #         print()


if __name__ == '__main__':
    main()
