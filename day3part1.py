def getTotalJoltage(banks):
    totalJoltage = 0
    for bank in banks:
        max_pair = -1
        digits = [int(d) for d in bank]
        for i in range(len(digits)):
            for j in range(i+1, len(digits)):
                pair = digits[i] * 10 + digits[j]
                if pair > max_pair:
                    max_pair = pair
        totalJoltage += max_pair
    return totalJoltage
