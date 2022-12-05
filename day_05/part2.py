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
    # Remove the last one to prevent a blank instruction.
    #  Don't do via stripping input data as it's important
    #  that the crates string is square.
    procedure_lines = procedure_lines[:-1]
    crates = make_crates(starting_crates_lines)

    for line in procedure_lines:
        count, source, dest = map(int, re.findall(r'\d+', line))

        crates_in_motion = []
        for _ in range(count):
            crates_in_motion.append(crates[source].pop())
        for _ in range(count):
            crates[dest].append(crates_in_motion.pop())

    answer = ''.join([
        crates[key].pop()
        for key in sorted(crates.keys())
    ])
    print(answer)


if __name__ == '__main__':
    main()
