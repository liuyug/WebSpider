import logging

from six.moves import queue

from .queue import SeedQueue, DoneQueue
from .utils import url_downloader

logger = logging.getLogger(__name__)


class HandlerBase(object):
    """
    Spider Handler Base Class

    seed_queue
        waiting urls
    done_queue
        downloaded urls
    """
    def __init__(self, agent=None, proxy=None):
        self.seed_queue = SeedQueue()
        self.done_queue = DoneQueue()
        self.is_shutdown = False
        self.agent = agent or 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130619 Firefox/17.0'
        self.proxy = proxy

    def handle(self, data):
        pass

    def __handle(self, item):
        url = item['url']
        data = item['data']
        if url in self.done_queue:
            return
        logger.debug('get url: %s, data: %s' % (url, data))
        ret = url_downloader(url, data=data,
                             agent=self.agent, proxy=self.proxy)
        if ret['error'] == 'Ok':
            self.handle(ret['data'])
            self.done_queue.put(url)
        else:
            new_item = {
                'url': url,
                'data': item['data'],
                'count': item['count'] + 1,
                'error': ret['error'],
            }
            self.seed_queue.put(new_item)

    def put(self, url, data):
        item = {
            'url': url,
            'data': data,
            'count': 0,
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
