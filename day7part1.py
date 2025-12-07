def count_splits(grid):
    
    rows, cols = len(grid), len(grid[0])
    start_col = grid[0].index('S')
    beams = {start_col}
    splits = 0
    
    for r in range(1,rows):
        new_beams = set()
        for c in beams:
            if 0<=c<=cols:
                if grid[r][c] == '^':
                    splits += 1
                    if c-1>=0:
                        new_beams.add(c-1)
                    if c+1<cols:
                        new_beams.add(c+1)
                elif grid[r][c] == '.':
                    new_beams.add(c)
        beams = new_beams
    return splits

with open('data.txt','r') as file:
    data = file.readlines()
    
print(count_splits(data))