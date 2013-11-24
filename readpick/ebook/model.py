import uuid
import logging
import tempfile
import random
import string
import urllib2 as urllib
from contextlib import closing

from bs4 import BeautifulSoup
from readpick.ebook.mobilizer import InstapaperMobilizer

logger = logging.getLogger(__name__)

default_not_found_template = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <!-- instapaper:crawl-error -->
        <title>Not available</title>
        <meta name="viewport" content="width=460; user-scalable=false" />
    </head>
    <body style="font-size: 22px;">
        <div style="margin: 30px auto; text-align: center; width: 350px; background-color: #ffd; padding: 10px; border: 1px solid #ccc;">

            <h1 style="font-size: 30px;">Sorry, this page is not available for mobilizing.</h1>
            
            <p>
                <a href="%s" style="color: #00f; font-weight: bold;">Open the original page</a>
            </p>
        </div>

    </body>
</html>'''


def id_generator(r = 8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(r))

#TODO: refactor in the same way jira-python is built

class Ebook(object):
    """
    request = '''{
        "author": "Jakub Marchwicki",
        "ebook_title": "Sample readpick.com ebook",
        "sections": [
            {
                "name": "The Unread list",
                "articles": [
                    {
                        "url": "http://t.co/VV5nVqi",
                        "title": "Optional page title"
                    },
                    {
                        "url": "http://m.onet.pl/wiadomosci/4986407,detal.html"
                    }
                ]
            },
            {
                "name": "The best of the best",
                "articles": [
                    {
                        "url": "http://www.uie.com/brainsparks/2011/12/30/the-hands-vs-the-brains/"
                    }
                ]
            }
        ]
    }'''

    Ebook.fromJson(request)

    #TODO: validate model upfront - raise exceptions where model is not correct
    #TODO: http://www.alexconrad.org/2011/10/json-validation.html
    """
    uuid = uuid.uuid1()
    ebook_title = None 
    author = None
    publisher = "readpick.com"
    sections = []
    
    def __init__(self, **entries):
        self.uuid = uuid.uuid1()
        self.ebook_title = None
        self.author = None
        self.publisher = "readpick.com"
        self.sections = []
        
        if entries is not None:
            self.__dict__.update(entries)
            self.sections = [Section.fromDict(section) for section in self.sections]
        
    @classmethod
    def fromJson(cls, request):
        import json
        o = json.loads(request)
        return cls(**o)
        
    def download(self, mobilizer=InstapaperMobilizer()):
        [section.download(mobilizer) for section in self.sections]

    def is_download_completed(self):
        downloaded = True
        [downloaded and section.is_download_completed() for section in self.sections]
        logger.debug("Ebook download completed.")
        return downloaded



class Section(object):
    name = "Unread list"
    articles = []
    
    def __init__(self, **entries):
        self.name = "Unread list"
        self.articles = []
        
        if entries is not None:
            self.__dict__.update(entries)
            self.articles = [Page.fromDict(art) for art in self.articles]            
    
    @classmethod
    def fromDict(cls, o):
        return cls(**o)
    
    def download(self, mobilizer):
        [article.download_text(mobilizer) for article in self.articles]

    def is_download_completed(self):
        downloaded = True
        [downloaded and page.is_download_completed() for page in self.articles]
        logger.debug("Section download completed.")
        return downloaded



class Page(object):

    downloaded = False
    url = None
    filename = None
    title = None
    text = None
    images = {}
    include_in_toc = True
    
    def __init__(self, **entries):
        self.url = None
        self.filename = None
        self.title = None
        self.text = None
        self.images = {}
        self.include_in_toc = True
        
        if entries is not None:
            self.__dict__.update(entries)

    @classmethod
    def fromDict(cls, o):
        return cls(**o)

    def download_text(self, mobilizer):
        import time
        time.sleep(30)

        if self.filename is None:
            self.filename = 'text_%s.html' % id_generator()
        
        if self.text is None:
            logger.debug("Downloading url: %s" % self.url)
            
            #grab url
            with closing(urllib.urlopen(mobilizer.url(self.url))) as article:
                #convert to soup
                soup = BeautifulSoup(article.read())
            
                #check for not mobilized pages
                if mobilizer.is_correctly_mobilized(soup) is False:
                    soup = BeautifulSoup(default_not_found_template % self.url)
                    logger.debug("URL wasn't properly mobilized - substituted with default page")

                soup = mobilizer.post_process_html(soup)

                self.text = tempfile.TemporaryFile()
                self.text.write(soup.prettify().encode('utf-8'))
                self.text.seek(0)
            
                #TODO: try catch in case html doesn't have title tags
                if self.title is None:
                    self.title = soup.html.head.title.string
    
            logger.info("Downloaded url: %s" % self.url)
        else:
            logger.info("Page text present - no need to download %s" % self.url)
        
        self.download_images()

        logger.debug("Page download completed.")
        self.downloaded = True
        
    def download_images(self, domain=None):
        soup = BeautifulSoup(self.text)
        
        image_list = soup.findAll("img")
        #list all images and download        
        for image in image_list:
            src = image['src']

            logger.debug("Downloading image %s" % src)
            #ignore dynamic / 'ad-based-images' - images without suffix
            suffix = src[src.rfind('.'):]
            if len(suffix) > 5 or not src.startswith('http'):
                logger.debug("Could not download: %s" % src)
                image.extract()
                continue

            with closing(urllib.urlopen(src)) as imgsrc:
                i = tempfile.TemporaryFile()
                i.write(imgsrc.read())
                i.seek(0)

                name = 'images/img_%s%s' % (id_generator(), suffix)
                image['src'] = name
                self.images[name] = i

        self.text = tempfile.TemporaryFile()
        self.text.write(soup.prettify().encode('utf-8'))
        self.text.seek(0) 

        if len(self.images) > 0:
            logger.info("Downloaded %s images for url: %s" % (len(self.images), self.url))

    def is_download_completed(self):
        return self.downloaded
