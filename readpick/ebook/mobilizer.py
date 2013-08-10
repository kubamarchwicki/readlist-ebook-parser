# coding=UTF-8

import logging
import re

from bs4 import BeautifulSoup, Comment


class InstapaperMobilizer(object):
    mobilizer_url = "http://www.instapaper.com/m?u=%s"

    def url(self, base_url):
        return self.mobilizer_url % base_url

    def is_correctly_mobilized(self, soup):
        return False if soup.find(text=re.compile('Instapaper')) is None else True

    def post_process_html(self, soup):

        #check for invalid html
        if soup.find(text=re.compile("instapaper:crawl-error")) is not None:
            return soup

        #stip comments
        [comment.extract() for comment in soup.findAll(text=lambda text:isinstance(text, Comment))]

        #remove <script/> tag
        [tag.extract() for tag in soup.findAll('script')]

        #remove <link /> tag
        [tag.extract() for tag in soup.findAll('link')]

        #remove onload attribute from <body />
        body = soup.find('body')
        del(body['onload'])
        del(body['onclick'])

        #remove text_controls (tags and actual controls)
        [tag.extract() for tag in soup.findAll('span', attrs = {'class': 'orig_line'})]
        [tag.extract() for tag in soup.findAll('div', attrs = {'id': 'controlbar_container'})]
        [tag.extract() for tag in soup.findAll('div', attrs = {'id': 'footer'})]

        return soup