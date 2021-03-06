#!/usr/bin/env python
"""Main readlist-ebook-parser"""

import argparse
import logging
import json
from datetime import date
from readpick.readlists.pocket import Pocket3 as Pocket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    parser = argparse.ArgumentParser(description='Download reading list items')
    parser.add_argument('-u', '--username', nargs='?', help='Pocket username', required=True)
    parser.add_argument('-p', '--password', nargs='?', help='Pocket password', required=True)
    parser.add_argument('-c', '--count', nargs='?', help='Number of articles to download', default=10)
    parser.add_argument('-f', '--favourite', help='Download only favourite', action="store_true")
    parser.add_argument('-mu', '--modify_unfav', help='Modify unfavourite after download', action="store_true")
    parser.add_argument('-ma', '--modify_arch', help='Modify archive after download', action="store_true")
    parser.add_argument('-s', '--sort', nargs='?', help='Sorting order', default='newest')

    args = parser.parse_args()
    logger.debug('Command line params %s' % args)
    controller(args)


def controller(args):
    pocket = Pocket(username=args.username,
                    password=args.password,
                    favourite=args.favourite,
                    count=args.count)
    article_list = pocket.get_list()

    items = map(lambda x: x['item_id'], article_list)
    if args.modify_unfav:
        pocket.modify(items, 'unfavorite')

    if args.modify_arch:
        pocket.modify(items, 'archive')


    print output_template % (date.today().strftime("%d/%m/%Y"), json.dumps(article_list, indent=8))


output_template = """{
    "author": "Jakub Marchwicki",
    "ebook_title": "Readlist %s",
    "sections": [
        {
            "name": "The Unread list",
            "articles": %s
        }
    ]
}"""

if __name__ == "__main__":
    run()

