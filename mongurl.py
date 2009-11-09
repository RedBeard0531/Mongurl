#!/usr/bin/python
import pymongo
from bottle import *
import sys
import random
import urllib
import urlparse
from datetime import datetime
import re

db = pymongo.Connection().mongurl

db.urls.ensure_index([('visits',1), ('created',1)])

@route('/')
def index():
    urls = db.urls.find().sort([('visits',-1), ('created',-1)]).limit(100)
    return template('mainpage', urls=urls, urljoin=urlparse.urljoin)

def genid():
    chars = ('abcdefghijklmnopqrstuvwxyz'
             'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return ''.join(random.sample(chars, 5))

@route('/', method="POST")
def post_url():
    url = request.body.getvalue()
    from_browser=False
    if url.startswith('url='):
        from_browser = True
        url = urllib.unquote(url[4:])
    url = url.strip()

    if not re.match(r'^\w+://', url):
        url = 'http://' + url

    while True:
        try:
            _id = genid()
            db.urls.insert(dict(
                _id = _id,
                url = url,
                created = datetime.now(),
                visits = 0,
                last_visited = None,
            ), safe=True)
        except:
            continue
        break

    db.real_urls.insert(dict(
        _id = url,
        created = datetime.now(),
        visits = 0,
        last_visited = None,
        tags = []
    )) # will silently fail if real_url already in system

    db.real_urls.update({'_id':url},{'$push':{'shorts': _id}})

    if from_browser:
        redirect('/', 303)
    else:
        return _id

def get_url_data(id):
    url = db.urls.find_one({'_id':id})
    if not url:
        abort(404, 'Non-existant id')
    return url

@route('/:id')
def forwarder(id):
    url = get_url_data(id)
    db.urls.update({'_id':id},
        { '$inc': {'visits': 1}
        , '$set': {'last_visited': datetime.now()}
        })
    db.real_urls.update({'_id':url['url']},
        { '$inc': {'visits': 1}
        , '$set': {'last_visited': datetime.now()}
        })
    redirect(url['url'], 301)

@route('/:id/url')
def get_url(id):
    return get_url_data(id)['url']

@route('/:id/info')
def get_info(id):
    url = get_url_data(id)
    url = dict((str(k), v) for k,v in url.iteritems())
    real_url = db.real_urls.find_one({'_id':url['url']})
    return template('urlpage', real_url=real_url, urljoin=urlparse.urljoin, **url)

if __name__ == '__main__':
    do_reload = '--reload' in sys.argv
    debug(do_reload)
    run(reloader=do_reload)
