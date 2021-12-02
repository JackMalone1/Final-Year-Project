

class DummyNode:
    def __init__(self):
        self.parent = None


class Node:
    def __init__(self, position, fmove=None, parent=None):
        if parent is None:
            parent = DummyNode()
