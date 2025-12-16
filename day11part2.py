from collections import defaultdict, deque

DAC, FFT = "dac", "fft"

def parse_graph(lines):
    g = defaultdict(list)
    nodes = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        device, outputs = line.split(":", 1)
        device = device.strip()
        outs = outputs.split()
        g[device].extend(outs)
        nodes.add(device)
        nodes.update(outs)
    # Ensure every node appears as a key (so g[node] is safe)
    for n in nodes:
        g[n]  # touch
    return g

def count_paths_svr_to_out_visiting_dac_and_fft(graph, start="svr", end="out"):
    # Build reverse graph
    rev = defaultdict(list)
    for u, nbrs in graph.items():
        for v in nbrs:
            rev[v].append(u)

    # Reachable from start
    def reach_from(s):
        seen = set()
        dq = deque([s])
        seen.add(s)
        while dq:
            u = dq.popleft()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    dq.append(v)
        return seen

    # Can reach end (reverse BFS from end)
    def can_reach(t):
        seen = set()
        dq = deque([t])
        seen.add(t)
        while dq:
            u = dq.popleft()
            for p in rev[u]:
                if p not in seen:
                    seen.add(p)
                    dq.append(p)
        return seen

    if start not in graph or end not in graph:
        return 0

    from_start = reach_from(start)
    to_end = can_reach(end)
    relevant = from_start & to_end
    if end not in relevant:
        return 0

    # Topological sort on relevant subgraph
    indeg = {u: 0 for u in relevant}
    for u in relevant:
        for v in graph[u]:
            if v in relevant:
                indeg[v] += 1

    q = deque([u for u in relevant if indeg[u] == 0])
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v in graph[u]:
            if v in relevant:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

    if len(topo) != len(relevant):
        # Cycle in the relevant subgraph. In that case, "number of paths" may be
        # enormous or undefined (infinite) unless you restrict to simple paths.
        raise ValueError("Cycle detected in svr->out relevant subgraph; DAG DP not applicable.")

    def reqbit(node):
        b = 0
        if node == DAC: b |= 1
        if node == FFT: b |= 2
        return b

    # dp[u][mask] = number of paths from u to end, given we've already visited
    # required devices encoded by mask BEFORE stepping onto u.
    dp = {u: [0, 0, 0, 0] for u in relevant}

    for u in reversed(topo):
        ub = reqbit(u)
        for mask in range(4):
            mask2 = mask | ub
            if u == end:
                dp[u][mask] = 1 if mask2 == 3 else 0
            else:
                total = 0
                for v in graph[u]:
                    if v in relevant:
                        total += dp[v][mask2]
                dp[u][mask] = total

    return dp[start][0]

# ---- run ----
with open("data.txt", "r") as f:
    graph = parse_graph(f)

ans = count_paths_svr_to_out_visiting_dac_and_fft(graph, start="svr", end="out")
print(ans)