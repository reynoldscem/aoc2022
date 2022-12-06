from argparse import ArgumentParser
from itertools import islice
from pathlib import Path


# https://docs.python.org/release/2.3.5/lib/itertools-example.html
def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    parser.add_argument(
        '--window-size', type=int, default=4
    )

    return parser


def main():
    args = build_parser().parse_args()

    window_size = args.window_size

    with open(args.input_filename) as fd:
        data = fd.read().strip()

    for index, substring in enumerate(window(data, window_size)):
        if len(substring) == len(set(substring)):
            print(index + window_size)
            break


if __name__ == '__main__':
    main()
