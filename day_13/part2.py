from argparse import ArgumentParser
from functools import cmp_to_key
from pathlib import Path
from math import prod
import json

from enum import Enum

DIVIDER_PACKETS = ([[2]], [[6]])


class Comparison(Enum):
    LESSER = -1
    EQUAL = 0
    GREATER = 1


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def parse_string_to_tuple(string):
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

    data = data.replace('\n\n', '\n')
    entries = parse_string_to_tuple(data)
    entries = entries + DIVIDER_PACKETS

    compare_key = cmp_to_key(lambda x, y: compare(x, y).value)
    sorted_entries = sorted(entries, key=compare_key)

    divider_indices = [
        sorted_entries.index(divider) + 1
        for divider in DIVIDER_PACKETS
    ]
    print(prod(divider_indices))


if __name__ == '__main__':
    main()
