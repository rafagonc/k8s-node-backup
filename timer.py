import datetime


class Timer:
    def __enter__(self):
        self.start = datetime.datetime.now()
        return self

    def __exit__(self, a, b, c):
        pass

    def end_timer(self, *args):
        self.end = datetime.datetime.now()
        self.interval = (self.end - self.start).total_seconds()