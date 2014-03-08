# coding=UTF-8

import unittest
import logging
import urllib2 as urllib

from bs4 import BeautifulSoup
from readpick.ebook.mobilizer import InstapaperMobilizer

class MockedInstapaperMobilizerTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(format="[%(name)s] %(levelname)s: %(message)s", 
                    level=logging.DEBUG)

    def test_correct_mobilization(self):
        soup = BeautifulSoup('''<html>
    <head>
        <title>Wkr&oacute;tce zmiany w egzaminach na prawo jazdy</title>
        <meta name="viewport" content="width=device-width; initial-scale=1.0; user-scalable=no; minimum-scale=1.0; maximum-scale=1.0;" />
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="robots" content="noindex"/>
        <link rel="icon" href="/images/favicon.png"/>
<!-- IP:TITLE
Wkrótce zmiany w egzaminach na prawo jazdy
/IP:TITLE -->
<!-- IP:IMAGES

/IP:IMAGES -->

        <style type="text/css">
            body {
                font-family: Georgia;
                font-size: 16px;
                margin: 0px auto 0px auto;
                width: 500px                                word-wrap: break-word;
            }
            
            h1 { font-size: 1.3em; }
            h2 { font-size: 1.15em; }
            h3, h4, h5, h6, h7 { font-size: 1.0em; }
            
            img { border: 0; display: block; margin: 0.5em 0; }
            pre, code { overflow: scroll; }
            #story { 
                                clear: both; padding: 0 10px; overflow: hidden; margin-bottom: 40px; 
            }

            .bar {
                color: #555;
                font-family: 'Helvetica'; 
                font-size: 11pt;
                                    margin: 0 -20px;
                    padding: 10px 0;
                            }            
            .top { border-bottom: 2px solid #000; }
            
                        
            #story div {
                margin: 1em 0;
            }
            
            .bottom {
                border-top: 2px solid #000;
                color: #555;
            }

            .bar a { color: #444; }
            
            blockquote {
                border-top: 1px solid #bbb;
                border-bottom: 1px solid #bbb;
                margin: 1.5em 0;
                padding: 0.5em 0;
            }
            blockquote.short { font-style: italic; }
            
            pre {
                white-space: pre-wrap;
            }
            
            ul.bodytext, ol.bodytext {
                list-style: none;
                margin-left: 0;
                padding-left: 0em;
            }
            
                        #text_controls {
                color: #555; 
                text-align: center; 
                font-size: 16px;
            }
            
                #text_controls a {
                    text-decoration: none;
                    color: #555;
                }
                    </style>
                <script type="text/javascript">
            /* thanks, http://www.quirksmode.org/js/cookies.html */
            function createCookie(name,value,days) {
                if (days) {
                    var date = new Date();
                    date.setTime(date.getTime()+(days*24*60*60*1000));
                    var expires = "; expires="+date.toGMTString();
                }
                else var expires = "";
                document.cookie = name+"="+value+expires+"; path=/";
            }

            function readCookie(name) {
                var nameEQ = name + "=";
                var ca = document.cookie.split(';');
                for(var i=0;i < ca.length;i++) {
                    var c = ca[i];
                    while (c.charAt(0)==' ') c = c.substring(1,c.length);
                    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
                }
                return null;
            }

            var _fontSize, _fontFamily, _lineHeight, _width;
            
            function loadDefaults()
            {
                _fontSize = 16;
                _fontFamily = "G";
                _lineHeight = 1.5;
                _width = 500;
            }
            
            function saveFont()
            {
                applyFont();
                createCookie("fontMetrics", [_fontSize, _fontFamily, _lineHeight, _width].join("_"), 365);
            }
            
            function loadFont()
            {
                var cookieData = readCookie("fontMetrics");
                if (cookieData && (cookieData = cookieData.split("_")) && cookieData.length == 4) {
                    _fontSize = parseInt(cookieData[0]);
                    _fontFamily = cookieData[1];
                    _lineHeight = parseFloat(cookieData[2]);
                    _width = parseInt(cookieData[3]);
                } else loadDefaults();

                applyFont();
            }
            
            function applyFont()
            {
                if (_fontSize < 10) _fontSize = 10;
                else if (_fontSize > 48) _fontSize = 48;

                if (_width < 300) _width = 300;
                else if (_width > document.body.clientWidth - 80) _width = document.body.clientWidth - 80;
                
                if (_lineHeight > 3.0) _lineHeight = 3.0;
                else if (_lineHeight < 1.1) _lineHeight = 1.1;
                
                var story = document.getElementById('story');
                
                story.style.fontSize = _fontSize + "px";
                switch (_fontFamily) {
                    case "T": story.style.fontFamily = "Times, 'Times New Roman', serif"; break;
                    case "H": story.style.fontFamily = "Helvetica, Arial, sans-serif"; break;
                    case "V": story.style.fontFamily = "Verdana, sans-serif"; break;
                    default:
                    _fontFamily = "G";
                    story.style.fontFamily = "Georgia, serif"; break;
                }
                
                document.body.style.width = _width;                story.style.lineHeight = _lineHeight;
                
                // alert('set font: ' + [_fontSize, _fontFamily, _lineHeight, _width].join("_"));
            }
        </script>
            </head>
    <body onload="loadFont();">
        <div class="bar top">
                            <div style="font-size: 10pt;">
                    View full page: 
                    <a href="http://m.onet.pl/wiadomosci/4986708,detal.html">m.onet.pl/wiadomosci/4986708,detal.html</a>

                </div>
                    </div>
                    <div id="text_controls_toggle" style="float: left; margin-left: 10px; margin-bottom: 30px; height: 20px;">
                <a href="#" style="color: #555;" onclick="document.getElementById('text_controls_toggle').style.display = 'none'; document.getElementById('text_controls').style.display = 'block'; document.getElementById('editing_controls').style.display = 'none'; return false;">
                    <span style="font-size: 9px; letter-spacing: -3px;">A</span>
                    <span style="font-size: 16px;">A</span>
                </a>
            </div>

            <div id="text_controls" style="display: none;">
                <div style="float: left; margin-top: 5px;  margin-left: 10px; margin-bottom: 25px; height: 20px;">
                    <a href="#" style="text-decoration: underline;" onclick="document.getElementById('text_controls').style.display = 'none'; document.getElementById('text_controls_toggle').style.display = 'block'; document.getElementById('editing_controls').style.display = 'block'; return false;">
                        <span style="font-family: Helvetica, Arial, sans-serif; font-size: 11px;">close</span>
                    </a>
                </div>

                
                <a href="#" onclick="_fontSize--; saveFont(); return false;">&ndash;</a>
                                <span style="font-size: 9px; letter-spacing: -3px;">A</span>

                <span style="font-size: 16px;">A</span>
                                <a href="#" onclick="_fontSize++; saveFont(); return false;">+</a>
                &nbsp;&nbsp;&nbsp;&nbsp;                <a href="#" onclick="_lineHeight -= 0.1; saveFont(); return false;" style="border-top: 1px solid #555; border-bottom: 1px solid #555; font-size: 2px; padding: 0 5px; vertical-align: 4px;">&nbsp;</a>
                                <a href="#" onclick="_lineHeight += 0.1; saveFont(); return false;" style="border-top: 1px solid #555; border-bottom: 1px solid #555; font-size: 3px; padding: 0 5px; vertical-align: 4px;">&nbsp;</a>
                &nbsp;&nbsp;&nbsp;&nbsp;                                <a href="#" onclick="_width -= 20; saveFont(); return false;" style="border-top: 1px solid #555; border-bottom: 1px solid #555; border-left: 6px solid #555; border-right: 6px solid #555; font-size: 8px; padding: 0 2px; vertical-align: 4px;">&nbsp;</a>
                                <a href="#" onclick="_width += 20; saveFont(); return false;" style="border-top: 1px solid #555; border-bottom: 1px solid #555; border-left: 3px solid #555; border-right: 3px solid #555; font-size: 8px; padding: 0 4px; vertical-align: 4px;">&nbsp;</a>
                &nbsp;&nbsp;&nbsp;&nbsp;                                <a href="#" onclick="_fontFamily = 'G'; saveFont(); return false;"  style="font-family: Georgia, serif;">G</a>

                                <a href="#" onclick="_fontFamily = 'T'; saveFont(); return false;"  style="font-family: Times, 'Times New Roman', serif;">T</a>
                                <a href="#" onclick="_fontFamily = 'H'; saveFont(); return false;"  style="font-family: Helvetica, Arial, sans-serif;">H</a>
                                <a href="#" onclick="_fontFamily = 'V'; saveFont(); return false;"  style="font-family: Verdana, sans-serif;">V</a>
                &nbsp;&nbsp;&nbsp;&nbsp;
                                    <a href="#" onclick="loadDefaults(); saveFont(); return false;" style="font-family: Helvetica, Arial, sans-serif; font-size: 11px; vertical-align: 2px; text-decoration: underline;">defaults</a>
                            </div>
        
        <div id="editing_controls" style="float: right; padding-top: 2px;">

                    </div>
        
        <div id="story">
<div>
<div>
<div>
<p>Za niespełna półtora
miesiąca wejdą w życie nowe regulacje dotyczące
egzaminów na prawo jazdy. Od 11 lutego zaczną
obowiązywać rozporządzenia, które
zmieniają zasady egzaminu teoretycznego.</p>
</div>
<p>Kandydaci na kierowców nie będą
znali wcześniej pytań testowych. Poznają je w czasie
egzaminu. Ważnym elementem sprawdzianu będzie film,
podczas którego padną pytania dotyczące sytuacji na
drodze. Egzaminowani będą mieli na odpowiedź tylko
20 sekund. Zdaniem dyrektora Wojewódzkiego Ośrodka Ruchu
Drogowego w Warszawie Andrzeja Szklarskiego, zmiany poprawią
przygotowanie kierowców do jazdy. Jego zdaniem istniejący
system źle kształci kierowców, dlatego, że
dostają oni zestaw pytań i odpowiedzi, których
uczą się na pamięć. Nie są więc,
zdaniem szefa WORD-u, zrozumieć zasad ruchu drogowego.<br /><br />
W trzech warszawskich ośrodkach egzaminacyjnych nie ma
już miejsc na egzamin teoretyczny do 11 lutego. Wielu
kandydatów na kierowców, z którymi rozmawiało
Polskie Radio chce zrobić wszystko, żeby nie zdawać
egzaminu teoretycznego na nowych zasadach. Dyrekcja
Wojewódzkiego Ośrodka Ruchu Drogowego zapewnia, że
ośrodki szkolenia kierowców są już przygotowane
na wprowadzenie nowych zasad egzaminów.</p>
<p></p>


</div>

</div></div>
        
        <div class="bar bottom">
                            <p style="font-size: 10pt;">
                    View full page: <a href="http://m.onet.pl/wiadomosci/4986708,detal.html">m.onet.pl/wiadomosci/4986708,detal.html</a>
                </p>
                <p style="font-size: 10pt;">
                    Generated by 
                    <a href="http://www.instapaper.com/">Instapaper</a>'s
                    Text engine, which transforms web pages for easy
                    text reading on mobile devices.
                </p>

                    </div>
    </body>
</html>
''')
        mobilizer = InstapaperMobilizer()
        self.assertTrue(mobilizer.is_correctly_mobilized(soup), "Correctly mobilized")
        
    def test_incorrect_mobilization(self):
        soup = BeautifulSoup('''''')

        mobilizer = InstapaperMobilizer()
        self.assertFalse(mobilizer.is_correctly_mobilized(soup), "Not mobilized")


class InstapaperMobilizerTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(format="[%(name)s] %(levelname)s: %(message)s",
                            level=logging.DEBUG)

    def test_complete_download_and_mobilization(self):
        mobilizer = InstapaperMobilizer()
        u = urllib.urlopen(mobilizer.url("http://m.onet.pl/wiadomosci/4986708,detal.html"))
        soup = BeautifulSoup(u.read())
        self.assertTrue(mobilizer.is_correctly_mobilized(soup), "Correctly mobilized")
        soup = mobilizer.post_process_html(soup)
        print soup.prettify()

if __name__ == '__main__':
    unittest.main()