from argparse import ArgumentParser
from collections import defaultdict
from copy import deepcopy
from pathlib import Path


class VM:
    def __init__(self, instructions):
        self.registers = defaultdict(int)
        self.register_history = defaultdict(dict)
        self.instructions = instructions
        self.program_counter = 0
        self.cycles = 0

        self.opcode = None
        self.operands = []

        self.registers['x'] = 1

    def fetch_decode(self):
        try:
            instruction_string = self.instructions[self.program_counter]
            self.program_counter += 1
        except IndexError:
            raise StopIteration("Instructions exhausted")

        match instruction_string.split():
            case ['addx', offset]:
                self.opcode = 'add'
                self.operands = ['x', int(offset)]
            case _:
                self.opcode = 'noop'
                self.operands = []

    def cycle(self):
        self.register_history[self.cycles] = deepcopy(self.registers)
        self.cycles += 1

    def _add(self):
        self.cycle()
        self.cycle()
        dest, value = self.operands
        self.registers[dest] += value

    def _noop(self):
        self.cycle()

    def execute(self):
        instruction_table = {
            'add': self._add,
            'noop': self._noop
        }

        instruction_table[self.opcode]()

    def clock(self):
        self.fetch_decode()
        self.execute()

    def __next__(self):
        self.clock()
        return self

    def __iter__(self):
        return self

    def __str__(self):
        return f'Cycles: {self.cycles}, X: {self.registers["x"]}'


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

    lines = data.splitlines()
    for machine in iter(VM(lines)):
        pass

    cycle_range = range(20, 260, 40)
    print(
        sum(
            cycle * machine.register_history[cycle - 1]['x']
            for cycle in cycle_range
        )
    )


if __name__ == '__main__':
    main()
