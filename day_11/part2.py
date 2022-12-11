from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm
from math import prod
import re


class MonkeyOrechestrator:
    def __init__(self, modulus):
        self.monkeys = dict()
        self.modulus = modulus

    @staticmethod
    def first_integer(string):
        from re import search
        return int(search(r'\d+', string).group())

    @staticmethod
    def all_integers(string):
        from re import findall
        return list(map(int, findall(r'\d+', string)))

    @staticmethod
    def make_operation_function(string):
        import re

        pattern = r'\W*Operation: new =\W*(.*)'
        operation_string = re.match(pattern, string).group(1)

        def operation(old):
            return eval(operation_string)

        return operation

    def make_monkey_from_string(self, string):
        lines = [
            line.strip()
            for line in string.strip().split('\n')
        ]
        (
            index_line,
            items_line,
            operation_line,
            condition_line,
            true_case_line,
            false_case_line
        ) = lines

        monkey_index = self.first_integer(index_line)
        items = self.all_integers(items_line)

        operation_function = self.make_operation_function(operation_line)

        test_divisor = self.first_integer(condition_line)

        def test_function(worry_level):
            return (worry_level % test_divisor) == 0

        true_throw_index = self.first_integer(true_case_line)
        false_throw_index = self.first_integer(false_case_line)

        monkey = Monkey(
            self,
            monkey_index, items,
            operation_function,
            test_function,
            test_divisor,
            true_throw_index, false_throw_index
        )
        self.monkeys[monkey_index] = monkey
        self.monkeys = dict(sorted(self.monkeys.items()))

        return monkey

    def transfer(self, destination, item):
        destination_monkey = self.monkeys[destination]

        destination_monkey.items.append(item)

    @property
    def monkey_business(self):
        inspect_counts = [
            monkey.inspection_count
            for monkey in self.monkeys.values()
        ]
        *rest, second_largest, largest = sorted(inspect_counts)

        return second_largest * largest

    def round(self):
        for monkey in self.monkeys.values():
            monkey.round()

    def __str__(self):
        return '\n'.join(str(monkey) for monkey in self.monkeys.values())


class Monkey:
    def __init__(
            self, orchestrator,
            index, items,
            operation_function,
            test_function,
            test_divisor,
            true_throw_index, false_throw_index):

        self.orchestrator = orchestrator

        self.index = index
        self.items = items
        self.operation_function = operation_function
        self.test_function = test_function
        self.test_divisor = test_divisor
        self.true_throw_index = true_throw_index
        self.false_throw_index = false_throw_index

        self.inspection_count = 0

    def inspect(self, item):
        self.inspection_count += 1
        return self.operation_function(item)

    def handle_items(self):
        while self.items:
            item = self.items.pop(0)
            if self.test_function(item):
                yield self.true_throw_index, item
            else:
                yield self.false_throw_index, item

    def round(self):
        self.items = [
            item % self.orchestrator.modulus
            for item in self.items
        ]

        self.items = [
            self.inspect(item)
            for item in self.items
        ]

        for destination, item in self.handle_items():
            self.orchestrator.transfer(destination, item)

    def __str__(self):
        item_string = ', '.join(map(str, self.items))
        return f'Monkey {self.index}: {item_string}'


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
        data = fd.read()

    divisor_strings = re.findall(r'divisible by (\d+)', data)
    modulus = prod(map(int, divisor_strings))

    monkey_spec = data.split('\n\n')
    orchestrator = MonkeyOrechestrator(modulus)
    for monkey_spec in monkey_spec:
        orchestrator.make_monkey_from_string(monkey_spec)

    for round_index in tqdm(range(1, 10001)):
        orchestrator.round()
        print(
            f'After round {round_index}, '
            'the monkeys are holding items with these worry levels:'
        )
        print(orchestrator)
        print(orchestrator.monkey_business)


if __name__ == '__main__':
    main()
