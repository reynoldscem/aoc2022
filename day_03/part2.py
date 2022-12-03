from argparse import ArgumentParser
from pathlib import Path
import itertools


# The classic missing iterator
# https://alexwlchan.net/2018/12/iterating-in-fixed-size-chunks/
def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


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

    sets = map(set, lines)

    triplets = chunked_iterable(iter(sets), 3)

    badges = [set.intersection(*triplet).pop() for triplet in triplets]

    print(
        sum(priority(badge) for badge in badges)
    )


if __name__ == '__main__':
    main()
