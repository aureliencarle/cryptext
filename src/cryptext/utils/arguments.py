"""Argument parser for cryptext."""

import argparse


def parse_args() -> argparse.Namespace:
    """Return the parsed command-line arguments of the program."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        'session',
        metavar='s',
        type=str,
        nargs='?',
        help='store the session name',
    )
    parser.add_argument(
        '--label', '-l', nargs=1, help='label name',
    )
    return parser.parse_args()
