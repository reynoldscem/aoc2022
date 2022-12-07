from abc import ABC, abstractmethod
from argparse import ArgumentParser
from itertools import islice
from pathlib import Path


TOTAL_DISK_SPACE = 70000000
UNUSED_SPACE_REQUIRED = 30000000


class FileSystemNode(ABC):
    @abstractmethod
    def size(self):
        pass

class Directory(FileSystemNode):
    def __init__(self, name):
        self.name = name
        self.children = dict()

    def add_child(self, child):
        self.children[child.name] = child
        child.parent = self

    @property
    def size(self):
        return sum(child.size for child in self.children.values())


class File(FileSystemNode):
    def __init__(self, name, size):
        self.name = name
        self._size = size
        self.parent = None

    @property
    def size(self):
        return self._size


class Machine:
    def __init__(self):
        self.working_directory = None

    def cd(self, destination):
        if not self.working_directory:
            self.working_directory = Directory(destination)
        elif destination == '..':
            self.working_directory = self.working_directory.parent
        else:
            self.working_directory = self.working_directory.children[destination]

    @staticmethod
    def make_fs_node(line):
        if line.startswith('dir'):
            _, dirname = line.split()
            return Directory(dirname)

        size, filename = line.split()

        return File(filename, int(size))

    def trace(self, command, output_lines=None):
        print(command)
        print(output_lines)
        print()
        if command.startswith('cd'):
            _, dest_directory = command.split()
            self.cd(dest_directory)

        for line in output_lines:
            node = self.make_fs_node(line)
            self.working_directory.add_child(node)


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

    # Get each command with lines of its output
    commands_with_outputs = [
        command.strip().splitlines()
        for command in data.split('$')
        if command
    ]

    all_directories = set()

    machine = Machine()
    for entry in commands_with_outputs:
        command, *output_lines = entry
        machine.trace(command, output_lines)
        all_directories.add(machine.working_directory)

    filesystem_size = max(directory.size for directory in all_directories)
    size_remaining = TOTAL_DISK_SPACE - filesystem_size

    extra_space_required = UNUSED_SPACE_REQUIRED - size_remaining

    print(f'Size remaining is {size_remaining}')
    print(f'Extra required is {extra_space_required}')
    directories_by_size = sorted(
        all_directories,
        key=lambda directory: directory.size
    )
    for directory in directories_by_size:
        if directory.size >= extra_space_required:
            print(directory.size)
            print(directory.name)
            break


if __name__ == '__main__':
    main()
