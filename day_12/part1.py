from functools import cached_property
from argparse import ArgumentParser
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


class HeightGrid:
    def __init__(self, height_grid, start_coordinate, end_coordinate):

        self.start_coordinate = start_coordinate
        self.end_coordinate = end_coordinate

        self.height_grid = height_grid

        self.n_rows, self.n_columns = self.row_and_column_count(height_grid)
        for row in height_grid:
            assert len(row) == self.n_columns, 'Must be square array!'

    def __getitem__(self, key):
        x, y = key
        return self.height_grid[x][y]

    @staticmethod
    def character_to_elevation(character):
        return ord(character) - ord('a')

    @staticmethod
    def row_and_column_count(grid):
        rows = len(grid)
        columns = len(grid[0])

        return rows, columns

    @staticmethod
    def _indices_2d(n_rows, n_columns):
        return [
            [
                (row_index, column_index)
                for column_index in range(n_columns)
            ]
            for row_index in range(n_rows)
        ]

    @cached_property
    def indices_2d(self):
        return self._indices_2d(self.n_rows, self.n_columns)

    @cached_property
    def coordinate_set(self):
        return set(
            self.flatten(self.indices_2d)
        )

    def valid(self, coordinate):
        return coordinate in self.coordinate_set

    def possible_neighbours(self, coordinate):
        # If we end up needing 8-neighbours...
        #
        # from itertools import product
        # deltas = (-1, 0, 1)
        # offsets = set(product(deltas, deltas)) - {(0, 0)}

        offsets = (
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0)
        )

        x, y = coordinate
        for dx, dy in offsets:
            candidate_neighbour = (x + dx, y + dy)
            if self.valid(candidate_neighbour):
                yield candidate_neighbour

    def reachable_neighbours(self, coordinate):
        this_height = self[coordinate]
        for possible_neighbour in self.possible_neighbours(coordinate):
            neighbour_height = self[possible_neighbour]
            if abs(neighbour_height - this_height) <= 1:
                yield possible_neighbour

    @staticmethod
    def flatten(matrix):
        return [entry for row in matrix for entry in row]

    @staticmethod
    def find(string, character):
        return next(
            index
            for index in range(len(string))
            if string[index] == character
        )

    @classmethod
    def start_end_indices_from_string(cls, string):
        from re import sub
        clean_string = sub(r'[^a-zA-Z]', '', string)

        start_index = cls.find(clean_string, 'S')
        end_index = cls.find(clean_string, 'E')

        return start_index, end_index

    @classmethod
    def make_from_input_string(cls, string):
        height_map_string = string.replace('S', 'a').replace('E', 'z')
        height_grid = [
            [cls.character_to_elevation(character) for character in line]
            for line in height_map_string.split('\n')
        ]
        n_rows, n_columns = cls.row_and_column_count(height_grid)
        indices = cls._indices_2d(n_rows, n_columns)
        indices_flat = cls.flatten(indices)

        (
            start_index_1d, end_index_1d
        ) = cls.start_end_indices_from_string(string)

        start_index_2d = indices_flat[start_index_1d]
        end_index_2d = indices_flat[end_index_1d]

        return cls(height_grid, start_index_2d, end_index_2d)

    def __str__(self):
        grid_string = '\n\n'.join(
            ' '.join(map(lambda x: f'{x:03d}', line))
            for line in self.height_grid
        )

        start_coordinate_string = f'Start: {self.start_coordinate}'
        end_coordinate_string = f'End: {self.end_coordinate}'

        return '\n'.join([
            start_coordinate_string,
            end_coordinate_string,
            '\n',
            grid_string
        ])


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        data = fd.read().strip()

    height_grid = HeightGrid.make_from_input_string(data)

    list(height_grid.possible_neighbours(height_grid.start_coordinate))

    import IPython
    IPython.embed()

    print(height_grid)


if __name__ == '__main__':
    main()
