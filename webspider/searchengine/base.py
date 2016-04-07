from six.moves.urllib.parse import urlencode


class EngineBase(object):
    method = 'POST'
    name = 'base'
    url = None
    data = None

    def __init__(self):
        self.data = {}

    def __str__(self):
        return self.name

    def get_url(self):
        if self.method == 'POST':
            return self.url
        elif self.method == 'GET':
            return '%s?%s' % (self.url, urlencode(self.data))
        else:
            raise ValueError('method error: %s' % self.method)

    def get_data(self):
        if self.method == 'POST':
            return urlencode(self.data) if self.data else None
        elif self.method == 'GET':
            return None
        else:
            raise ValueError('method error: %s' % self.method)

    def set_search(self, **kwargs):
        for k, v in kwargs.item():
            self.data[k] = v
