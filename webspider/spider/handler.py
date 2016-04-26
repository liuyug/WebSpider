
from six.moves import queue

from .queue import SeedQueue, DoneQueue, DeadQueue
from .utils import url_downloader, perror


class HandlerBase(object):
    """
    Spider Handler Base Class

    seed_queue
        waiting urls
    done_queue
        downloaded urls
    dead_queue
        dead url, don't get url content
    """
    seed_queue = None
    done_queue = None
    dead_queue = None
    is_shutdown = False
    retry = 1
    agent = None
    proxy = None
    cookie = None

    def __init__(self, agent=None, proxy=None, cookie=None, retry=None):
        self.seed_queue = SeedQueue()
        self.done_queue = DoneQueue()
        self.dead_queue = DeadQueue()
        self.retry = retry or 1
        self.agent = agent
        self.proxy = proxy
        self.cookie = cookie

    def handle(self, data, url):
        pass

    def __handle(self, item):
        url = item['url']
        data = item['data']
        get_url = '%s?%s' % (url, data) if data else url
        if get_url in self.done_queue or get_url in self.dead_queue:
            return
        ret = url_downloader(url, data=data, cookie=self.cookie,
                             retry=2,
                             agent=self.agent, proxy=self.proxy)
        if ret['error'] == 'Ok':
            self.handle(ret['data'], url)
            self.done_queue.put(get_url)
            self.cookie = ret['cookie']
        elif item['count'] < self.retry:
            new_item = {
                'url': url,
                'data': item['data'],
                'count': item['count'] + 1,
                'error': ret['error'],
            }
            self.seed_queue.put(new_item)
        else:
            perror('Failed to get %s: %s' % (url, ret['error']))
            self.dead_queue.put(get_url)

    def put(self, url, data=None):
        item = {
            'url': url,
            'data': data,
            'count': 1,
            'error': None,
        }
        self.seed_queue.put(item)

    def cleanup(self):
        pass

    def shutdown(self):
        self.is_shutdown = True

    def run_loop(self):
        while not self.is_shutdown:
            try:
                item = self.seed_queue.get(timeout=1)
                self.__handle(item)
                self.seed_queue.task_done()
            except queue.Empty:
                pass
        self.cleanup()

    def run_once(self):
        while not self.seed_queue.empty():
            item = self.seed_queue.get()
            self.__handle(item)
            self.seed_queue.task_done()
        self.cleanup()
