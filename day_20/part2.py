from argparse import ArgumentParser
from pathlib import Path


KEY = 811589153


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def mix(number_list, n_mixes):
    num_elements = len(number_list)
    indices = list(range(len(number_list)))

    for _ in range(n_mixes):
        for position in range(num_elements):
            source_position = indices.index(position)

            value_to_move = number_list[position]

            index_lookup = indices.pop(source_position)
            assert index_lookup == position

            destination_position = (
                source_position + value_to_move
            ) % (num_elements - 1)

            indices.insert(destination_position, position)

    return [
        number_list[index]
        for index in indices
    ]


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        input_numbers = [
            int(entry) * KEY
            for entry in fd.read().strip().splitlines()
        ]

    mixed = mix(input_numbers, 10)

    base_position = mixed.index(0)
    offsets = (1000, 2000, 3000)
    indices = [
        (base_position + offset) % len(mixed)
        for offset in offsets
    ]
    print([mixed[index] for index in indices])
    print(
        sum(mixed[index] for index in indices)
    )


if __name__ == '__main__':
    main()
