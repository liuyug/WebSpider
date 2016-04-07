
import time
import re
import gzip
import logging
import socket

from six.moves.urllib.error import URLError
from six.moves.urllib.request import Request, urlopen, build_opener

import socks
from sockshandler import SocksiPyHandler

logger = logging.getLogger(__name__)


def html_chardet(text):
    """ return html charset """
    text_ascii = text[:1024].decode('ascii', 'ignore')
    # search meta tag
    html5_charset_pattern = '''<meta[ ]+charset=["']?([-a-zA-Z0-9]+)["']?'''
    charset_pattern = '''<meta[ ]+http-equiv=["']?content-type["' ]+content=["']?text/html;[ ]*charset=([-a-zA-Z0-9]+)["']?'''
    charset_search = re.compile(charset_pattern, re.IGNORECASE)
    charset_match = charset_search.search(text_ascii)
    if charset_match:
        return charset_match.group(1)
    html5_charset_search = re.compile(html5_charset_pattern, re.IGNORECASE)
    html5_charset_match = html5_charset_search.search(text_ascii)
    if html5_charset_match:
        return html5_charset_match.group(1)
    # hard decode test
    text_1024 = text[:1024]
    for x in ['utf-8', 'gbk', 'cp1252', 'iso-8859-1']:
        try:
            text_1024.decode(x)
            return x
        except:
            pass
    return None


def url_downloader(url, data=None, path=None,
                   timeout=10, retry=3, retry_ivl=5, agent=None, proxy=None):
    """Download URL link
    url:    url to download
    data:   post data
    path:   download to local file
    timeout:    socket timeout
    retry:  retry times to download url
    retry_ivl:  interval time when retry
    agent:  http user agent
    proxy:  socks5://127.0.0.1:1080
    """
    if not agent:
        agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130619 Firefox/17.0'
    while True:
        try:
            request = Request(url, data=data)
            request.add_header('User-Agent', agent)
            response = None
            if proxy:
                scheme, host, port = proxy.split(':')
                host = host.strip('/')
                opener = build_opener(SocksiPyHandler(
                    socks.PROXY_TYPES[scheme.upper()], host, int(port)
                ))
                response = opener.open(request, timeout=timeout)
            else:
                response = urlopen(request, timeout=timeout)
            content_encoding = response.info().get('content-encoding')
            if content_encoding:
                logger.info('Find content-encoding: %s', content_encoding)
                r_data = gzip.decompress(response.read())
            else:
                r_data = response.read()
            if path:
                with open(path, 'wb') as f:
                    f.write(r_data)
                r_data = None
            response.close()
            mime = response.info().get('content-type')
            real_url = response.geturl()
            err = 'Ok'
            break
        except (URLError, socket.error) as err:
            response and response.close()
            retry -= 1
            if retry > 0:
                logger.warn('Wait %d seconds to retry... (%d): %s' % (retry_ivl, retry, err))
                time.sleep(retry_ivl)
                retry_ivl += retry_ivl
                timeout += timeout
            else:
                logger.error('%s - %s' % (err, url))
                mime = r_data = real_url = None
                break
    return {'mime': mime, 'path': path, 'data': r_data, 'url': real_url, 'error': err}
