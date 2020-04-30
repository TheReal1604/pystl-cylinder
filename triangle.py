from point import Point


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point, fx: int, fy: int, fz: int):
        self.points = []
        self.mpoints = []
        self.facet = []
        self.points.append(p1)
        self.points.append(p2)
        self.points.append(p3)
        self.facet.append(fx)
        self.facet.append(fy)
        self.facet.append(fz)


    def getpoints(self):
        return self.points

    def tostl(self):
        return "facet normal {} {} {}\n" \
               "\touter loop\n" \
               "\t\tvertex {} {} {}\n" \
               "\t\tvertex {} {} {}\n" \
               "\t\tvertex {} {} {}\n" \
               "\tendloop\n" \
               "endfacet\n".format(self.facet[0], self.facet[1], self.facet[2],
                                   self.points[0].getx(),self.points[0].gety(), self.points[0].getz(),
                                 self.points[1].getx(), self.points[1].gety(), self.points[1].getz(),
                                 self.points[2].getx(), self.points[2].gety(), self.points[2].getz())