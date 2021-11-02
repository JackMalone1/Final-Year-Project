class dummy_node():
    def __init__(self):
        self.parent = None

class node():
    def __init__(self, position, fmove=None, parent=None):
        if parent is None:
            parent = dummy_node()
