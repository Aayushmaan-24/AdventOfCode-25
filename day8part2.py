import math

def find_last_connection(input_text):
    # Step 1: Parse input
    lines = input_text.strip().split('\n')
    boxes = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))
    
    n = len(boxes)
    
    # Step 2: Calculate all pairwise distances
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            pairs.append((dist, i, j))
    
    # Step 3: Sort by distance
    pairs.sort()
    
    # Step 4: Union-Find data structure
    parent = list(range(n))
    size = [1] * n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x == root_y:
            return False
        if size[root_x] < size[root_y]:
            root_x, root_y = root_y, root_x
        parent[root_y] = root_x
        size[root_x] += size[root_y]
        return True
    
    # Step 5: Build MST until all are connected
    for dist, a, b in pairs:
        if union(a, b):
            # Check if all are connected
            if size[find(a)] == n:
                return boxes[a][0] * boxes[b][0]  # Multiply X-coordinates
    
    return None  # Should never reach here if input is valid

# Run
with open('data.txt', 'r') as file:
    data = file.read()
    
print(find_last_connection(data))