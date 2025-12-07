def count_quantum_timelines(grid):
    rows, cols = len(grid), len(grid[0])
    start_col = grid[0].index('S')

    # Track how many timelines reach each cell
    timelines = [0] * cols
    timelines[start_col] = 1

    for r in range(1, rows):
        new_timelines = [0] * cols
        for c in range(cols):
            if timelines[c] == 0:
                continue
            cell = grid[r][c]
            if cell == '.':
                new_timelines[c] += timelines[c]
            elif cell == '^':
                if c - 1 >= 0:
                    new_timelines[c - 1] += timelines[c]
                if c + 1 < cols:
                    new_timelines[c + 1] += timelines[c]
        timelines = new_timelines

    return sum(timelines)

with open('data.txt','r') as file:
    data = file.readlines()
    
print(count_quantum_timelines(data))