import matplotlib.pyplot as plt

# Point class with x, y as point
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# To find the left most point 
def left_index(points):
    left = 0
    for i in range(1, len(points)):
        if points[i].x < points[left].x:
            left = i
        elif points[i].x == points[left].x:
            if points[i].y > points[left].y:
                left = i
    return left

# To index the point in dataset
def index(point, points):
    idx = 0
    for i in range(1, len(points)):
        if points[i].x == point.x and points[i].y == point.y:
                idx = i
    return idx

# To sort data points
def sort(points):
    for i in range(0, len(points)):
        for j in range(i+1,len(points)):
            if points[j].x < points[i].x:
                tam = points[j]
                points[j] = points[i]
                points[i] = tam
    return points

# To devide data points to two partitions
def devide(points):
    pts1 = []
    pts2 = []
    if len(points) % 2 == 0:
        for i in range(0, int(len(points)/2)):
            pts1.append(points[i])
            pts2.append(points[int(len(points)/2)+i])
    if len(points) % 2 == 1:
        for i in range(0, int(len(points)/2)):
            pts1.append(points[i])
            pts2.append(points[int(len(points)/2)-1+i])
        pts2.append(points[-1])
    return pts1, pts2

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

# To find convex hull of points
def convex_hull(points, n):
    '''
    There must be at least 3 points.
    '''
    if n < 3:
        return 

    '''
    Finding the leftmost point.
    '''
    l = left_index(points)
    
    '''
    Start from leftmost point, keep moving counterclockwise until reach the start point again.
    '''
    hull = []
    p = l
    q = 0

    while (True):
        hull.append(p)

        ''' 
        Search for a point 'q' such that orientation(p, x, q) is counterclockwise for all points 'x'.
        The idea is to keep track of last visited most counterclockwise point in q.
        If any point 'i' is more counterclockwise than q, then update q.
        '''
        q = (p + 1) % n
        for i in range(n):
            # If i is more counterclockwise than current q, then update q  
            if (orientation(points[p], points[i], points[q]) == 1):
                q = i

        ''' 
        If q is the most counterclockwise with respect to p, set p as q for next iteration, so that q is added to result 'hull'.
        '''
        p = q
        
        '''
        While we don't come to first point.
        '''
        if p == l:
            break

    '''
    Print result
    '''
    return hull

# To merge two convex hulls
def convex_hull_mh(points):
    '''
    Sort and devide dataset
    '''
    sort(points)
    data1, data2 = devide(points)

    '''
    Create subhull.
    '''
    cvxhull1 = convex_hull(data1, len(data1))
    cvxhull2 = convex_hull(data2, len(data2))

    hull1 = []
    for i in cvxhull1:
        hull1.append(data1[i])
    hull2 = []
    for i in cvxhull2:
        hull2.append(data2[i])

    '''
    Get the rightmost point of left convex hull.
    '''
    p = max(hull1, key = lambda point: point.x)

    '''
    Get the leftmost poitn of right convex hull.
    '''
    q = min(hull2, key = lambda point: point.x)

    '''
    Make copies of p and q.
    '''
    cp_p = p
    cp_q = q

    '''
    Raise the bridge pq to the uper tangent.
    '''
    prev_p = None
    prev_q = None
    while (True):
        prev_p = p
        prev_q = q
        if index(q, hull2)-1:
            # move p clockwise as long as it makes left turn
            while orientation(p, hull2[index(q, hull2)-1], q) == -1:
                q = hull2[index(q, hull2)-1]
        if index(p, hull1)+1:
            # move p as long as it makes right turn
            while orientation(q, hull1[index(p, hull1)+1], p) == 1:
                p = hull1[index(p, hull1)+1]

        if p == prev_p and q == prev_q:
            break
    
    '''
    Lower the bridge cp_p cp_q to the lower tangent
    '''
    prev_p = None
    prev_q = None
    while (True):
        prev_p = cp_p
        prev_q = cp_q
        if index(cp_q, hull2)+1:
            # move q as long as it makes right turn
            while orientation(cp_p, hull2[index(cp_q, hull2)+1], cp_q) == 1:
                cp_q = hull2[index(cp_q, hull2)+1]
        if index(cp_p, hull1)-1:
            # move p as long as it makes left turn
            while orientation(cp_q, hull1[index(cp_p, hull1)-1], cp_p) == -1:
                cp_p = hull1[index(cp_p, hull1)-1]
        if cp_p == prev_p and cp_q == prev_q:
            break
    m0 = index(cp_p, hull1)
    n0 = index(cp_q, hull2)
    n1 = index(q, hull2)
    m1 = index(p, hull1)

    '''
    Final result.
    '''
    result = []
    for i in range(0,m0+1):
        result.append(hull1[i])
    for i in range(n0,n1+1):
        result.append(hull2[i])
    for i in range(m1,len(hull1)):
        result.append(hull1[i])
    return result

# To display points and their convex hull
def display_pts(points):
    x = [points[p].x for p in range(len(points))]
    y = [points[p].y for p in range(len(points))]
    plt.plot(x, y, marker = "o", linestyle = "None", color = "black")

def display_mh(points, hull):
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
    plt.title("Convex Hull of {} random points by Merge Hull Algorithm".format(len(points)))

    '''
    Display points and their convex hull
    '''
    plt.axis("off")
    plt.show()



