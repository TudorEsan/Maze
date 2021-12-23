class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        if self.f == other.f:
            if self.h <= other.f:
                return True
            else: return False
        elif self.f < other.f:
            return True
        return False

    def __hash__(self):
        return hash((self.parent, self.position, self.g, self.h, self.f))

    def __sub__(self, other):
        return (other.position[0] - self.position[0], other.position[1] - self.position[1])