from point import Point
from triangle import Triangle
from math import cos, sin, radians
import argparse


"""
Calculates x,y of the corresponding point of the outer circles

@:param r radius
@:param degree
"""


def calc_coordinates(r, degree):
    return [round((0 + (r * cos(radians(degree)))), 4), round((0 + (r * sin(radians(degree)))), 4)]


"""
Calculates the stl "facet normal" of a given triangle (cross product)

@:param p1 Point 1 of the triangle
@:param p2 Point 2 of the triangle
@:param p3 Point 3 of the triangle
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
        "x": (uvec['y'] * vvec['z']) - (uvec['z'] * vvec['y']),
        "y": (uvec['z'] * vvec['x']) - (uvec['x'] * vvec['z']),
        "z": (uvec['x'] * vvec['y']) - (uvec['y'] * vvec['x'])
    }

    return nvec


"""
Calculates all needed points and triangles for a cylinder

@:param r radius
@:param trarr array of triangles
@
"""


def calcpoints(r, ru, height, steps):
    degree = 0
    pamount = round(360 / steps)
    points = []
    trarr = []
    upoints = []
    tstr = ""

    # generate lower triangles (sides)
    for p in range(0, pamount):
        coords = calc_coordinates(r, degree)
        points.append(Point(coords[0], coords[1], 0, degree))
        degree += steps

    for p in range(0, len(points)):
        #upperpoint = Point(points[p].getx(), points[p].gety(), height)
        coordupper = calc_coordinates(ru, points[p].getdegree())
        upperpoint = Point(coordupper[0], coordupper[1], height)

        if p == len(points) - 1:
            appendtriangle(trarr, points[p], points[0], upperpoint, True)
        else:
            appendtriangle(trarr, points[p], points[p + 1], upperpoint, True)

    # generate upper triangles (sides)
    degree = 0

    for p in range(0, pamount):
        coords = calc_coordinates(ru, degree)
        upoints.append(Point(coords[0], coords[1], height, degree))
        degree += steps

    for p in range(0, len(upoints)):
        if p == len(upoints) - 1:
            coordupper = calc_coordinates(r, upoints[0].getdegree())
            upperpoint = Point(coordupper[0], coordupper[1], 0)
            appendtriangle(trarr, upoints[p], upoints[0], upperpoint, False)
        else:
            coordupper = calc_coordinates(r, upoints[p + 1].getdegree())
            upperpoint = Point(coordupper[0], coordupper[1], 0)
            appendtriangle(trarr, upoints[p], upoints[p + 1], upperpoint, False)

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
            appendtriangle(trarr, curp[p], nextp, mirrorp, bool(i))

        for p in range(round(len(curp) / 2) + 1, round(len(curp))):
            mirrorp = Point(curp[p].getx(), curp[p].gety() * -1, localheight)
            if p == len(curp) - 1:
                nextp = curp[0]
            else:
                nextp = curp[p + 1]
            appendtriangle(trarr, curp[p], nextp, mirrorp, bool(i))

    for t in trarr:
        tstr += t.tostl()

    print("Processed {} triangles, {} points.".format(len(trarr), len(upoints) + len(points)))

    return tstr


def appendtriangle(trcontainer, p1, p2, p3, ccw: bool):
    if ccw:
        nvec = calc_triangle_normal(p1, p2, p3)
        trcontainer.append(Triangle(p1, p2, p3, nvec['x'], nvec['y'], nvec['z']))
    else:
        nvec = calc_triangle_normal(p3, p2, p1)
        trcontainer.append(Triangle(p3, p2, p1, nvec['x'], nvec['y'], nvec['z']))


"""
Maps a string to a distance in degree between the outer points of the cylinder
=> Lower distance = more points generated

@:param ql String which represents choosen quality of the stl file
@:return int which represents the distance between outer points of the cylinder sides
"""


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
    argparser.add_argument('-rl', '--lower-radius', required=True)
    argparser.add_argument('-ru', '--upper-radius', required=True)
    argparser.add_argument('-q', '--quality', required=False, help="A parameter to switch between qualitys. "
                                                                   "(aka how much points are generated)"
                                                                   " OPTIONS: ultrahigh, high, mid, low, cube")
    argparser.add_argument('-he', '--height', required=False)
    argparser.add_argument('-aq', '--all-qualities', required=False, help="generate multiple stl files - "
                                                                          "a sample from each quality setting",
                           action="store_true")

    args = argparser.parse_args()

    if args.all_qualities:
        print("All qualities requested, processing cylinders.")
        for q in ["ultrahigh", "high", "mid", "low", "cube"]:
            print("Processing {} quality setting.".format(q))
            f = open("{}.stl".format(q), "w")
            f.write("solid {}\n".format(q))
            f.write(calcpoints(int(args.lower_radius), int(args.upper_radius), int(args.height), qualitytodeg(q)))
            f.write("endsolid {}".format(q))
            f.close()
    else:
        f = open("demo.stl", "w")
        f.write("solid demo\n")
        f.write(calcpoints(int(args.lower_radius), int(args.upper_radius), int(args.height), qualitytodeg(args.quality)))
        f.write("endsolid demo")
        f.close()

