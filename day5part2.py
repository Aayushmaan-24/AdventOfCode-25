def countFreshIDs(data):
    
    ranges = [line.strip() for line in data.split('\n') if line.strip()]
    fresh_ranges = []
    
    for range in ranges:
        if '-' in range:
            start , end = map(int, range.split('-'))
            fresh_ranges.append((start, end))
    
    fresh_ranges.sort(key=lambda x:x[0])
    
    mergedRanges = []
    cur_start, cur_end = fresh_ranges[0]
    for start , end in fresh_ranges[1:]:
        if start <= cur_end + 1:
            cur_end = max(cur_end, end)
        else:
            mergedRanges.append((cur_start, cur_end))
            cur_start, cur_end = start,end
    mergedRanges.append((cur_start, cur_end))
    
    freshCount = 0
    for start, end in mergedRanges:
        freshCount += (end - start + 1)
    return freshCount
        
