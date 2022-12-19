from argparse import ArgumentParser
from pathlib import Path


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input-filename', type=Path,
        required=True
    )

    return parser


def parse_line(line):
    from re import findall

    return tuple(map(int, findall(r'(-?\d+)', line)))


def plot_faces(faces):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure()
    ax = Axes3D(fig)
    fig.add_axes(ax)

    for i, face in enumerate(faces):
        poly = Poly3DCollection([face])
        poly.set_facecolor([f'C{i}'])
        poly.set_alpha(0.5)
        ax.add_collection3d(poly)

    plt.show()


def vector3_add(first, second):
    return tuple(
        first_entry + second_entry
        for first_entry, second_entry in zip(first, second)
    )


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        lines = fd.read().strip().splitlines()

    coordinates = [
        parse_line(line)
        for line in lines
    ]

    front_face = ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0))
    back_face = ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1))
    top_face = ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0))
    bottom_face = ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1))
    left_face = ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0))
    right_face = ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))

    canonical_faces = [
        front_face, back_face,
        top_face, bottom_face,
        left_face, right_face
    ]
    # plot_faces(canonical_faces)

    visible_faces = set()
    for coordinate in coordinates:
        cube_faces = set(
            tuple(sorted(set(
                vector3_add(reference_coordinate, coordinate)
                for reference_coordinate in face
            )))
            for face in canonical_faces
        )
        visible_faces ^= cube_faces
    print(len(visible_faces))


if __name__ == '__main__':
    main()
