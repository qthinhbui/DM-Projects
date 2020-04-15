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
def convex_hull_ja(points, n):
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

# To display points and their convex hull
def display_ja(points, hull):
    '''
    All points
    '''
    x = [points[p].x for p in range(len(points))]
    y = [points[p].y for p in range(len(points))]
    plt.plot(x, y, marker = "o", linestyle = "None", color = "black")
    
    '''
    Convex hull
    '''
    ch_x = [points[p].x for p in hull]
    ch_x.append(ch_x[0])
    ch_y = [points[p].y for p in hull]
    ch_y.append(ch_y[0])
    plt.plot(ch_x, ch_y, color = "brown")
    plt.title("Convex Hull of {} random points by Jarvis Algorithm".format(len(points)))

    '''
    Display points and their convex hull
    '''
    plt.axis("off")
    plt.show()