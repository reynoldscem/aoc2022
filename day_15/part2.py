from functools import cached_property
from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def distance(self, other):
        difference = self.sub(other)

        return difference.norm

    @cached_property
    def norm(self):
        return sum(abs(component) for component in self.coordinates)

    @cached_property
    def coordinates(self):
        return (self.x, self.y)

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __str__(self):
        return f'({self.x}, {self.y})'


class Ball:
    def __init__(self, vector, radius):
        self.vector = vector
        self.radius = radius

    @classmethod
    def from_vector_pair(cls, first, second):
        radius = first.distance(second)
        return cls(first, radius)

    def in_ball(self, vector):
        return self.vector.distance(vector) <= self.radius

    def __str__(self):
        return f'Ball of radius {self.radius} centred at {self.vector}'

    def __contains__(self, vector):
        return self.in_ball(vector)

    @property
    def min_x(self):
        return self.vector.x - self.radius

    @property
    def max_x(self):
        return self.vector.x + self.radius

    @property
    def centre(self):
        return self.vector

    def outside_boundary(self):
        def generator():
            dilated_radius = (self.radius + 1)
            coordinate = Vector(
                self.centre.x - dilated_radius,
                self.centre.y
            )
            for offset in range(0, dilated_radius + 1):
                yield coordinate
                coordinate = Vector(
                    coordinate.x + 1,
                    coordinate.y - 1
                )
            for offset in range(0, dilated_radius + 1):
                yield coordinate
                coordinate = Vector(
                    coordinate.x + 1,
                    coordinate.y + 1
                )
            for offset in range(0, dilated_radius + 1):
                yield coordinate
                coordinate = Vector(
                    coordinate.x - 1,
                    coordinate.y + 1
                )
            for offset in range(0, dilated_radius + 1):
                yield coordinate
                coordinate = Vector(
                    coordinate.x - 1,
                    coordinate.y - 1
                )
        return generator()


def parse_line(line):
    from re import findall

    return tuple(map(int, findall(r'(-?\d+)', line)))


def potential_beacon_locations(balls, bound):
    for ball in balls:
        for vector in ball.outside_boundary():
            if vector.x < 0 or vector.y < 0:
                continue
            if vector.x > bound or vector.y > bound:
                continue
            if not any(vector in test_ball for test_ball in balls):
                yield vector


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        lines = fd.read().strip().splitlines()

    coordinate_values = [
        parse_line(line)
        for line in lines
    ]

    vector_pairs = [
        (Vector(first_x, first_y), Vector(second_x, second_y))
        for (first_x, first_y, second_x, second_y) in coordinate_values
    ]
    balls = [
        Ball.from_vector_pair(first, second)
        for first, second in vector_pairs
    ]

    bound = 4000000
    beacon = next(potential_beacon_locations(balls, bound))
    print(beacon)
    tuning_frequency = beacon.x * bound + beacon.y
    print(tuning_frequency)


if __name__ == '__main__':
    main()
