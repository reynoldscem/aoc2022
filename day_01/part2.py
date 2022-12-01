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
        data = fd.read().split('\n\n')
    print(
        sum(sorted(
            sum(int(calories) for calories in line.split())
            for line in data
        )[::-1][:3])
    )


if __name__ == '__main__':
    main()
