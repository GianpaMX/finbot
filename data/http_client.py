import urllib.request
from urllib.parse import urlsplit, parse_qs
from xml.etree import cElementTree


class HttpClient(object):
    def get_from_url(self, url):
        split_url = urlsplit(url)
        qs = parse_qs(split_url.query)

        if 'u' in qs:
            actual_url = qs['u'].pop()
        else:
            actual_url = url

        req = urllib.request.Request(actual_url)
        with urllib.request.urlopen(req) as file:
            return cElementTree.fromstring(file.read())
