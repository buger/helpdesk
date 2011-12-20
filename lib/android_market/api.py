import urllib
from google.appengine.api import urlfetch

import json

import lxml
import lxml.html
from lxml import etree as ElementTree
from codecs import getdecoder, getencoder, getwriter, getreader 

import re
from StringIO import StringIO


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
        review = {
            "user": el.find('span/strong').text,
            "date": el.find('span[2]').text.strip(),
            "version": el.xpath("text()")[0] or "",
            "title": el.find('div/h4').text, 
            "rank": el.xpath("count(div/div/div[contains(@class,'SPRITE_star_on_dark')])"),
        }

        reviews.append(review)
        
    return reviews

"""
    <div class="doc-review"><span class="doc-review-author"><strong>Anthony</strong></span><span class="doc-review-date"> on December 20, 2011</span> (LG Optimus One with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=01960237110398242444"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 5.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div></div><h4 class="review-title">Birdz</h4></div><p class="review-text">Awsome</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>k_ayaz002</strong></span><span class="doc-review-date"> on December 20, 2011</span> (Samsung Galaxy Fit with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=13129576951772416049"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 3.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div></div><h4 class="review-title">How to download????</h4></div><p class="review-text">How to download all this games as im new to android market</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>Peter</strong></span><span class="doc-review-date"> on December 20, 2011</span> (Samsung Galaxy S with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=13767819655925452787"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 5.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div></div><h4 class="review-title">Owesome</h4></div><p class="review-text">Like it</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>Pete</strong></span><span class="doc-review-date"> on December 20, 2011</span> (Motorola Droid X with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=13298040263685121283"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 4.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div></div><h4 class="review-title">Angry birds</h4></div><p class="review-text">Great game</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>Sinisa</strong></span><span class="doc-review-date"> on December 20, 2011</span> (HTC Wildfire S with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=16391239221804477291"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 5.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div></div><h4 class="review-title">Question</h4></div><p class="review-text">When`s the Mighty Eagle update coming ?</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>Bharat</strong></span><span class="doc-review-date"> on December 20, 2011</span> (HTC Wildfire with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=06241959480341818530"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 5.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div></div><h4 class="review-title">Addictive</h4></div><p class="review-text">Despite being a little slow on HTC Wildfire, this game&#39;s a lot of fun.</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>S.M.SOHEL REZA</strong></span><span class="doc-review-date"> on December 20, 2011</span> (Samsung Galaxy Mini with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=05299157343653209790"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 1.0 stars (Below average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div></div><h4 class="review-title">Bad</h4></div><p class="review-text">Bad update, not working</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>javadude</strong></span><span class="doc-review-date"> on December 20, 2011</span> (HTC Nexus One with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=03400451285610404001"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 4.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div></div><h4 class="review-title">Overhyped now</h4></div><p class="review-text">Getting tired of seeing AB on  shirts cups mugs walls airports ...</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>Tyler</strong></span><span class="doc-review-date"> on December 20, 2011</span> (HTC myTouch 3G Slide with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=10397671735960004485"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 3.0 stars (Above average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div></div><h4 class="review-title">Ugh</h4></div><p class="review-text">Where are the &quot;unlocked&quot; levels? The &quot;what&#39;s new&quot; section of the update lies.</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr><div class="doc-review"><span class="doc-review-author"><strong>Michael</strong></span><span class="doc-review-date"> on December 20, 2011</span> (Samsung Galaxy S with version 2.0.0)<span><a href="/details?id=com.rovio.angrybirds&reviewId=12685774967753026627"><div class="goog-inline-block review-permalink" title="Link to this review"></div></a></span><div class="doc-review-ratings-line"><div class="ratings goog-inline-block" title="Rating: 2.0 stars (Below average)"><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_on_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div><div class="goog-inline-block star SPRITE_star_off_dark"></div></div><h4 class="review-title">Used to be fun...</h4></div><p class="review-text">Was a great game, after the update it runs half as fast and freezes all the time. Just like the Angry Birds Seasons. Uninstalled... Please fix!!!!!!!</p><div class="review-footer goog-inline-block"><div class="doc-review-label"> </div><div class="per-review-controls goog-inline-block"></div></div></div><hr>
"""