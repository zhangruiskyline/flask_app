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


import json
try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote


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


def online_translate(to_translate, from_language="auto", to_language="auto"):
    api_url = "http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s"
    req = request.Request(url=api_url % (to_translate, from_language, 'en'),
                              headers=agent)

    # url="http://translate.google.com/translate_a/t?clien#t=p&ie=UTF-8&oe=UTF-8"
    # +"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
    # , headers = headers)
    r = request.urlopen(req)
    return r.read().decode('utf-8')


