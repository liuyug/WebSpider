#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import logging

from ..spider.utils import url_downloader


logging.basicConfig(level=logging.DEBUG)


def test():
    urls = (
        'http://www.cisco.com',
        'http://www.baidu.com',
    )
    for url in urls:
        ret = url_downloader(url)
        print('mime', ret['mime'])
        print('path', ret['path'])
        print('url', ret['url'])
        print('data', ret['data'][:1024] if ret['data'] else None)


if __name__ == '__main__':
    test()
