import datetime


class PercentTracker():
    def __init__(self):
        self.amount = 0
        self.counter = 0
        self.start = datetime.datetime.now()

    def print_message(self, param=None):
        elapsed = datetime.datetime.now() - self.start
        self.counter += 1
        percentage = (float(self.counter) / float(self.amount)) * 100
        percent = round(percentage, 3)
        percent = format(percent, '.3f')
        if param:
            print(elapsed, '\t', '{} of {}\t{}%'.format(
                self.counter, self.amount, percent), '\t', param)
        else:
            print(elapsed, '\t', '{} of {}\t{}%'.format(
                self.counter, self.amount, percent))
