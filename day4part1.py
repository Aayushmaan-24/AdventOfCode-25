def giveAvailableRolls(inputStr):
    grid = [list(row) for row in inputStr.split('\n') if row]
    rows = len(grid)
    availableRolls = 0
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    for r in range(rows):
        for c in range(len(grid[r])):
            if grid[r][c] == '@':
                neighbours = 0
                for dr,dc in directions:
                    new_r, new_c = r + dr, c+dc
                    if 0 <= new_r < rows and 0 <= new_c < len(grid[new_r]) and grid[new_r][new_c] == '@':
                        neighbours += 1
                if neighbours < 4:
                    availableRolls += 1
                    
    return availableRolls
