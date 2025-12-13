
import re
from pathlib import Path
from pulp import LpProblem, LpVariable, lpSum, LpInteger, LpMinimize, LpStatusOptimal


# --------- parsing helpers ----------------------------------------------------

def parse_line(line):
    # extract {targets}
    mt = re.search(r'\{([^}]*)\}', line)
    if not mt:
        return None
    target = list(map(int, mt.group(1).split(',')))

    # extract button lists
    groups = re.findall(r'\(([^)]*)\)', line)
    buttons = []
    for g in groups:
        g = g.strip()
        if g == "":
            buttons.append([])
        else:
            buttons.append(list(map(int, g.split(','))))

    return target, buttons


# --------- solve one machine --------------------------------------------------

def solve_machine(target, buttons):
    # dimensions
    m = len(buttons)         # variables x0..xm-1
    n = len(target)          # counters

    # ILP
    prob = LpProblem("machine", LpMinimize)

    # variables: x_j >=0 integer
    x = [LpVariable(f"x{j}", lowBound=0, cat=LpInteger) for j in range(m)]

    # objective: minimize sum x_j
    prob += lpSum(x)

    # constraints: for each counter i, sum_{j containing i} x_j = target[i]
    for i in range(n):
        prob += lpSum(x[j] for j in range(m) if i in buttons[j]) == target[i]

    # solve
    status = prob.solve()
    if status != 1:  # 1 == LpStatusOptimal
        raise RuntimeError("No optimal solution found")

    # return the minimal total presses for this machine
    return sum(v.value() for v in x)


# --------- solve all machines in a file --------------------------------------

def solve_file(filename):
    total = 0
    for line in Path(filename).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parsed = parse_line(line)
        if not parsed:
            continue
        target, buttons = parsed
        total += solve_machine(target, buttons)
    return total


if __name__ == "__main__":
    print(solve_file("data.txt"))   # <-- your uploaded file
