def solve_cephalopod(raw: str) -> int:
    lines = raw.rstrip("\n").splitlines()
    op_line = lines[-1]
    num_lines = lines[:-1]

    width = max(len(line) for line in lines)
    padded = [line.ljust(width) for line in lines]

    # find blank columns
    is_space_col = [
        all(row[c] == ' ' for row in padded)
        for c in range(width)
    ]

    # group columns into problems
    groups = []
    current = []
    for c in range(width):
        if not is_space_col[c]:
            current.append(c)
        else:
            if current:
                groups.append(current)
                current = []
    if current:
        groups.append(current)

    total = 0
    from math import prod

    for g in groups:
        nums = []
        op = op_line[g[0]]
        for r in num_lines:
            chunk = r[g[0]:g[-1]+1].strip()
            if chunk:
                nums.append(int(chunk))

        total += sum(nums) if op == "+" else prod(nums)

    return total


if __name__ == "__main__":
    with open("data.txt", "r", encoding="utf-8") as f:
        text = f.read()
    answer = solve_cephalopod(text)
    print(answer)
