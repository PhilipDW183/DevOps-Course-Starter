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

    @property
    def doing_items(self):
        doing_items_id = self.list_targets.get("Doing")
        doing_items = [item for item in self.items if item.idList == doing_items_id]
        return doing_items

    @property
    def to_do_items(self):
        to_do_items_id = self.list_targets.get("To Do")
        to_do_items = [item for item in self.items if item.idList == to_do_items_id]
        return to_do_items
