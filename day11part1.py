def parse_graph(input_lines):
    graph = {}
    for line in input_lines:
        if ':' in line:
            device, outputs = line.split(':', 1)
            graph[device.strip()] = [out.strip() for out in outputs.split()]
    return graph

def count_paths(graph, start, end, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()
    
    path = path + [start]
    if start == end:
        return 1
    
    if start in visited:
        return 0
    
    visited.add(start)
    count = 0
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            count += count_paths(graph, neighbor, end, path, visited.copy())
    
    visited.remove(start)
    return count

# Read input
with open('data.txt', 'r') as f:
    lines = f.readlines()

graph = parse_graph(lines)
result = count_paths(graph, 'you', 'out')
print(f"Number of paths from 'you' to 'out': {result}")