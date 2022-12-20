from argparse import ArgumentParser
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def mix(number_list):
    num_elements = len(number_list)
    index_order = number_list.copy()

    indices = list(range(len(number_list)))

    for position in range(num_elements):
        source_position = indices.index(position)
        value_to_move = number_list[source_position]
        element = number_list.pop(source_position)
        indices.pop(source_position)

        destination_position = (
            source_position + value_to_move
        ) % (num_elements - 1)

        number_list = (
            number_list[:destination_position] +
            [value_to_move] +
            number_list[destination_position:]
        )
        indices = (
            indices[:destination_position] +
            [destination_position] +
            indices[destination_position:]
        )
        # print(f'{source_position}, {destination_position}')
        # print(f'Move {element} to {destination_position}')
        # print(number_list)

    return number_list


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        input_numbers = [
            int(entry)
            for entry in fd.read().strip().splitlines()
        ]

    # print(input_numbers)
    mixed = mix(input_numbers)

    base_position = mixed.index(0)
    offsets = (1000, 2000, 3000)
    indices = [
        (base_position + offset) % len(mixed)
        for offset in offsets
    ]

    print(
        sum(mixed[index] for index in indices)
    )


if __name__ == '__main__':
    main()
