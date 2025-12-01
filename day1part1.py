def count_Zero(rotations):
    
    initial = 50
    zeros = 0
    
    for rotation in rotations:
        
        rotation = rotation.strip()
        if not rotation:
            continue
        direction = rotation[0].upper()
        distance = int(rotation[1:])
        
        if direction == 'L':
            initial = (initial - distance) % 100
        elif direction == 'R':
            initial = (initial + distance) % 100
        else:
            raise ValueError(f"Bad direction")
        
        if initial == 0:
            zeros += 1
    return zeros
