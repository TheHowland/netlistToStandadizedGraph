class IterLimiter:
    def __init__(self, limit: int):
        self.limit = limit
        self.iter = 0

    def reInit(self, limit = None):
        if limit is None:
            limit = self.limit
        self.iter = 0

    @property
    def limitReached(self):
        self.iter += 1
        return self.limit == self.iter
