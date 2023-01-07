from get_envrion import get_env
import argparse

VERSION = get_env('VERSION')


def main(args):
    print(f'Hello {args.name}! This is version {args.version}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default='Placeholder', help='Your name')
    parser.add_argument('--version', type=str, default=VERSION)
    parsed_args = parser.parse_args()
    main(args=parsed_args)
    print(VERSION)
