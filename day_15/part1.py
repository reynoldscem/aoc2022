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


def parse_line(line):
    from re import findall

    return tuple(map(int, findall(r'(-?\d+)', line)))


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        lines = fd.read().strip().splitlines()

    coordinate_values = [
        parse_line(line)
        for line in lines
    ]
    beacons = [
        Vector(second_x, second_y)
        for (_, _, second_x, second_y) in coordinate_values
    ]

    vector_pairs = [
        (Vector(first_x, first_y), Vector(second_x, second_y))
        for (first_x, first_y, second_x, second_y) in coordinate_values
    ]
    balls = [
        Ball.from_vector_pair(first, second)
        for first, second in vector_pairs
    ]
    x_min = min(ball.min_x for ball in balls)
    x_max = max(ball.max_x for ball in balls)

    y = 2000000
    test_vectors = (
        Vector(x, y)
        for x in range(x_min, x_max + 1)
    )
    count = sum(
        vector not in beacons and any(vector in ball for ball in balls)
        for vector in test_vectors
    )
    print(count)


if __name__ == '__main__':
    main()
