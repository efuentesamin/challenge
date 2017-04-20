#! /usr/bin/env python3
import argparse


def main():
    arg_parser = argparse.ArgumentParser(description='<-------- Polymath Ventures Engineering Challenge -------->')
    arg_group = arg_parser.add_mutually_exclusive_group(required=True)
    arg_group.add_argument(
        "--rebuild",
        action="store_true",
        help='Rebuilds the categories database from the API response.'
    )
    arg_group.add_argument(
        "--render",
        type=int,
        help='Generates an HTML file with the category tree based on the supplied <cat_id>.',
        metavar='<cat_id>'
    )
    args = arg_parser.parse_args()

    if args.rebuild:
        print('--------> Building Data Base...')
    elif args.render is not None:
        print('--------> Building {}.html file...'.format(args.render))


if __name__ == '__main__':
    main()

