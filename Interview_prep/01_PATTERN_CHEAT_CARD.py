"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  INTERVIEW DAY QUICK REFERENCE — PATTERN RECOGNITION CARD                  ║
║  Read this 15 minutes before your interview.                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────
# STEP 1: READ THE PROBLEM. WHAT DOES IT SAY?
# ─────────────────────────────────────────────────────────────────

PATTERN_TRIGGERS = {
    # The problem says...                    # You think...
    "find pair that sums to":                "Hash Map → O(n)",
    "sorted array, find target":             "Binary Search → O(log n)",
    "sorted array, find pair":               "Two Pointers → O(n)",
    "longest/shortest subarray":             "Sliding Window → O(n)",
    "subarray sum equals k":                 "Prefix Sum + Hash Map → O(n)",
    "max subarray sum":                      "Kadane's Algorithm → O(n)",
    "merge overlapping intervals":           "Sort by start + sweep → O(n log n)",
    "find duplicates":                       "Hash Set → O(n)",
    "group by property":                     "Hash Map (defaultdict) → O(n)",
    "top k / kth largest":                   "Min-Heap of size k → O(n log k)",
    "find median from stream":              "Two Heaps → O(log n) per add",
    "valid brackets/nesting":               "Stack → O(n)",
    "next greater element":                 "Monotonic Stack → O(n)",
    "shortest path, unweighted":            "BFS → O(V+E)",
    "shortest path, weighted":              "Dijkstra → O(E log V)",
    "all paths / explore all":              "DFS / Backtracking",
    "ordering with dependencies":           "Topological Sort → O(V+E)",
    "detect cycle (directed)":              "DFS 3-state coloring → O(V+E)",
    "detect cycle (undirected)":            "Union-Find → O(E α(V))",
    "connected components":                 "Union-Find or BFS/DFS",
    "count ways to reach":                  "Dynamic Programming",
    "minimum cost / maximum value":         "Dynamic Programming",
    "can string be segmented":              "DP (word break pattern)",
    "generate all combinations":            "Backtracking",
    "generate all permutations":            "Backtracking",
    "prefix matching / autocomplete":       "Trie",
    "tree depth/height":                    "DFS Recursion",
    "tree level by level":                  "BFS with Queue",
    "BST search/validate":                  "BST property + Inorder",
    "linked list cycle":                    "Floyd's (slow/fast pointers)",
    "reverse linked list":                  "Three pointers iterative",
    "minimum window containing":            "Sliding Window + Counter",
    "matrix search":                        "Binary Search (flatten) or BFS/DFS",
    "design with O(1) operations":          "Hash Map + auxiliary structure",
}


# ─────────────────────────────────────────────────────────────────
# STEP 2: COMMON PYTHON SNIPPETS (saves you 5 min per problem)
# ─────────────────────────────────────────────────────────────────

PYTHON_SNIPPETS = """
# ━━━ IMPORTS YOU'LL ALWAYS NEED ━━━
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right
from math import inf, ceil
from typing import List, Optional

# ━━━ HASH MAP PATTERNS ━━━
count = Counter(arr)                    # frequency count
groups = defaultdict(list)              # group by key
seen = set()                            # existence check

# ━━━ HEAP PATTERNS ━━━
heap = []
heappush(heap, (priority, item))        # min-heap by priority
heappush(heap, (-val, item))            # MAX-heap trick
priority, item = heappop(heap)

# ━━━ BINARY SEARCH TEMPLATE ━━━
left, right = 0, len(arr) - 1
while left <= right:                    # find exact
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1

left, right = lo, hi                    # find boundary
while left < right:
    mid = (left + right) // 2
    if condition(mid): right = mid
    else: left = mid + 1
# answer = left

# ━━━ BFS TEMPLATE ━━━
queue = deque([start])
visited = {start}
level = 0
while queue:
    for _ in range(len(queue)):         # process level
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    level += 1

# ━━━ DFS TEMPLATE ━━━
visited = set()
def dfs(node):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor)

# ━━━ TOPOLOGICAL SORT (Kahn's) ━━━
in_degree = {u: 0 for u in graph}
for u in graph:
    for v in graph[u]:
        in_degree[v] += 1
queue = deque(u for u in in_degree if in_degree[u] == 0)
order = []
while queue:
    node = queue.popleft()
    order.append(node)
    for neighbor in graph[node]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

# ━━━ UNION-FIND ━━━
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])     # path compression
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    if rank[px] < rank[py]: px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]: rank[px] += 1
    return True

# ━━━ SLIDING WINDOW TEMPLATE ━━━
left = 0
for right in range(len(s)):
    # expand: add s[right] to window
    while INVALID:
        # shrink: remove s[left] from window
        left += 1
    # update answer with window [left, right]

# ━━━ KADANE'S ALGORITHM ━━━
max_sum = curr_sum = nums[0]
for num in nums[1:]:
    curr_sum = max(num, curr_sum + num)
    max_sum = max(max_sum, curr_sum)

# ━━━ BACKTRACKING TEMPLATE ━━━
def backtrack(start, path):
    if COMPLETE:
        result.append(path[:])
        return
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path)          # i+1 for combinations, i for reuse
        path.pop()                       # ← backtrack

# ━━━ DP TEMPLATE ━━━
dp = [0] * (n + 1)                      # or [[0]*(m+1) for _ in range(n+1)]
dp[0] = BASE_CASE
for i in range(1, n + 1):
    dp[i] = RECURRENCE(dp[i-1], dp[i-2], ...)
return dp[n]

# ━━━ TREE NODE ━━━
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ━━━ LINKED LIST NODE ━━━
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# ━━━ GRID DIRECTIONS ━━━
DIRS = [(0,1), (0,-1), (1,0), (-1,0)]   # right, left, down, up
for dr, dc in DIRS:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # process (nr, nc)
        pass

# ━━━ USEFUL ONE-LINERS ━━━
# Flatten 2D list
flat = [item for row in matrix for item in row]

# Character frequency
freq = [0] * 26
for c in s:
    freq[ord(c) - ord('a')] += 1

# Build adjacency list from edges
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # if undirected
"""


# ─────────────────────────────────────────────────────────────────
# STEP 3: COMPLEXITY REFERENCE
# ─────────────────────────────────────────────────────────────────

COMPLEXITY_TABLE = """
 TIME COMPLEXITY — What's fast enough?
 ┌────────────────┬──────────────────┬──────────────────────┐
 │ Input Size (n) │ Max Complexity   │ Algorithms           │
 ├────────────────┼──────────────────┼──────────────────────┤
 │ n ≤ 10         │ O(n!) or O(2^n)  │ Backtracking, brute  │
 │ n ≤ 20         │ O(2^n)           │ Bitmask DP           │
 │ n ≤ 100        │ O(n³)            │ Floyd-Warshall       │
 │ n ≤ 1,000      │ O(n²)            │ Nested loops, 2D DP  │
 │ n ≤ 100,000    │ O(n log n)       │ Sort, divide-conquer │
 │ n ≤ 1,000,000  │ O(n)             │ Hash map, one pass   │
 │ n ≤ 10^9       │ O(log n)         │ Binary search, math  │
 └────────────────┴──────────────────┴──────────────────────┘

 SPACE COMPLEXITY — Common trade-offs:
 ┌──────────┬────────────────────────────────────────┐
 │ O(1)     │ Two pointers, Kadane's, greedy vars    │
 │ O(k)     │ Heap of size k, sliding window of k    │
 │ O(n)     │ Hash map, stack, queue, 1D DP          │
 │ O(n²)    │ 2D DP, adjacency matrix                │
 │ O(h)     │ Tree recursion (h = log n balanced)    │
 └──────────┴────────────────────────────────────────┘
"""

if __name__ == "__main__":
    print("=== PATTERN TRIGGERS ===")
    for trigger, approach in PATTERN_TRIGGERS.items():
        print(f"  {trigger:45s} → {approach}")
    print(COMPLEXITY_TABLE)
