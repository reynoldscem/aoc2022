from argparse import ArgumentParser
from pathlib import Path


SHAPE_SCORES = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3,
}


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
        data = fd.read().rstrip()

    data = data.replace('X', 'A')
    data = data.replace('Y', 'B')
    data = data.replace('Z', 'C')
    data = data.replace('A', 'Rock')
    data = data.replace('B', 'Paper')
    data = data.replace('C', 'Scissors')

    lines = data.splitlines()

    move_pairs = [line.split() for line in lines]

    my_moves = [pair[1] for pair in move_pairs]
    my_shape_scores = [SHAPE_SCORES[move] for move in my_moves]
    my_total_shape_score = sum(my_shape_scores)

    n_lines = len(lines)
    n_draws = sum(first == second for first, second in move_pairs)
    n_losses = sum(
        (first == 'Rock' and second == 'Scissors') or
        (first == 'Paper' and second == 'Rock') or
        (first == 'Scissors' and second == 'Paper')
        for first, second in move_pairs
    )
    n_wins = n_lines - (n_draws + n_losses)

    draw_score = 3 * n_draws
    win_score = 6 * n_wins
    total_score = my_total_shape_score + win_score + draw_score

    print(total_score)


if __name__ == '__main__':
    main()
