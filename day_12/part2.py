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

    @staticmethod
    def manhattan(coordinate, other):
        x, y = coordinate
        other_x, other_y = other

        return abs(x - other_x) + abs(y - other_y)

    def reachable_neighbours(self, coordinate):
        this_height = self[coordinate]
        for possible_neighbour in self.possible_neighbours(coordinate):
            neighbour_height = self[possible_neighbour]
            if neighbour_height <= this_height + 1:
                yield possible_neighbour

    def trace_path(self, preceding_node, current):
        path = []
        while current in preceding_node:
            current = preceding_node[current]
            path.insert(0, current)

        return path

    def a_star_search(self):
        from collections import defaultdict
        from math import inf

        start_coordinate = self.start_coordinate
        target_coordinate = self.end_coordinate

        def heuristic(coordinate):
            return self.manhattan(coordinate, target_coordinate)

        preceding_lookup = dict()

        # shortest_path_cost_from_start_to_coordinate
        cost_to_coordinate = defaultdict(lambda: inf)
        cost_to_coordinate[start_coordinate] = 0

        # Only a true upper bound if the heuristic is admissible (it is)
        upper_bound_cost_to_coordinate = defaultdict(lambda: inf)
        upper_bound_cost_to_coordinate[start_coordinate] = (
            self.manhattan(start_coordinate, target_coordinate)
        )

        frontier = set()
        frontier.add(start_coordinate)

        while frontier:
            current = min(
                frontier, key=lambda x: upper_bound_cost_to_coordinate[x]
            )
            if current == target_coordinate:
                return self.trace_path(preceding_lookup, current)

            frontier.remove(current)

            for neighbour in self.reachable_neighbours(current):
                potential_score = 1 + cost_to_coordinate[current]
                if potential_score < cost_to_coordinate[neighbour]:
                    preceding_lookup[neighbour] = current

                    cost_to_coordinate[neighbour] = potential_score
                    upper_bound_cost_to_coordinate[neighbour] = (
                        potential_score + heuristic(neighbour)
                    )
                    if neighbour not in frontier:
                        frontier.add(neighbour)

        raise Exception("Couldn't find item!")

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

        height_flat = cls.flatten(height_grid)
        start_indices_2d = [
            indices_flat[index_1d]
            for index_1d in range(len(indices_flat))
            if height_flat[index_1d] == 0
        ]

        end_index_2d = indices_flat[end_index_1d]

        return [
            cls(height_grid, start_index_2d, end_index_2d)
            for start_index_2d in start_indices_2d
        ]

    @property
    def grid_string(self):
        return '\n\n'.join(
            ' '.join(map(lambda x: f'{x:03d}', line))
            for line in self.height_grid
        )

    def __str__(self):
        start_coordinate_string = f'Start: {self.start_coordinate}'
        end_coordinate_string = f'End: {self.end_coordinate}'

        return '\n'.join([
            start_coordinate_string,
            end_coordinate_string,
            '\n',
            self.grid_string
        ])


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        data = fd.read().strip()

    height_grids = HeightGrid.make_from_input_string(data)

    lengths = []
    for grid in height_grids:
        try:
            path = grid.a_star_search()
            lengths.append(len(path))
        except Exception:
            pass

    print(min(lengths))


if __name__ == '__main__':
    main()
