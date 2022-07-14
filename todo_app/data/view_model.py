class ViewModel:

    def __init__(self, items, list_targets):
        self._items = items
        self._list_targets = list_targets

    @property
    def items(self):
        return self._items

    @property
    def list_targets(self):
        return self._list_targets
