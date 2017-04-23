#! /usr/bin/env python3
import argparse
from controllers.data_base import DataBaseController
from controllers.render import RenderController


def main():
    """
    Entry point for Polymath Ventures Engineering Challenge
    :return: None
    """
    args = get_args()

    if args.rebuild:
        DataBaseController().rebuild()
    elif args.render is not None:
        RenderController.render(args.render)


def get_args():
    """
    Parses and return args
    :return: Parsed args
    """
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
        help='Generates an HTML file with the category tree based on the supplied <cat_id>. (i. e. --render 20081)',
        metavar='<cat_id>'
    )
    return arg_parser.parse_args()


if __name__ == '__main__':
    main()

