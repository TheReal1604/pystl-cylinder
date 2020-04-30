from point import Point
from triangle import Triangle
from math import cos, sin, radians
import argparse


"""
Calculates x,y of the corresponding point
@:param r radius
@:param degree
"""


def calc_coordinates(r, degree):
    return [round((0 + (r * cos(radians(degree)))), 4), round((0 + (r * sin(radians(degree)))), 4)]


"""
Calculates all needed points and triangles for a cylinder

@:param r radius
@:param trarr array of triangles
@
"""


def calc_triangle_normal(p1: Point, p2: Point, p3: Point):
    uvec = {
        "x": p2.getx() - p1.getx(),
        "y": p2.gety() - p1.gety(),
        "z": p2.getz() - p1.getz()
    }
    vvec = {
        "x": p3.getx() - p1.getx(),
        "y": p3.gety() - p1.gety(),
        "z": p3.getz() - p1.getz()
    }

    nvec = {
        "x": uvec['y'] * vvec['z'] - uvec['z'] * vvec['y'],
        "y": uvec['z'] * vvec['x'] - uvec['x'] * vvec['z'],
        "z": uvec['x'] * vvec['y'] - uvec['y'] * vvec['x']
    }

    return nvec


def calcpoints(r, height, steps):
    degree = 0
    pamount = round(360 / steps)
    points = []
    trarr = []
    upoints = []
    tstr = ""

    # generate lower triangles (sides)
    for p in range(0, pamount):
        coords = calc_coordinates(r, degree)
        degree += steps
        points.append(Point(coords[0], coords[1], 0))

    for p in range(0, len(points)):
        if p == len(points) - 1:
            upperpoint = Point(points[p].getx(), points[p].gety(), height)
            nvec = calc_triangle_normal(points[p], points[0], upperpoint)
            trarr.append(Triangle(points[p], points[0], upperpoint, nvec['x'], nvec['y'], nvec['z']))
        else:
            upperpoint = Point(points[p].getx(), points[p].gety(), height)
            nvec = calc_triangle_normal(points[p], points[p + 1], upperpoint)
            trarr.append(Triangle(points[p], points[p + 1], upperpoint, nvec['x'], nvec['y'], nvec['z']))

    # generate upper triangles (sides)
    degree = 0

    for p in range(0, pamount):
        coords = calc_coordinates(r, degree)
        degree += steps
        upoints.append(Point(coords[0], coords[1], height))

    for p in range(0, len(upoints)):
        if p == len(upoints) - 1:
            upperpoint = Point(upoints[0].getx(), upoints[0].gety(), 0)
            nvec = calc_triangle_normal(upoints[p], upoints[0], upperpoint)
            trarr.append(Triangle(upoints[p], upoints[0], upperpoint, nvec['x'], nvec['y'], nvec['z']))
        else:
            upperpoint = Point(upoints[p + 1].getx(), upoints[p + 1].gety(), 0)
            nvec = calc_triangle_normal(upoints[p], upoints[p + 1], upperpoint)
            trarr.append(Triangle(upoints[p], upoints[p + 1], upperpoint, nvec['x'], nvec['y'], nvec['z']))

    # generate top and bottom "plates"
    for i in range(0, 2):
        if i == 0:
            curp = points
            localheight = 0
        else:
            curp = upoints
            localheight = height

        for p in range(1, round(len(curp)/2)):
            mirrorp = Point(curp[p].getx(), curp[p].gety() * -1, localheight)
            nextp = curp[p + 1]
            nvec = calc_triangle_normal(curp[p], nextp, mirrorp)
            trarr.append(Triangle(curp[p], nextp, mirrorp, nvec['x'], nvec['y'], nvec['z']))

        for p in range(round(len(curp) / 2) + 1, round(len(curp))):
            if p == len(curp) - 1:
                mirrorp = Point(curp[p].getx(), curp[p].gety() * -1, localheight)
                nextp = curp[0]
                nvec = calc_triangle_normal(curp[p], nextp, mirrorp)
                trarr.append(Triangle(curp[p], nextp, mirrorp, nvec['x'], nvec['y'], nvec['z']))
            else:
                mirrorp = Point(curp[p].getx(), curp[p].gety() * -1, localheight)
                nextp = curp[p + 1]
                nvec = calc_triangle_normal(curp[p], nextp, mirrorp)
                trarr.append(Triangle(curp[p], nextp, mirrorp, nvec['x'], nvec['y'], nvec['z']))

    for t in trarr:
        tstr += t.tostl()

    print("Processed {} triangles, {} points.".format(len(trarr), len(upoints) + len(points)))

    return tstr


def qualitytodeg(ql):
    mapper = {
        "ultrahigh": 1,
        "high": 10,
        "mid": 30,
        "low": 60,
        "cube": 90,
    }

    if ql in mapper:
        return mapper.get(ql)
    else:
        return 30


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-r', '--radius', required=True)
    argparser.add_argument('-q', '--quality', required=False, help="A parameter to switch between qualitys. "
                                                                   "(aka how much points are generated)"
                                                                   " OPTIONS: ultrahigh, high, mid, low, cube")
    argparser.add_argument('-he', '--height', required=False)

    args = argparser.parse_args()

    f = open("demo.stl", "w")
    f.write("solid demo\n")
    f.write(calcpoints(int(args.radius), int(args.height), qualitytodeg(args.quality)))
    f.write("endsolid demo")
    f.close()

