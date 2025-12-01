def countZeros(rotations):
    
    initial = 50
    zeros = 0
    
    for rotation in rotations:
        
        rotation = rotation.strip()
        if not rotation:
            continue
        direction = rotation[0].upper()
        distance = int(rotation[1:])
        
        if direction == 'L':
            step = -1
        elif direction == 'R':
            step = 1
        else:
            raise ValueError(f"Bad Direction")
        
        for _ in range(distance):
            initial = (initial+step) % 100
            if initial == 0:
                zeros += 1
                
    return zeros