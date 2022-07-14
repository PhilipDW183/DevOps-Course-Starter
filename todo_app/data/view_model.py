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
    def to_do_items(self):
        to_do_items_id = self.list_targets.get("To Do")
        to_do_items = self.filter_items(self.items, to_do_items_id)
        return to_do_items

    @property
    def doing_items(self):
        doing_items_id = self.list_targets.get("Doing")
        doing_items = self.filter_items(self.items, doing_items_id)
        return doing_items

    @property
    def done_items(self):
        done_items_id = self.list_targets.get("Done")
        done_items = self.filter_items(self.items, done_items_id)
        return done_items

    def filter_items(self, items, id):
        return [item for item in items if item.idList == id]
