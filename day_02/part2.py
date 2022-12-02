from argparse import ArgumentParser
from collections import Counter
from pathlib import Path


SHAPE_SCORES = {
    'Rock': 1,
    'Paper': 2,
    'Scissors': 3,
}

MOVES_AND_BEATING_MOVES = [
    ('Rock', 'Paper'),
    ('Paper', 'Scissors'),
    ('Scissors', 'Rock')
]
MOVE_TO_WIN = dict(MOVES_AND_BEATING_MOVES)
MOVE_TO_LOSE = dict([reversed(pair) for pair in MOVES_AND_BEATING_MOVES])


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def win(indicator):
    return indicator == 'Z'


def lose(indicator):
    return indicator == 'X'


def main():
    args = build_parser().parse_args()
    with open(args.input_filename) as fd:
        data = fd.read().rstrip()

    # Characters now tell us wins, losses, draws
    character_counter = Counter(data)
    n_draws = character_counter['Y']
    n_wins = character_counter['Z']

    data = data.replace('A', 'Rock')
    data = data.replace('B', 'Paper')
    data = data.replace('C', 'Scissors')

    lines = data.splitlines()

    move_pairs = [line.split() for line in lines]

    for move_pair in move_pairs:
        opponent_move, win_lose_draw_indicator = move_pair
        if win(win_lose_draw_indicator):
            move_pair[1] = MOVE_TO_WIN[opponent_move]
        elif lose(win_lose_draw_indicator):
            move_pair[1] = MOVE_TO_LOSE[opponent_move]
        else:
            move_pair[1] = move_pair[0]

    my_moves = [pair[1] for pair in move_pairs]
    my_shape_scores = [SHAPE_SCORES[move] for move in my_moves]
    my_total_shape_score = sum(my_shape_scores)

    draw_score = 3 * n_draws
    win_score = 6 * n_wins
    total_score = my_total_shape_score + win_score + draw_score

    print(total_score)


if __name__ == '__main__':
    main()
