
from .baidu import BaiduEngine
from .bing import BingEngine
from .google import GoogleEngine


def getEngine(name):
    name = name.lower()
    if name == 'baidu':
        return BaiduEngine()
    elif name == 'bing':
        return BingEngine()
    elif name == 'google':
        return GoogleEngine()
    else:
        raise ValueError('Don\'t find engine %s' % name)
