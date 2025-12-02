import bisect

def generateDoublePatterns(max_n: int):
    candidates = []
    max_len = len(str(max_n))
    for k in range(1, max_len//2+1):
        mult = 10 ** k +1
        s_min = 10 ** (k-1)
        s_max = min(10 ** k - 1, max_n//mult)
        if s_min > s_max:
            continue
        for s in range(s_min, s_max+1):
            n = s*mult
            candidates.append(n)
    candidates.sort()
    return candidates

def parse_ranges(range_str):
    ranges = []
    for part in range_str.split(','):
        part = part.strip()
        if not part:
            continue
        lo_str, hi_str = part.split('-')
        lo = int(lo_str)
        hi = int(hi_str)
        ranges.append((lo,hi))
    return ranges

def findInvalid(range_str):
    ranges = parse_ranges(range_str)
    if not ranges:
        return []
    max_n = max(hi for _, hi in ranges)
    candidates = generateDoublePatterns(max_n)
    invalid = []
    for lo,hi in ranges:
        left = bisect.bisect_left(candidates,lo)
        right = bisect.bisect_right(candidates, hi)
        invalid.extend(candidates[left:right])
    return invalid
    
    
def sum_invalids(range_str):
    return sum(findInvalid(range_str))

