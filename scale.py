class Scale:
    def __init__(self, values=None):
        if values:
            self.values = values
        else:
            self.values = ['okay', 'good', 'great', 'awesome']

    def score(self, value):
        return self.values.index(value) / (len(self.values) - 1)
