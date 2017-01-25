# -*- coding: utf-8 -*-
"""
You need to fill in your API key from google below. Note that querying
supported languages is not implemented.
Language Code
-------- ----
Afrikaans 	af
Albanian 	sq
Arabic 	ar
Belarusian 	be
Bulgarian 	bg
Catalan 	ca
Chinese Simplified 	zh-CN
Chinese Traditional 	zh-TW
Croatian 	hr
Czech 	cs
Danish 	da
Dutch 	nl
English 	en
Estonian 	et
Filipino 	tl
Finnish 	fi
French 	fr
Galician 	gl
German 	de
Greek 	el
Hebrew 	iw
Hindi 	hi
Hungarian 	hu
Icelandic 	is
Indonesian 	id
Irish 	ga
Italian 	it
Japanese 	ja
Korean 	ko
Latvian 	lv
Lithuanian 	lt
Macedonian 	mk
Malay 	ms
Maltese 	mt
Norwegian 	no
Persian 	fa
Polish 	pl
Portuguese 	pt
Romanian 	ro
Russian 	ru
Serbian 	sr
Slovak 	sk
Slovenian 	sl
Spanish 	es
Swahili 	sw
Swedish 	sv
Thai 	th
Turkish 	tr
Ukrainian 	uk
Vietnamese 	vi
Welsh 	cy
Yiddish 	yi
"""
import sys
import re
import simplejson
import json


import sys
import re
import goslate

if (sys.version_info[0] < 3):
    import urllib2
    import urllib
    import HTMLParser
else:
    import html.parser
    import urllib.request
    import urllib.parse

### Hard-coded variables ###


api = 'YOUR-API-KEY-GOES-HERE'

languages = ["af", "sq", "ar","be", "bg", "ca", "zh-CN", "zh-TW", "hr",
             "cs", "da", "nl", "en", "et", "tl", "fi", "fr", "gl", "de",
             "el", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "ko",
             "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro",
             "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk",
             "vi", "cy", "yi"]

agent = {'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
}

def unescape(text):
    if (sys.version_info[0] < 3):
        parser = HTMLParser.HTMLParser()
    else:
        parser = html.parser.HTMLParser()
    return (parser.unescape(text))


def google_translate(to_translate, from_language="auto", to_language="auto"):
    """Returns the translation using google translate
    you must shortcut the language you define
    (French = fr, English = en, Spanish = es, etc...)
    if not defined it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?
    """
    '''
    base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    if (sys.version_info[0] < 3):
#        to_translate = urllib.quote_plus(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib2.Request(link, headers=agent)
        raw_data = urllib2.urlopen(request).read()
    else:
#        to_translate = urllib.parse.quote(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib.request.Request(link, headers=agent)
        raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)
    '''
    gs = goslate.Goslate()
    return gs.translate(to_translate, 'en')


