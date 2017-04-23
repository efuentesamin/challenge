

class Category:

    def __init__(self, id, name, level, parent, best_offer, expired, leaf):
        self.id = id
        self.name = name
        self.level = level
        self.parent = parent
        self.best_offer = best_offer
        self.expired = expired
        self.leaf = leaf
        self.children = []

    def __str__(self):
        return '{} {}'.format('-***' * self.level, self.name)
