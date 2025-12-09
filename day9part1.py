def solve(input_text):
    
    lines = input_text.strip().split('\n')
    red_tiles = []
    for line in lines:
        x, y = map(int, line.split(','))
        red_tiles.append((x,y))
        
    n = len(red_tiles)
    
    max_area = 0
    
    for i in range(n):
        for j in range(i+1,n):
            
            x1,y1 = red_tiles[i]
            x2,y2 = red_tiles[j]
            
            width = abs(x2-x1) + 1
            height = abs(y2-y1) + 1
            
            area = width * height
            
            if area > max_area:
                max_area = area
    return max_area


with open('data.txt','r') as file:
    data = file.read()

print(solve(data))           