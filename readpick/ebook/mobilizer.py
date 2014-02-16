# coding=UTF-8

import re
import urllib2 as urllib
from contextlib import closing
from bs4 import BeautifulSoup, Comment


#TODO: different mobilizer than instapaper
class InstapaperMobilizer(object):
    mobilizer_url = "http://mobilizer.instapaper.com/m?u=%s"

    def url_content(self, base_url):
        with closing(urllib.urlopen(self.mobilizer_url % base_url)) as article:
            return BeautifulSoup(article.read())

    def is_correctly_mobilized(self, soup):
        return True

    #TODO: correct mobilization check
    #        return False if soup.find(text=re.compile('Instapaper')) is None else True

    def post_process_html(self, soup):
        #check for invalid html
        if soup.find(text=re.compile("instapaper:crawl-error")) is not None:
            return soup

        #stip comments
        [comment.extract() for comment in soup.findAll(text=lambda text: isinstance(text, Comment))]

        #remove <script/> tag
        [tag.extract() for tag in soup.findAll('script')]

        #TODO: correct invalid <link> tag (not closed) and rerun
        #remove <link /> tag
        #        [tag.extract() for tag in soup.findAll('link')]

        #remove onload attribute from <body />
        body = soup.find('body')
        del (body['onload'])
        del (body['onclick'])

        #remove text_controls (tags and actual controls)
        [tag.extract() for tag in soup.findAll('span', attrs={'class': 'orig_line'})]
        [tag.extract() for tag in soup.findAll('div', attrs={'id': 'controlbar_container'})]
        [tag.extract() for tag in soup.findAll('div', attrs={'id': 'footer'})]

        return soup
