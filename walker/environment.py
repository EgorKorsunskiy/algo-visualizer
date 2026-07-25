class Environment:
    def __init__(self, store={}, outer=None) -> None:
        self.store = {}
        self.outer = outer

    def get(self, key):
        store = self.store
        outer = self.outer
        while key not in store and outer != None:
            store = outer.store
            outer = outer.outer
        if key not in store:
            return None
        return store[key]

    def set(self, key, value):
        self.store[key] = value
