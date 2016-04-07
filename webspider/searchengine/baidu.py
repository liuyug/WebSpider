
from .base import EngineBase


class BaiduEngine(EngineBase):
    def __init__(self):
        super(BaiduEngine, self).__init__()
        self.method = 'GET'
        self.name = 'baidu'
        self.url = 'http://www.baidu.com/s'
        self.num_per_page = 10

    def set_search(self, search=None, page=0):
        self.data['wd'] = search
        self.data['pn'] = page * self.num_per_page
