from scale import Scale
from mylibrary import OrderedSet


class Choice:
    def __init__(self, text, scale):
        self.text = text
        self.value = None
        self.included = True
        self.comparisons = {}
        self.scale = scale

    def __gt__(self, other):
        try:
            if not self.score() == other.score():
                return self.score() > other.score()
        except ValueError:
            pass

        try:
            return self.comparisons[other]
        except KeyError:
            self.comparisons[other] = self.manual_compare(other)
            return self.comparisons[other]

    def __lt__(self, other):
        return not self.__gt__(other)

    def __hash__(self):
        return hash(self.text)

    def manual_compare(self, other):
        raise NotImplementedError

    def score(self):
        return self.scale.score(self.value)

    def __str__(self):
        return self.text


class ChoiceList(OrderedSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = 0
        self.scale = Scale()

    def include(self, item):
        self[item].included = True
        self.size += 1

    def exclude(self, item):
        self[item].included = False
        self.size -= 1

    def best(self):
        return max(i for i in self if i.included)

    def next_best(self):
        self.best().included = False
        return self.best()

    def add(self, key):
        super().add(key)
        self.size += 1

    def __len__(self):
        return self.size

    def __contains__(self, item):
        try:
            return self[item].included
        except KeyError:
            return False

    def discard(self, key):
        super().discard(key)
        self.size -= 1

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def excluded(self):
        end = self.end
        curr = end[2]
        list_ = []
        while curr is not end:
            if not curr[0].included:
                list_.append(curr[0])
            curr = curr[2]
        return list_


class DecisionMaker:
    def __init__(self):
        self.lists = {}
