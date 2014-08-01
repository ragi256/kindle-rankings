#!/usr/bin/ python
# coding: utf-8

import sys
import os
sys.path.append('/home/usrs/sd12425/usr/py-lib')
from BeautifulSoup import BeautifulStoneSoup
from urllib2 import URLError, HTTPError
from pyzon import Pyzon

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
ID = os.getenv("ID")
if ACCESS_KEY is None:
    import secret
    ACCESS_KEY = secret.ACCESS_KEY
    SECRET_ACCESS_KEY = secret.SECRET_ACCESS_KEY
    ID = secret.ID

pyzon = Pyzon(ACCESS_KEY, SECRET_ACCESS_KEY, ID)
pyzon.setLocale('JP')

KINDLE_COMIC_NODE = '2293143051'
KINDLE_NODES = {'少年コミック': '2430812051', '青年コミック': '2430869051',
                '少女コミック': '2430765051', '女性コミック': '2430737051',
                '4コマまんが': '2430727051'}

# books_comicにchildrenはない
BOOKS_COMIC_NODE = '2278488051'

# kindleではMostGiftedはない
RESPONSE_GROUP_LIST = [
    "MostGifted", "NewReleases", "MostWishedFor", "TopSellers"]


def getXML(function, *args, **kwargs):
    while True:
        try:
            xml = function(*args, **kwargs)
        except (HTTPError, URLError):
            #        except (HTTPError, URLError),e:
            #            print 'Error', e
            continue
        break
    return xml


def getRanking():
    rankings = []
    for i in range(1, 4):
        ranking = []
        RESPONSE_GROUP = RESPONSE_GROUP_LIST[i]

        xml = getXML(
            pyzon.BrowseNodeLookup, KINDLE_COMIC_NODE, ResponseGroup=RESPONSE_GROUP)
        soup = BeautifulStoneSoup(xml)

        items = soup.find('topitemset')
        items = items.findAll('topitem')
        print '=' * 20, RESPONSE_GROUP, '=' * 20
        if items is None:
            continue

        for item in items:
            element = [None, None, None]
            ASIN = item.asin.string
            element[0], element[1] = item.title.string, item.author.string
            xml = getXML(pyzon.ItemLookup, ASIN, ResponseGroup='Images')
            soup = BeautifulStoneSoup(xml)
            images = soup.find('imageset')
            for image in images.contents:
                if image.name == 'largeimage':
                    element[2] = image.url.string
            ranking.append(element)
#        rankings[RESPONSE_GROUP] = ranking
        rankings.append(ranking)
 #       print ranking[0]
    return rankings

if __name__ == '__main__':
    import pickle
    output = open('rankings.txt', 'w')
    rankings = getRanking()
    pickle.dump(rankings, output)
    output.close()


#=========================================================================
