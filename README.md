A small library to convert a reading list into an ebook
-------------------------------------------------------

## Usage:

Retrive list from Pocket
`python readpick/readlist/main.py -u [username] -p [password]`

Optional parameters

 * `-f` - download only favourites
 * `-c [num]` - define the number of articles (items) to download
 * `-s [newest|oldest]` - define sorting order
 * `-mu` - modify after downloading: unfavourite
 * '-ma` - modify after downloading: archive

Generate epub ebook
`python readpick/ebook/main.py -o [output_filename] << items_list.json`


## TODOs
* Create setup.py and list project (virtualenv) dependencies (BeautifulSoup, jinja2).
