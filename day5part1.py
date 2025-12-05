def count_fresh_ingridients(data):
    
    parts = data.strip().split('\n\n')
    ranges_text = parts[0].split('\n')
    available_ids = [int(line) for line in parts[1].split('\n') if line.strip()]
    
    fresh_ranges = []
    for line in ranges_text:
        if '-' in line:
            start , end = map(int, line.split('-'))
            fresh_ranges.append((start,end))
            
    fresh_count = 0
    for ingridient_id in available_ids:
        is_fresh = False
        for start , end in fresh_ranges:
            if start <= ingridient_id <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1
    return fresh_count

with open('database.txt','r') as file:
    data = file.read()
print(count_fresh_ingridients(data))