from six.moves.queue import Queue


class SeedQueue(Queue):
    pass


class DoneQueue(list):
    def put(self, item):
        self.append(item)


class DeadQueue(list):
    def put(self, item):
        self.append(item)
