import logging
import unittest
import re
from bs4 import BeautifulSoup

import readpick.ebook.model as model

class EbookModelTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(format="[%(name)s] %(levelname)s: %(message)s",
                            level=logging.DEBUG)

    def test_page_download(self):
        p = model.Page()
        p.url = "http://www.cooper.com/2011/03/06/more_better_faster_ux_design"
        p.download_text()

        self.assertEqual(len(p.images), 4)

        text = p.text.read()
        for image in p.images.keys():
            self.assertTrue(re.search(image, text))

    def test_multiple_url_download(self):
        s = model.Section()
        s.name = "section-name"
        s.articles.append(model.Page(url="http://sport.wp.pl/martykul.html?wid=14377651"))
        s.articles.append(model.Page(url="http://sport.wp.pl/martykul.html?wid=14374592&"))

        s.download()
        filenames = set([x.filename for x in s.articles])
        self.assertEquals(len(filenames), 2)
        self.assertNotEqual(s.articles[0].filename, s.articles[1].filename)
        self.assertIsNotNone(s.articles[0].text)
        self.assertIsNotNone(s.articles[1].text)

    def test_multiple_text_pages(self):
        text1 = "12345 test-tekst"
        text2 = "98765 text-tekst-2"

        s = model.Section()
        s.name = "section-name"
        s.articles.append(model.Page(text=text1))
        s.articles.append(model.Page(text=text2))

        s.download()
        filenames = set([x.filename for x in s.articles])
        self.assertEquals(len(filenames), 2)
        self.assertNotEqual(s.articles[0].filename, s.articles[1].filename)
        self.assertEqual(s.articles[0].text.read().strip(), text1)
        self.assertEqual(s.articles[1].text.read().strip(), text2)

    def test_invalid_mobilizing(self):
        p = model.Page()
        p.url = "https://www.online.citibank.pl/retail/blue/img/logo.gif"

        p.download_text()

        self.assertEqual(len(p.images), 0)

        text = BeautifulSoup(p.text.read())
        self.assertEqual("Not available", text.html.head.title.string.strip())

class EbookMarshallingTest(unittest.TestCase):

    def test_json_unmarshall(self):
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

        ebook = model.Ebook.fromJson(request)
        self.assertEquals(ebook.author, "Jakub Marchwicki")
        self.assertEquals(ebook.ebook_title, "Sample readpick.com ebook")
        self.assertEquals(len(ebook.sections), 2)
        self.assertTrue(isinstance(ebook.sections[0], model.Section))
        self.assertEquals(len(ebook.sections[0].articles), 2)
        self.assertTrue(isinstance(ebook.sections[0].articles[0], model.Page))

if __name__ == '__main__':
    unittest.main()