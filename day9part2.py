# optimized_solution.py
# Usage: put your data.txt (one "x,y" per line) next to this script and run it.

from bisect import bisect_left, bisect_right

def parse_points(text):
    pts = [tuple(map(int, line.split(',')))
           for line in text.strip().splitlines() if line.strip()]
    return pts

def build_edges(pts):
    # ordered polygon edges (wrap-around)
    edges = []
    n = len(pts)
    for i in range(n):
        x1,y1 = pts[i]
        x2,y2 = pts[(i+1)%n]
        edges.append((x1,y1,x2,y2))
    return edges

def intervals_at_sample_x(edges, sample_x):
    """
    Intersect the vertical line x = sample_x with the polygon.
    Return a list of inclusive intervals [(y0,y1), (y2,y3), ...]
    where each pair (y_k, y_{k+1}) comes from sorted horizontal-edge y-values.
    We treat these as inclusive bounds (points on boundary count).
    """
    ys = []
    for x1,y1,x2,y2 in edges:
        # only horizontal edges produce intersections with x=sample_x
        if y1 == y2:
            xa, xb = (x1, x2) if x1 <= x2 else (x2, x1)
            # sample_x is fractional (x + 0.5); strict inequality is safe
            if xa < sample_x < xb:
                ys.append(y1)
    ys.sort()
    # pair up successive intersections -> interior intervals
    intervals = []
    if len(ys) % 2 != 0:
        # polygon should provide even number of intersections for a vertical line
        # but guard defensively
        raise RuntimeError("odd number of intersections at x={}".format(sample_x))
    for k in range(0, len(ys), 2):
        a = ys[k]
        b = ys[k+1]
        # keep as inclusive interval [a, b]
        intervals.append((a, b))
    return intervals

def merge_intervals(segs):
    # helper: merge overlapping inclusive intervals (if needed)
    if not segs:
        return []
    segs = sorted(segs)
    out = []
    cur_a, cur_b = segs[0]
    for a,b in segs[1:]:
        if a <= cur_b:
            cur_b = max(cur_b, b)
        else:
            out.append((cur_a, cur_b))
            cur_a, cur_b = a, b
    out.append((cur_a, cur_b))
    return out

def max_rectangle_area_from_reds(text):
    pts = parse_points(text)
    n = len(pts)
    if n == 0:
        return 0

    edges = build_edges(pts)

    # unique x values where red tiles exist (these are candidate column x's)
    xs = sorted({x for x,_ in pts})

    # map x -> sorted list of red y's at that x (vertices)
    red_by_x = {}
    for x,y in pts:
        red_by_x.setdefault(x, []).append(y)
    for x in red_by_x:
        red_by_x[x].sort()

    # compute interior intervals at sample_x = x + 0.5 for every x in xs
    intervals_by_x = {}
    for x in xs:
        sample = x + 0.5
        iv = intervals_at_sample_x(edges, sample)
        # merging shouldn't usually be necessary, but safe
        iv = merge_intervals(iv)
        intervals_by_x[x] = iv

    best = 0
    m = len(xs)

    # For each pair of distinct x columns (xi < xj)
    for i in range(m):
        xi = xs[i]
        Si = intervals_by_x.get(xi, [])
        if not Si:
            continue
        red_y_i = red_by_x.get(xi, [])
        if not red_y_i:
            continue

        for j in range(i+1, m):
            xj = xs[j]
            Sj = intervals_by_x.get(xj, [])
            if not Sj:
                continue
            red_y_j = red_by_x.get(xj, [])
            if not red_y_j:
                continue

            # intersect interval lists Si and Sj (two-pointer)
            p = q = 0
            while p < len(Si) and q < len(Sj):
                a1,b1 = Si[p]
                a2,b2 = Sj[q]
                lo = max(a1, a2)
                hi = min(b1, b2)
                if lo <= hi:
                    # find red y's at xi in [lo, hi], and at xj in [lo, hi]
                    ys_i = red_y_i
                    ys_j = red_y_j
                    li = bisect_left(ys_i, lo)
                    ri = bisect_right(ys_i, hi)
                    lj = bisect_left(ys_j, lo)
                    rj = bisect_right(ys_j, hi)
                    if li < ri and lj < rj:
                        # iterate over the pairs - these lists are typically tiny (avg 1)
                        width = (xj - xi + 1)
                        for yi in ys_i[li:ri]:
                            for yj in ys_j[lj:rj]:
                                height = abs(yj - yi) + 1
                                area = width * height
                                if area > best:
                                    best = area
                # advance pointer with smaller endpoint
                if b1 < b2:
                    p += 1
                else:
                    q += 1

    return best

if __name__ == "__main__":
    with open("data.txt") as f:
        data = f.read()
    print(max_rectangle_area_from_reds(data))
