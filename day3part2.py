def getTotalJoltage(banks, n=12):
    totalJoltage = 0
    for bank in banks:
        max_num = selectMax(bank, n)
        if max_num:
            totalJoltage += int(max_num)
    return totalJoltage

def selectMax(bank, k):
    n = len(bank)
    if k > n:
        return None
    if k == n:
        return bank
    drops = n-k
    stack = []
    for i , digit in enumerate(bank):
        while drops > 0 and stack and stack[-1] < digit:
            stack.pop()
            drops -= 1
        stack.append(digit)
    return ''.join(stack[:k])

