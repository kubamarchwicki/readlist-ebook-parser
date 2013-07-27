#!/usr/bin/env python
"""Main readlist-ebook-parser"""

import argparse


def run():
    parser = argparse.ArgumentParser(description='Process reading lists to and save it as an ebook')
    parser.add_argument('-c', '--config', nargs=1, help='Configuration file')
    parser.add_argument('-d', '--data', nargs=1, help='Reading list data')
    parser.add_argument('-t', '--type', nargs=1, choices=['epub', 'mobi'], default='epub',
                        help='Output file type')
    parser.add_argument('-o', '--output', nargs=1, help='Output file name', required=True)

    args = parser.parse_args()
    print(args)



if __name__ == "__main__":
    run()

