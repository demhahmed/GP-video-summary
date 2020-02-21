import bisect


def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect.bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError
