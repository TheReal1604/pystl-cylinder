class Point:
    def __init__(self, x, y, z, degree=0):
        self.x = x
        self.y = y
        self.z = z
        self.degree = degree

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getz(self):
        return self.z

    def getdegree(self):
        return self.degree