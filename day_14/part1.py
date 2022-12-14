from functools import cached_property
from argparse import ArgumentParser
from more_itertools import windowed
from pathlib import Path
from enum import Enum


class Material(Enum):
    ROCK = 1
    SAND = 2


def transpose(matrix):
    return zip(*matrix)


class Cave:
    def __init__(self, rock_points, source=None):
        self.grid = dict()
        for rock_point in rock_points:
            self.grid[rock_point] = Material.ROCK

        if source:
            self.source_coordinate = source

    @cached_property
    def bounding_coords(self):
        xs, ys = transpose(self.grid.keys())

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        return (min_x, max_x), (min_y, max_y)

    def generate_sand(self, do_print=False):
        sand_coordinate = self.source_coordinate

        x_offsets = (0, -1, 1)
        while True:
            if do_print:
                print(self)

            sand_x, sand_y = sand_coordinate

            (min_x, max_x), (min_y, max_y) = self.bounding_coords
            if sand_y > max_y:
                break

            for x_offset in x_offsets:
                potential_sand_coord = (sand_x + x_offset, sand_y + 1)

                if potential_sand_coord not in self.grid:
                    break
            else:
                self.grid[sand_coordinate] = Material.SAND
                sand_coordinate = self.source_coordinate
                continue

            sand_coordinate = potential_sand_coord

    def __str__(self):
        string = ''

        (min_x, max_x), (min_y, max_y) = self.bounding_coords
        print((min_x, max_x))
        print((min_y, max_y))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) not in self.grid:
                    character = '.'
                elif self.grid[x, y] == Material.ROCK:
                    character = '#'
                elif self.grid[x, y] == Material.SAND:
                    character = 'o'
                elif (x, y) == self.source_coordinate:
                    character = '+'
                else:
                    character = '@'

                string += character
            string += '\n'

        n_sand = sum(
            material == Material.SAND for material in self.grid.values()
        )
        return f'{string}\n{n_sand}'

        xs, ys = (
            map(str, coords)
            for coords in transpose(self.grid.keys())
        )

        return '\n'.join([
            ', '.join(xs),
            ', '.join(ys)
        ])


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def parse_coordinate(string):
    return tuple(int(entry) for entry in string.split(','))


def parse_path(string):
    coordinate_strings = string.split(' -> ')

    return [
        parse_coordinate(coordinate_string)
        for coordinate_string in coordinate_strings
    ]


def vector_subtract(first, second):
    return (
        first[0] - second[0],
        first[1] - second[1]
    )


def vector_add(first, second):
    return (
        first[0] + second[0],
        first[1] + second[1]
    )


def normalise(vector):
    # Manhattan norm
    norm = abs(sum(vector))

    return (
        vector[0] // norm,
        vector[1] // norm
    )


def all_points_along_path(source, dest):
    difference = vector_subtract(dest, source)
    norm = abs(sum(difference))
    direction = normalise(difference)

    points = {source}
    for _ in range(norm):
        new_point = vector_add(source, direction)
        points.add(new_point)
        source = new_point

    return points


def get_rock_points(lines):
    rock_points = set()
    for line in lines:
        path = parse_path(line)

        rock_points = set.union(
            *[
                all_points_along_path(source_coord, dest_coord)
                for source_coord, dest_coord in windowed(path, 2)
            ],
            rock_points
        )

    return rock_points


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        input_lines = fd.read().strip().splitlines()

    rock_points = get_rock_points(input_lines)
    cave = Cave(rock_points, source=(500, 0))

    print(cave)
    cave.generate_sand(do_print=False)
    print(cave)
    units = sum(material == Material.SAND for material in cave.grid.values())
    print(units)


if __name__ == '__main__':
    main()
