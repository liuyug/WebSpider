
from .baidu import BaiduEngine
from .bing import BingEngine
from .google import GoogleEngine


def getEngine(name, **kwargs):
    name = name.lower()
    if name == 'baidu':
        return BaiduEngine(**kwargs)
    elif name == 'bing':
        return BingEngine(**kwargs)
    elif name == 'google':
        return GoogleEngine(**kwargs)
    else:
        raise ValueError('Don\'t find engine %s' % name)
