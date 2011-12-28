import urllib
from google.appengine.api import urlfetch

import json

import lxml
import lxml.html
from lxml import etree as ElementTree
from codecs import getdecoder, getencoder, getwriter, getreader 

import re
from StringIO import StringIO
from datetime import datetime


def getReviews(language, appId):
    url = "https://market.android.com/getreviews"

    url = "%s?id=%s&reviewType=1&rating=0&reviewSortOrder=0&pageNum=0&hl=en" % (url, appId)

    params = {
        "xhr": 1
    }

    req = urlfetch.fetch(
        url = url,
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'
        },
        payload = urllib.urlencode(params),
        method=urlfetch.POST
    ).content

    regex = re.compile('.*?("htmlContent".*)',re.DOTALL) 
    req = unicode(req, 'utf-8').encode('utf-8')
    m = regex.match(req)

    json_text='{'+m.group(1)
    data = json.loads(json_text)

    html = data['htmlContent'].replace('&nbsp;',' ').replace('&amp;','&')

    tree = lxml.html.fromstring(html)

    reviews = []

    for el in tree.findall('div'):        
        if el.find('span/strong') is not None:
            user = el.find('span/strong').text
            date = el.find('span[2]').text.strip()
        else:
            user = None            
            date = el.find('span[1]').text.strip()

        if el.find('p') is not None:
            review = el.find('p').text
        else:
            review = None
            

        date = date.replace("on ",'')
        date = datetime.strptime(date, "%B %d, %Y")

        if len(el.xpath("text()")) > 0:
            version = el.xpath("text()")[0].strip()
        else:
            version = ""
        
        if re.search(u"with", version):
            # Phone with version - Samsung Galaxy S with version 1.2.03
            m = re.search("\((.*) with version (.*)\)", version)
            version = m.group(2)
            device = m.group(1)           
        else:
            m = re.search("Version ([\d\.]*)", version)

            if m is None:
                # Phone without version - SEMC Xperia X10                
                m = re.search("\((.*)\)", version)
                version = None
                if m:
                    device = m.group(1)
                else:
                    device = None
            else:
                # Version without phone
                version = m.group(1)
                device = None
        
        title = el.find('div/h4').text        

        if device is None:
            m1 = re.search("galaxy nexus", review or "", re.I)
            m2 = re.search("galaxy nexus", title or "", re.I)

            if m1 is not None or m2 is not None:
                device = "Galaxy Nexus"
            
                
        review = {
            "user": user,
            "date": date,
            "version": version,
            "device": device,
            "title": title, 
            "rank": int(el.xpath("count(div/div/div[contains(@class,'SPRITE_star_on_dark')])")),
            "review": review
        }

        reviews.append(review)
        
    return reviews