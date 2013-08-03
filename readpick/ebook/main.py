#!/usr/bin/env python
"""Main readlist-ebook-parser"""

import sys
import argparse
import logging
import shutil
from readpick.ebook.model import Ebook
from readpick.ebook.epub import Epub

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    parser = argparse.ArgumentParser(description='Process reading lists to and save it as an ebook')
    parser.add_argument('-t', '--type', nargs='?', choices=['epub', 'mobi'], default='epub',
                        help='Output file type')
    parser.add_argument('-o', '--output', nargs='?', help='Output file name', required=True)

    args = parser.parse_args()
    logger.debug('Command line params %s' % args)
    controller(args)


def controller(args):

    input_json = ''.join(sys.stdin.readlines())
    ebook = Ebook.fromJson(input_json)
    ebook.download()
    if ebook.is_download_completed():
        epub = Epub(ebook)
        archive = epub.create_archive()
        shutil.copyfileobj(archive, open(args.output, 'w'))


if __name__ == "__main__":
    run()

