import random

class Point:
    def __init__(self, id, x, y, z, position) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.position = position
        

class PairPoint:
    def __init__(self, left : Point, right: Point, idx = 10000) -> None:
        self.left = left
        self.right = right
        self.idx = idx
        
    def get_mid_point(self):
        _x_mid = (self.left.x + self.right.x) // 2
        _y_mid = (self.left.y + self.right.y) // 2
        _z_mid = (self.left.z + self.right.z) // 2
        self.idx += 1
        return Point(self.idx, _x_mid, _y_mid, _z_mid, -1)
    
class Way:
    def __init__(self, id) -> None:
        self.id = id
        # Way are list of nodes
        self.points = []
    
    def _addPoint(self, point):
        self.points.append(point)
    
class LaneLet:
    def __init__(self, id) -> None:
        self.id = id
        # Lanelet are list of Way
        self.ways = []
    
    def _addWay(self, way):
        self.ways.append(way)

class Map:
    def __init__(self) -> None:
        self.map = []
    
    def _addLaneLet(self, lanelet : LaneLet):
        self.map.append(lanelet)
        