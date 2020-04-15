import matplotlib.pyplot as plt
import random

# Point class with x, y as point
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# To find the most left point
def left(points):
    left = point(0,0)
    for i in range(1, len(points)):
        if points[i].x < left.x:
            left = points[i]
        elif points[i].x == left.x:
            if points[i].y > left.y:
                left = points[i]
    return left

# To find the most right most point
def right(points):
    right = point(0,0)
    for i in range(1, len(points)):
        if points[i].x > right.x:
            right = points[i]
        elif points[i].x == right.x:
            if points[i].y > right.y:
                right = points[i]
    return right

# To return the distance from point to the line.
def distance(start, end, point):
    area = abs((start.x - point.x) * (end.y - point.y) - (end.x - point.x) * (start.y - point.y))
    dist = ((start.x - end.x) ** 2 + (start.x - end.x) ** 2) ** 0.5
    distance = area / dist
    return distance

# To find the farthest point from line
def maxpt_from_line(start, end, points):
    max_dist = 0
    max_pt = point(0,0)
    for pt in points:
        if pt != start and pt != end:
            dist = distance(start, end, pt)
            if dist > max_dist:
                max_dist = dist
                max_pt = pt
    return max_pt

# To find orientation of ordered triplet (p, q, r):
# - 1 --> Clockwise
# 0 --> p, q and r are colinear
# 1 --> Counterclockwise
def orientation(start, origin, end):
    value = (start.x - origin.x) * (end.y - origin.y) - (end.x - origin.x) * (start.y - origin.y)
    if value == 0:
        return 0
    elif value > 0:
        return - 1
    else:
        return 1

# To find the points on the left side of the line
def left_side_line(start, end, points):
    lsl = []
    for pt in points:
        if orientation(start, pt, end) == 1:
            lsl.append(pt)
    return lsl

# To find the subhull of the points
def sub_hull(mi, ma, points):
    left_pts = left_side_line(mi, ma, points)
    mpt = maxpt_from_line(mi, ma, left_pts)
    if len(left_pts) < 1:
        return [ma]
    subhull = sub_hull(mi, mpt, left_pts)
    subhull.extend(sub_hull(mpt, ma, left_pts))
    return subhull

def convex_hull_qh(points, n):
    plt.figure()
    plt.axis("off")
    #plt.title("Convex Hull of {} random points by QuickHull Algorithm".format(len(points)))
    display_pts(points)
    plt.show()
    '''
    There must be at least 3 points.
    '''
    if n < 3:
        return 

    '''
    Finding the leftmost and rightmost point.
    '''
    le = left(points)
    ri = right(points)
    plt.axis("off")
    #plt.title("Convex Hull of {} random points by QuickHull Algorithm".format(len(points)))
    display_pts(points)
    display_ln(le, ri, st = ":", cl = "blue")
    plt.show()
    '''
    Build the convex hull.
    '''
    display_ln(le, ri, st = ":", cl = "blue")
    
    hull = sub_hull(le, ri, points)
    display_hull(points, hull, "red")
    display_ln(le, hull[0], st = "-.", cl = "red")

    hu_ll = sub_hull(ri, le, points)
    display_hull(points, hu_ll, "green")
    display_ln(ri, hu_ll[0], st = "-.", cl = "green")

    hull.extend(hu_ll)
    plt.show()

    '''
    Print result
    '''    
    return hull

# To display points and their convex hull
def display_ln(m, n, st, cl):
    plt.plot([m.x,n.x], [m.y,n.y], linestyle = st, color = cl)

def display_pts(points):
    x = [points[p].x for p in range(len(points))]
    y = [points[p].y for p in range(len(points))]
    plt.plot(x, y, marker = "o", linestyle = "None", color = "black")

def display_hull(points, hull, cl):
    x = [points[p].x for p in range(len(points))]
    y = [points[p].y for p in range(len(points))]
    plt.plot(x, y, marker = "o", linestyle ="None", color = "black")
    ch_x = [p.x for p in hull]
    ch_y = [p.y for p in hull]
    plt.plot(ch_x, ch_y, linestyle = "-.", color = cl)
    plt.axis("off")

def display_qh(points, hull):
    '''
    All points
    '''
    x = [points[p].x for p in range(len(points))]
    y = [points[p].y for p in range(len(points))]
    plt.plot(x, y, marker = "o", linestyle = "None", color = "black")
    
    '''
    Convex hull
    '''
    ch_x = [p.x for p in hull]
    ch_x.append(ch_x[0])
    ch_y = [p.y for p in hull]
    ch_y.append(ch_y[0])
    plt.plot(ch_x, ch_y, color = "brown")
    #plt.title("Convex Hull of {} random points by QuickHull Algorithm".format(len(points)))

    '''
    Display points and their convex hull
    '''
    plt.axis("off")
    plt.show()