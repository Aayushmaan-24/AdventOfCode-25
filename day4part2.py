def canBeRemoved(inputStr):
    
    grid = [list(row) for row in inputStr.split('\n') if row]
    rows = len(grid)
    removed = 0
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    while True:
        rolls = []
        for r in range(rows):
            for c in range(len(grid[r])):
                if grid[r][c] != '@':
                    continue
                neighbor = 0
                for dr, dc in directions:
                    new_r, new_c = r+dr, c+dc
                    if 0 <= new_r < rows and 0<=new_c<len(grid[new_r]) and grid[new_r][new_c] == '@':
                        neighbor += 1
                if neighbor < 4:
                    rolls.append((r,c))
        if not rolls:
            break
        removedNow = len(rolls)
        removed += removedNow
        for r,c in rolls:
            grid[r][c] = '.'
    return removed

