#!/usr/bin/env python
"""Main readlist-ebook-parser"""

import argparse
import logging
import shutil
from model import Ebook
from epub import Epub

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    parser = argparse.ArgumentParser(description='Process reading lists to and save it as an ebook')
    parser.add_argument('-c', '--config', nargs='?', help='Configuration file')
    parser.add_argument('-d', '--data', nargs='?', help='Reading list data',
                        type=argparse.FileType('r'))
    parser.add_argument('-t', '--type', nargs='?', choices=['epub', 'mobi'], default='epub',
                        help='Output file type')
    parser.add_argument('-o', '--output', nargs='?', help='Output file name', required=True)

    args = parser.parse_args()
    logger.debug('Command line params %s' % args)
    controller(args)


def controller(args):

    ebook = Ebook.fromJson(args.data.read())
    ebook.download()
    if ebook.is_download_completed():
        epub = Epub(ebook)
        archive = epub.create_archive()
        shutil.copyfileobj(archive, open(args.output, 'w'))


if __name__ == "__main__":
    run()

