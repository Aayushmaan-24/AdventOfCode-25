from math import prod

def solve_cephalopod_right_to_left(raw: str) -> int:


    lines = raw.rstrip("\n").splitlines()
    if len(lines) < 2:
        raise ValueError("Need at least one digit-row and one operator row")

    # Operator row is the last line
    op_line = lines[-1]
    num_lines = lines[:-1]  # rows containing digits (top to bottom)

    # Pad all rows to the same width so column indexing is consistent
    width = max(len(l) for l in lines)
    padded_digits = [l.ljust(width) for l in num_lines]
    padded_all = [l.ljust(width) for l in lines]  # includes operator row


    is_blank_col = [all(row[c] == ' ' for row in padded_all) for c in range(width)]

    # Group contiguous non-blank columns into problems
    groups = []
    cur = []
    for c in range(width):
        if not is_blank_col[c]:
            cur.append(c)
        else:
            if cur:
                groups.append(cur)
                cur = []
    if cur:
        groups.append(cur)

    grand_total = 0

    for g in groups:
        # Find operator inside this group's columns (scan operator row)
        op_chars = [padded_all[-1][c] for c in g]  # operator row sliced across group
        op = None
        for ch in op_chars:
            if ch in ('+', '*'):
                op = ch
                break
        if op is None:
            raise ValueError(f"No operator found in group columns {g}")

        # For cephalopod reading: each character column inside g is a separate number.
        # Numbers should be read right-to-left (so traverse columns reversed).
        nums = []
        for c in reversed(g):
            # Collect characters top-to-bottom from the digit rows for this column
            digits = ''.join(padded_digits[r][c] for r in range(len(padded_digits)))
            # Remove spaces — remaining characters form the number (top is most significant)
            digits = digits.replace(' ', '')
            if digits:  # ignore empty columns (should rarely happen)
                # Safety: ensure we only have digits (if input includes commas etc, adapt here)
                if not digits.isdigit():
                    raise ValueError(f"Non-digit characters found when parsing number: '{digits}' in column {c}")
                nums.append(int(digits))

        # If no numbers were found, skip (or raise)
        if not nums:
            continue

        # Compute value for this problem
        if op == '+':
            value = sum(nums)
        else:  # op == '*'
            value = prod(nums)

        grand_total += value

    return grand_total


if __name__ == "__main__":
    with open("data.txt", "r", encoding="utf-8") as f:
        text = f.read()

    answer = solve_cephalopod_right_to_left(text)
    print(answer)