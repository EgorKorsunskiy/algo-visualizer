class Environment:
    def __init__(self, store={}, outer=None) -> None:
        self.store = {}
        self.outer = outer

    def find_store(self, key):
        store = self.store
        outer = self.outer
        while key not in store and outer != None:
            store = outer.store
            outer = outer.outer
        if key not in store:
            return None
        return store

    def get(self, key):
        store = self.find_store(key)
        if store is None:
            return None
        return store[key]

    def set(self, key, value, recursive=False):
        if recursive and self.find_store(key):
            self.find_store(key)[key] = value
        else:
            self.store[key] = value
