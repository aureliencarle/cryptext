import argparse


def arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        'session',
        metavar='s',
        type=str,
        nargs='?',
        help='store the session name',
    )
    parser.add_argument(
        '--label',
        '-l',
        nargs=1,
        help='label name',
    )
    return parser.parse_args()
