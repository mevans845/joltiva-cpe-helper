from get_envrion import get_env
import argparse

VERSION = get_env('VERSION')


def main(args):
    print(f'Hello {args.name}! This is version {args.version}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default='Placeholder', help='Your name')
    parser.add_argument('--version', type=str, default=VERSION)
    parser.add_argument('--directory', type=str, default='./tmp', help='Directory to watch')
    parser.add_argument('--directory-to-move', type=str, default='./non-prod/', help='Directory to move files to')
    parsed_args = parser.parse_args()
    main(args=parsed_args)
    print(VERSION)
