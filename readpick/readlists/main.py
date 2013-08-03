#!/usr/bin/env python
"""Main readlist-ebook-parser"""

import argparse
import logging
import json
from datetime import date
from readpick.readlists.pocket import Pocket2 as Pocket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    parser = argparse.ArgumentParser(description='Download reading list items')
    parser.add_argument('-u', '--username', nargs='?', help='Pocket username')
    parser.add_argument('-p', '--password', nargs='?', help='Pocket password')
    parser.add_argument('-s', '--sort', nargs='?', help='Sorting order', default='newest')

    args = parser.parse_args()
    logger.debug('Command line params %s' % args)
    controller(args)


def controller(args):
    #so far - I'm not trying to log in a person and authorize
    pocket = Pocket(username=args.username, password=args.password)
    article_list = pocket.get_list()

    print output_template % (date.today().strftime("%d/%m"), json.dumps(article_list, indent=16))

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

