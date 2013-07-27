# coding=UTF-8

import tempfile
import zipfile
import mimetypes
import logging

from jinja2 import Template

logger = logging.getLogger(__name__)


class SystemFile(object):
    filename = None;
    content = None;

    def __init__(self, filename, content):
        self.filename = filename
        self.content = content


class Epub(object):

    __all_pages = []
    system_files = None
    ebook = None

    def __init__(self, ebook):
        system_files = {}

        #create templates for META-INF/containter.xml
        system_files["META-INF/containter.xml"] = container_xml

        #create templates for OEBPS/content.opf
        self.__all_pages = reduce(lambda x, y: x+y, [section.articles for section in ebook.sections])
        all_images = reduce(lambda x,y: x+y, [page.images.keys() for page in self.__all_pages])
        content_opf_data = {"ebook": ebook,
                            "htmls": map(lambda x: x.filename, self.__all_pages),
                            "images": map(lambda x: {"name": x, "mediaType": mimetypes.guess_type(x)[0]}, all_images)}

        if len(self.__all_pages) == 1:
            #render single article
            content_opf_data["ebook"].ebook_title = self.__all_pages[0].title
            system_files["OEBPS/content.opf"] = single_document_content_opf.render(content_opf_data)
        else:
            #render multiple articles content and other files
            system_files["OEBPS/content.opf"] = content_opf.render(content_opf_data)

            #create templates for OEBPS/title-page.html
            system_files["OEBPS/title-page.html"] = titlepage_html.render({"ebook": ebook})

            #create templates for OEBPS/toc.html
            system_files["OEBPS/toc.html"] = toc_html.render({"ebook": ebook})

            #create templates for OEBPS/toc.ncx
            system_files["OEBPS/toc.ncx"] = toc_ncx.render({"ebook": ebook})

        self.system_files = system_files
        self.ebook = ebook

    def create_archive(self):
        archive = tempfile.TemporaryFile()

        filelist = []
        with zipfile.ZipFile(archive, "w") as fout:
            filelist.append("mimetype")
            fout.writestr('mimetype', 'application/epub+zip', compress_type = zipfile.ZIP_STORED)
            for (filename, content) in self.system_files.items():
                filelist.append(filename)
                fout.writestr(filename, content.encode("utf-8"), compress_type = zipfile.ZIP_DEFLATED)
            for page in self.__all_pages:
                filelist.append("OEBPS/%s" % page.filename)
                fout.writestr('OEBPS/%s' % page.filename, page.text.read(), compress_type = zipfile.ZIP_DEFLATED)
                for (name, image) in page.images.items():
                    filelist.append("OEBPS/%s" % name)
                    fout.writestr('OEBPS/%s' % name, image.read(), compress_type = zipfile.ZIP_DEFLATED)


        logger.info("Created zipfile size: %s" % convert_bytes(archive.tell()))
        logger.debug("Archive file list: %s" % filelist)
        archive.seek(0)
        return archive


def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size


container_xml = u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''

single_document_content_opf = Template(u'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<opf:package xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="readpick" version="2.0">
  <opf:metadata>
    <dc:identifier id="bookid">urn:uuid:{{ ebook.uuid }}</dc:identifier>
    <dc:language>en-US</dc:language>
    <dc:title>{{ ebook.ebook_title }}</dc:title>
    <dc:creator opf:role="aut">{{ ebook.author }}</dc:creator>
    <dc:publisher>readpick.com</dc:publisher>
  </opf:metadata>
  <opf:manifest>
    <opf:item id="html_001" media-type="application/xhtml+xml" href="{{ htmls[0] }}"/>
    {% for item in images %}<opf:item id="image_00{{ loop.index }}" media-type="{{ item.mediaType }}" href="{{ item.name }}"/>
    {% endfor %}
  </opf:manifest>
  <opf:spine toc="ncxtoc">
    <opf:itemref idref="html_001" linear="yes"/>
  </opf:spine>
</opf:package>

''')

content_opf = Template(u'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<opf:package xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="readpick" version="2.0">
  <opf:metadata>
    <dc:identifier id="bookid">urn:uuid:{{ ebook.uuid }}</dc:identifier>
    <dc:language>en-US</dc:language>
    <dc:title>{{ ebook.ebook_title }}</dc:title>
    <dc:creator opf:role="aut">{{ ebook.author }}</dc:creator>
    <dc:publisher>readpick.com</dc:publisher>
    <dc:subject>News</dc:subject>
    <opf:x-metadata>
      <output content-type="application/x-mobipocket-subscription-magazine" encoding="utf-8"/>
    </opf:x-metadata>
  </opf:metadata>
  <opf:manifest>
    <opf:item id="ncxtoc" media-type="application/x-dtbncx+xml" href="toc.ncx"/>
    <opf:item id="html_001" media-type="application/xhtml+xml" href="title-page.html"/>
    <opf:item id="html_002" media-type="application/xhtml+xml" href="toc.html"/>
    {% for item in htmls %}<opf:item id="html_00{{ loop.index + 2 }}" media-type="application/xhtml+xml" href="{{ item }}"/>
    {% endfor %}
    {% for item in images %}<opf:item id="image_00{{ loop.index }}" media-type="{{ item.mediaType }}" href="{{ item.name }}"/>
    {% endfor %}
  </opf:manifest>
  <opf:spine toc="ncxtoc">
    <opf:itemref idref="html_001" linear="yes"/>
    {% for item in htmls %}<opf:itemref idref="html_00{{ loop.index + 2 }}" linear="yes"/>
    {% endfor %}
  </opf:spine>
  <opf:guide>
    <opf:reference href="title-page.html" type="title-page" title="Title Page"/>
    <opf:reference href="toc.html" type="toc" title="Table of Contents"/>
  </opf:guide>
</opf:package>

''')

titlepage_html = Template(u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <title>{{ ebook.ebook_title }}</title>
  <style type="text/css">
.title, .authors {
  text-align: center;
}
span.author {
  margin: 1em;
}
  </style>
</head>
<body>
  <h1 class="title">{{ ebook.ebook_title }}</h1>
  <h3 class="authors">
  <span class="author">{{ ebook.author }}</span>
  </h3>
</body>
</html>

''')

toc_html = Template(u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <title>{{ ebook.ebook_title }}</title>
  <style type="text/css">
.tocEntry-1 {
}
.tocEntry-2 {
    text-indent: 1em;
}
.tocEntry-3 {
    text-indent: 2em;
}
.tocEntry-4 {
    text-indent: 3em;
}
  </style>
</head>
<body>
    <div class="tocEntry-1">
      <a href="title-page.html">{{ ebook.ebook_title }}</a>
    </div>
    {% for section in ebook.sections %}{% for item in section.articles %}{% if loop.index == 1 %}<div class="tocEntry-2">
      <a href="{{ item.filename }}">{{ section.name }}</a>
    </div>
    {% endif %}{% if item.include_in_toc %}<div class="tocEntry-3">
      <a href="{{ item.filename }}">{{ item.title }}</a>
    </div>{% endif %}{% endfor %}{% endfor %}
</body>
</html>


''')

toc_ncx = Template(u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:{{ ebook.uuid }}"/>
    <meta name="dtb:depth" content="3"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{{ ebook.ebook_title }}</text>
  </docTitle>
  <navMap>
    <navPoint class="periodical" id="periodical" playOrder="1">
      <navLabel><text>{{ ebook.ebook_title }}</text></navLabel>
      <content src="title-page.html"/>
      {% for section in ebook.sections %}<navPoint class="section" id="section" playOrder="2">
        <navLabel><text>{{ section.name }}</text></navLabel>
        <content src="{{ section.articles[0].filename }}"/>
          {% for item in section.articles %}{% if item.include_in_toc %}<navPoint class="article" id="navPoint-{{ loop.index + 2 }} " playOrder="{{ loop.index + 2 }}">
            <navLabel><text>{{ item.title }}</text></navLabel>
            <content src="{{ item.filename }}"/>
          </navPoint>
      {% endif %}{% endfor %}</navPoint>
    {% endfor %}</navPoint>
  </navMap>
</ncx>


''')