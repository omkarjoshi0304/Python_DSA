# NEETCODE 150 — COMPLETE REVISION GUIDE
**Omkar Joshi — Final Interview Prep Sprint**

> You've solved all 150 problems. This guide consolidates every pattern, algorithm, and technique into one reference for rapid revision before interviews.

---

## How to Use This Guide

**For Daily Revision:**
- Pick 1-2 topics per day
- Read the pattern summary
- Re-solve the ★★★ problems from memory (no looking!)
- Check off the revision checklist

**The Week Before Interview:**
- Read this entire guide in one sitting (90 min)
- Re-solve all ★★★ problems (there are 35)
- Review the "Common Mistakes" sections

**The Night Before:**
- Read only the "Quick Reference" sections
- Skim the code templates
- Sleep early!

---

## Table of Contents

1. [Arrays & Hashing](#1-arrays--hashing)
2. [Two Pointers](#2-two-pointers)
3. [Sliding Window](#3-sliding-window)
4. [Stack](#4-stack)
5. [Binary Search](#5-binary-search)
6. [Linked List](#6-linked-list)
7. [Trees](#7-trees)
8. [Tries](#8-tries)
9. [Heap / Priority Queue](#9-heap--priority-queue)
10. [Backtracking](#10-backtracking)
11. [Graphs](#11-graphs)
12. [Advanced Graphs](#12-advanced-graphs)
13. [1-D Dynamic Programming](#13-1-d-dynamic-programming)
14. [2-D Dynamic Programming](#14-2-d-dynamic-programming)
15. [Greedy](#15-greedy)
16. [Intervals](#16-intervals)
17. [Math & Geometry](#17-math--geometry)
18. [Bit Manipulation](#18-bit-manipulation)

---

## 1. Arrays & Hashing

### Core Concepts

**Hash Map (dict):** O(1) lookup, insertion, deletion (average case)
- Use when: "Have I seen this before?", "What's the count/frequency?", "Map X to Y"
- Python: `d = {}`, `d = defaultdict(list)`, `Counter(arr)`

**Hash Set:** O(1) membership check
- Use when: "Does X exist?", "Remove duplicates"
- Python: `s = set()`, `s.add(x)`, `x in s`

### The Core Pattern: Complement/Pair Search

```python
# THE FOUNDATIONAL PATTERN — appears in 30% of problems
def two_sum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

**Why it works:** Instead of O(n²) nested loop checking every pair, we ask "what number would complete this pair?" and check if we've seen it in O(1).

### Problems & Patterns (9 total)

| # | Problem | Pattern | Key Insight | Priority |
|---|---------|---------|-------------|----------|
| 1 | Contains Duplicate | Hash Set | If len(set) == len(list) → no duplicates | ★★ |
| 2 | Valid Anagram | Counter / Frequency Array | Sort or count frequencies | ★★ |
| 3 | Two Sum | Hash Map (complement) | Store seen values, check complement | ★★★ |
| 4 | Group Anagrams | Hash Map (sorted tuple key) | Anagrams have same sorted chars | ★★★ |
| 5 | Top K Frequent Elements | Bucket Sort OR Heap | Bucket: index=frequency, O(n) | ★★★ |
| 6 | Product of Array Except Self | Prefix/Suffix products | Answer[i] = prefix[i] × suffix[i] | ★★★ |
| 7 | Valid Sudoku | Hash Set per row/col/box | Track seen in 3 separate sets | ★★ |
| 8 | Encode and Decode Strings | Length prefix | "4#word5#hello" format | ★ |
| 9 | Longest Consecutive Sequence | Hash Set + Smart Start | Only start sequence if n-1 not in set | ★★★ |

### Quick Reference Template

```python
from collections import defaultdict, Counter

# Frequency count
count = Counter(arr)               # {'a': 3, 'b': 2}
freq = defaultdict(int)
for x in arr: freq[x] += 1

# Grouping by property
groups = defaultdict(list)
for item in items:
    key = compute_key(item)
    groups[key].append(item)

# Remove duplicates (preserve order)
seen = set()
result = [x for x in arr if not (x in seen or seen.add(x))]
```

### Common Mistakes

- ❌ Using `list` for membership checks (`if x in my_list` is O(n))
- ❌ Forgetting that dict keys must be hashable (can't use list/dict as key)
- ✅ Use `tuple(sorted(s))` as key for anagrams, not just `sorted(s)`

### Revision Checklist

- [ ] Can solve Two Sum in under 3 minutes
- [ ] Know when to use Counter vs defaultdict vs plain dict
- [ ] Understand bucket sort for Top K Frequent
- [ ] Can explain prefix/suffix product approach without code

---

## 2. Two Pointers

### Core Concepts

**Two Pointers:** Use two variables to traverse data, usually:
- **Opposite ends:** left=0, right=len-1, move toward each other
- **Same direction, different speeds:** slow/fast (Floyd's algorithm)

**When to use:**
- Sorted array + find pair/triplet
- Linked list cycle detection
- In-place array modification
- Palindrome checks

### The Pattern

```python
# OPPOSITE ENDS — for sorted arrays
left, right = 0, len(arr) - 1
while left < right:
    if condition_met(arr[left], arr[right]):
        # found answer
        return result
    elif need_larger:
        left += 1
    else:
        right -= 1

# SLOW/FAST — for linked lists
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True  # cycle detected
```

### Problems & Patterns (5 total)

| # | Problem | Pattern | Key Insight | Priority |
|---|---------|---------|-------------|----------|
| 10 | Valid Palindrome | Two pointers (ends) | Skip non-alphanumeric, compare lowercase | ★★ |
| 11 | Two Sum II (Sorted) | Two pointers (ends) | Use sorted property, O(1) space | ★★ |
| 12 | 3Sum | Sort + Fix one + Two pointers | Reduce to 2Sum, skip duplicates | ★★★ |
| 13 | Container With Most Water | Two pointers (ends) | Move shorter wall inward | ★★★ |
| 14 | Trapping Rain Water | Two pointers + track maxes | Water = min(left_max, right_max) - height | ★★ |

### 3Sum Deep Dive (Most Common Interview Question)

```python
def three_sum(nums):
    nums.sort()  # MUST sort first
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i-1]:
            continue
            
        left, right = i + 1, len(nums) - 1
        target = -nums[i]  # we want a + b = -c
        
        while left < right:
            total = nums[left] + nums[right]
            if total < target:
                left += 1
            elif total > target:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates for second element
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                # Skip duplicates for third element
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
    
    return result
```

**Why sort?** Sorting enables two pointers to systematically search the space. After sorting, we know: moving left increases sum, moving right decreases sum.

### Common Mistakes

- ❌ Forgetting to skip duplicates in 3Sum (gets duplicate triplets)
- ❌ Not checking `fast and fast.next` before `fast.next.next` (NoneType error)
- ✅ Always check pointers don't cross: `while left < right`

### Revision Checklist

- [ ] Can solve 3Sum with proper duplicate handling
- [ ] Understand Container With Most Water greedy choice
- [ ] Know Floyd's cycle detection (tortoise & hare)

---

## 3. Sliding Window

### Core Concepts

**Sliding Window:** A subarray/substring that expands and contracts as you iterate.
- Avoids recomputing everything from scratch for each position
- Almost always gives O(n) solution vs O(n²) brute force

**Two Types:**
1. **Fixed size:** Window is always k elements
2. **Variable size:** Window grows/shrinks based on condition

### The Universal Template

```python
# VARIABLE SIZE (most common)
left = 0
for right in range(len(arr)):
    # ADD arr[right] to window state
    window_state.add(arr[right])
    
    # SHRINK window while invalid
    while WINDOW_IS_INVALID:
        # REMOVE arr[left] from window state
        window_state.remove(arr[left])
        left += 1
    
    # UPDATE answer (window [left, right] is valid)
    max_length = max(max_length, right - left + 1)
```

### Problems & Patterns (6 total)

| # | Problem | State Tracking | Expand/Shrink Logic | Priority |
|---|---------|----------------|---------------------|----------|
| 15 | Best Time to Buy/Sell Stock | Track min price | Not a window, but similar idea | ★★★ |
| 16 | Longest Substring Without Repeating | Set of chars | Shrink when duplicate found | ★★★ |
| 17 | Longest Repeating Char Replacement | Char frequencies | Shrink when replacements > k | ★★ |
| 18 | Permutation in String | Char frequencies | Compare window to target counts | ★★ |
| 19 | Minimum Window Substring | Char frequencies + formed count | Shrink while all chars met | ★★★ |
| 20 | Sliding Window Maximum | Monotonic deque | Deque stores indices in decreasing order | ★★ |

### Longest Substring Without Repeating Characters

```python
def length_of_longest_substring(s):
    char_set = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        # Shrink until no duplicates
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Why this works:** Each character is added once and removed once → O(n) total operations despite the inner while loop.

### Minimum Window Substring (Hardest Pattern)

```python
def min_window(s, t):
    if not s or not t: return ""
    
    dict_t = Counter(t)
    required = len(dict_t)  # unique chars needed
    
    left = 0
    formed = 0              # unique chars with required freq
    window_counts = defaultdict(int)
    ans = (float('inf'), None, None)  # (length, left, right)
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] += 1
        
        # Check if this char's frequency matches requirement
        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1
        
        # Try to shrink window while it's valid
        while left <= right and formed == required:
            # Update answer
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            
            # Shrink from left
            char = s[left]
            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1
            left += 1
    
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2]+1]
```

### Common Mistakes

- ❌ Not handling edge case: empty string or k=0
- ❌ Forgetting to update `left` pointer inside while loop
- ✅ Use `right - left + 1` for length (inclusive range)

### Revision Checklist

- [ ] Can recite the sliding window template from memory
- [ ] Understand difference between fixed vs variable window
- [ ] Know when to use set vs Counter for state tracking

---

## 4. Stack

### Core Concepts

**Stack:** LIFO (Last In, First Out)
- Python: just use a list with `append()` and `pop()`
- O(1) push, pop, peek

**When to use:**
- Matching/nesting (parentheses, HTML tags)
- "Next greater/smaller element" → **Monotonic Stack**
- Undo/redo, function call tracking
- DFS (iterative)

### The Monotonic Stack Pattern

```python
# NEXT GREATER ELEMENT (template)
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # stores indices
    
    for i in range(len(nums)):
        # While current is greater than stack top
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]  # found its next greater
        stack.append(i)
    
    return result
```

**Why monotonic?** Stack maintains elements in increasing/decreasing order. When we see a number that breaks the pattern, we know it's the "next greater" for all smaller numbers in the stack.

### Problems & Patterns (7 total)

| # | Problem | Pattern | Key Insight | Priority |
|---|---------|---------|-------------|----------|
| 21 | Valid Parentheses | Matching stack | Push openers, pop on closers | ★★★ |
| 22 | Min Stack | Two stacks | One for values, one tracks min | ★★ |
| 23 | Evaluate Reverse Polish Notation | Operator stack | Pop operands, push result | ★ |
| 24 | Generate Parentheses | Backtracking (not stack) | Track open/close counts | ★★ |
| 25 | Daily Temperatures | Monotonic stack (decreasing) | Stack stores indices, not values | ★★★ |
| 26 | Car Fleet | Sort + monotonic stack | Stack stores times to reach target | ★★ |
| 27 | Largest Rectangle in Histogram | Monotonic stack (increasing) | Width = curr - prev_stack_top - 1 | ★★ |

### Daily Temperatures (Classic Monotonic Stack)

```python
def daily_temperatures(temps):
    result = [0] * len(temps)
    stack = []  # stores indices
    
    for i, t in enumerate(temps):
        # While current temp is warmer than stack top
        while stack and t > temps[stack[-1]]:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx  # days until warmer
        stack.append(i)
    
    return result
```

**Complexity:** O(n) time, O(n) space. Each element pushed and popped at most once.

### Common Mistakes

- ❌ Storing values in monotonic stack (should store indices!)
- ❌ Wrong bracket matching: need to check PAIRS, not just counts
- ✅ Check `stack` before accessing `stack[-1]`

### Revision Checklist

- [ ] Can solve Valid Parentheses in under 2 minutes
- [ ] Understand why monotonic stack is O(n) not O(n²)
- [ ] Know Min Stack design (two stacks vs one with tuples)

---

## 5. Binary Search

### Core Concepts

**Binary Search:** Cut search space in half each step → O(log n)

**Two Flavors:**
1. **Find exact value** in sorted array
2. **Find boundary** or search on answer space

### Templates

```python
# TEMPLATE 1: Find exact value
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:  # NOTE: <=
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # not found

# TEMPLATE 2: Find leftmost True (boundary)
def binary_search_boundary(lo, hi, condition):
    left, right = lo, hi
    
    while left < right:  # NOTE: <
        mid = (left + right) // 2
        if condition(mid):
            right = mid      # mid might be answer
        else:
            left = mid + 1   # mid too small
    
    return left
```

### Problems & Patterns (7 total)

| # | Problem | Type | Key Insight | Priority |
|---|---------|------|-------------|----------|
| 28 | Binary Search | Basic template | Find exact value | ★★★ |
| 29 | Search a 2D Matrix | Treat as 1D | row = idx // cols, col = idx % cols | ★★ |
| 30 | Koko Eating Bananas | Search on answer | Can she finish in h hours at speed k? | ★★★ |
| 31 | Find Min in Rotated Sorted Array | Modified BS | Compare mid with right, not left | ★★ |
| 32 | Search in Rotated Sorted Array | Modified BS | One half is always sorted | ★★★ |
| 33 | Time Based Key-Value Store | BS on timestamps | Store list per key, BS to find ≤ timestamp | ★ |
| 34 | Median of Two Sorted Arrays | Binary search on partition | Tricky — find correct partition point | ★ |

### Koko Eating Bananas (Binary Search on Answer)

```python
def min_eating_speed(piles, h):
    import math
    
    def can_finish(speed):
        hours = sum(math.ceil(pile / speed) for pile in piles)
        return hours <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = (left + right) // 2
        if can_finish(mid):
            right = mid      # try slower
        else:
            left = mid + 1   # must go faster
    
    return left
```

**Key insight:** If speed K works, all speeds > K also work. This monotonic property enables binary search.

### Search in Rotated Sorted Array

```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        
        # Determine which half is sorted
        if nums[left] <= nums[mid]:  # left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1  # target in sorted left half
            else:
                left = mid + 1   # target in rotated right half
        else:  # right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1   # target in sorted right half
            else:
                right = mid - 1  # target in rotated left half
    
    return -1
```

### Common Mistakes

- ❌ Off-by-one errors: `left <= right` vs `left < right`
- ❌ Integer overflow: use `left + (right - left) // 2` in other languages
- ✅ Always think: "What makes left half vs right half different?"

### Revision Checklist

- [ ] Can write both BS templates from memory
- [ ] Understand when to use `<=` vs `<` in while condition
- [ ] Know "binary search on answer" pattern (Koko bananas)

---

## 6. Linked List

### Core Concepts

**Linked List:** Chain of nodes, each pointing to next (and optionally previous).

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

**Key Techniques:**
- **Dummy head:** Simplifies edge cases (empty list, modify head)
- **Slow/Fast pointers:** Find middle, detect cycles
- **Reverse:** Three pointers (prev, curr, next)

### Problems & Patterns (11 total)

| # | Problem | Technique | Key Insight | Priority |
|---|---------|-----------|-------------|----------|
| 35 | Reverse Linked List | Three pointers | prev=None, curr=head, save next | ★★★ |
| 36 | Merge Two Sorted Lists | Dummy head | Compare and link smaller node | ★★★ |
| 37 | Reorder List | Slow/Fast + Reverse + Merge | Find mid, reverse 2nd half, merge | ★★ |
| 38 | Remove Nth From End | Two pointers (gap of n) | Fast goes n ahead, then move both | ★★ |
| 39 | Copy List with Random Pointer | Hash map | Map old → new nodes | ★ |
| 40 | Add Two Numbers | Carry tracking | Handle carry, different lengths | ★ |
| 41 | Linked List Cycle | Floyd's (slow/fast) | If they meet → cycle exists | ★★★ |
| 42 | Find Duplicate Number | Floyd's on array | Treat as linked list: next = nums[i] | ★ |
| 43 | LRU Cache | Hash map + Doubly Linked List | O(1) get/put with eviction | ★★★ |
| 44 | Merge K Sorted Lists | Min heap | Pop min, add its next to heap | ★★ |
| 45 | Reverse Nodes in K-Group | Recursion + reverse | Reverse k at a time, connect groups | ★ |

### Reverse Linked List (Must Know)

```python
def reverse_list(head):
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next  # save next
        curr.next = prev       # reverse pointer
        prev = curr            # advance prev
        curr = next_temp       # advance curr
    
    return prev  # new head
```

### Linked List Cycle Detection (Floyd's)

```python
def has_cycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False

# To find cycle start (LC 142):
# After meeting, reset slow to head
# Move both 1 step at a time
# They meet at cycle start
```

**Why it works:** In a cycle, fast gains 1 step per iteration. It will eventually catch slow.

### LRU Cache (Design)

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key → node
        # Dummy head/tail for easier insert/remove
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)  # move to front (most recent)
            return node.val
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            # Evict LRU (tail.prev)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
    
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add(self, node):  # add to front (after head)
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
```

### Common Mistakes

- ❌ Not checking `fast.next` before `fast.next.next` (NoneType error)
- ❌ Losing reference to next node before changing pointers
- ✅ Use dummy head to simplify edge cases

### Revision Checklist

- [ ] Can reverse a linked list in under 2 minutes
- [ ] Understand Floyd's cycle detection proof
- [ ] Can design LRU Cache with O(1) operations

---

## 7. Trees

### Core Concepts

**Binary Tree:** Each node has at most 2 children.
**Binary Search Tree (BST):** left < root < right for all nodes.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

**Traversals (must know all):**
- **Inorder:** Left → Root → Right (gives sorted order for BST)
- **Preorder:** Root → Left → Right (copy structure)
- **Postorder:** Left → Right → Root (delete tree, calculate sizes)
- **Level-order:** BFS with queue

### Recursive Template

```python
def solve(node):
    # BASE CASE
    if not node:
        return base_value
    
    # RECURSIVE CASE
    left_result = solve(node.left)
    right_result = solve(node.right)
    
    # COMBINE
    return combine(node.val, left_result, right_result)
```

### Problems & Patterns (15 total)

| # | Problem | Pattern | Key Insight | Priority |
|---|---------|---------|-------------|----------|
| 46 | Invert Binary Tree | DFS (swap children) | Swap left and right recursively | ★★★ |
| 47 | Max Depth of Binary Tree | DFS | 1 + max(left_depth, right_depth) | ★★★ |
| 48 | Diameter of Binary Tree | DFS (track global max) | Diameter through node = left + right | ★ |
| 49 | Balanced Binary Tree | DFS (bottom-up) | Check heights and balance at each node | ★ |
| 50 | Same Tree | DFS | Recursively check val, left, right | ★ |
| 51 | Subtree of Another Tree | DFS | Check isSame at each node | ★ |
| 52 | Lowest Common Ancestor (BST) | BST property | If p < root < q, root is LCA | ★★★ |
| 53 | Binary Tree Level Order Traversal | BFS (queue) | Process nodes level by level | ★★★ |
| 54 | Binary Tree Right Side View | BFS or DFS | Last node at each level | ★ |
| 55 | Count Good Nodes | DFS (track max so far) | Good if val >= max in path | ★ |
| 56 | Validate BST | DFS (with bounds) | Check low < val < high recursively | ★★★ |
| 57 | Kth Smallest in BST | Inorder traversal | Inorder gives sorted order | ★★ |
| 58 | Construct Tree from Pre+In | Recursion | Preorder[0] = root, split by inorder | ★ |
| 59 | Binary Tree Max Path Sum | DFS (track global max) | Max through node = left + val + right | ★★ |
| 60 | Serialize/Deserialize Tree | Preorder + null markers | Use "N" for null nodes | ★★ |

### Validate Binary Search Tree (Common Mistake!)

```python
def is_valid_bst(root):
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        
        # Current node must be in range (low, high)
        if not (low < node.val < high):
            return False
        
        # Left subtree: all values < node.val
        # Right subtree: all values > node.val
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))
    
    return validate(root)
```

**Common mistake:** Only checking `left.val < root.val < right.val` for immediate children. Must check against ALL ancestors!

### Binary Tree Level Order Traversal (BFS)

```python
def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)  # nodes at this level
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

### Common Mistakes

- ❌ Forgetting to check `if not node` at start of recursion
- ❌ Validate BST: only checking immediate children
- ✅ Inorder traversal of BST must be strictly increasing

### Revision Checklist

- [ ] Can write all 4 traversals from memory
- [ ] Understand Validate BST with bounds
- [ ] Know LCA for BST vs general binary tree difference

---

## 8. Tries

### Core Concepts

**Trie (Prefix Tree):** Tree where each node represents a character. Paths from root spell words.

**When to use:**
- Autocomplete / prefix matching
- Spell checker
- Word search in grid with dictionary

### Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char → TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix):
        return self._find(prefix) is not None
    
    def _find(self, text):
        node = self.root
        for char in text:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### Problems & Patterns (3 total)

| # | Problem | Pattern | Priority |
|---|---------|---------|----------|
| 61 | Implement Trie | Basic operations | ★★ |
| 62 | Design Add and Search Words | Trie + DFS (for '.') | ★★ |
| 63 | Word Search II | Trie + Backtracking | ★ |

### Revision Checklist

- [ ] Can implement Trie from scratch
- [ ] Understand when Trie is better than hash map

---

## 9. Heap / Priority Queue

### Core Concepts

**Heap:** Tree-based structure where parent is always smaller (min-heap) or larger (max-heap) than children.

**Python:** `heapq` module provides min-heap.

```python
import heapq

heap = []
heapq.heappush(heap, val)       # O(log n)
min_val = heapq.heappop(heap)   # O(log n)
min_val = heap[0]               # O(1) peek

# Max-heap trick: negate values
heapq.heappush(heap, -val)
max_val = -heapq.heappop(heap)

# K largest/smallest
k_largest = heapq.nlargest(k, nums)
k_smallest = heapq.nsmallest(k, nums)
```

### Problems & Patterns (7 total)

| # | Problem | Pattern | Key Insight | Priority |
|---|---------|---------|-------------|----------|
| 64 | Kth Largest Element in Stream | Min-heap of size k | Maintain k largest, heap[0] is kth | ★★ |
| 65 | Last Stone Weight | Max-heap | Smash two largest repeatedly | ★ |
| 66 | K Closest Points to Origin | Min-heap | Use distance as key | ★ |
| 67 | Kth Largest Element in Array | QuickSelect or Heap | Heap: O(n log k), QuickSelect: O(n) avg | ★★★ |
| 68 | Task Scheduler | Max-heap + cooling queue | Process most frequent task available | ★★ |
| 69 | Design Twitter | Heap for merge K lists | Merge K sorted timelines | ★ |
| 70 | Find Median from Data Stream | Two heaps (max + min) | Max-heap for lower half, min-heap for upper | ★★★ |

### Find Median from Data Stream (Classic)

```python
class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (lower half)
        self.large = []  # min-heap (upper half)
    
    def add_num(self, num):
        # Add to small (negate for max-heap)
        heapq.heappush(self.small, -num)
        
        # Balance: ensure all in small ≤ all in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes (small can have 1 more element)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

### Common Mistakes

- ❌ Forgetting Python heapq is min-heap (need to negate for max)
- ✅ For Kth largest: use min-heap of size k, not max-heap

### Revision Checklist

- [ ] Understand two-heap median technique
- [ ] Know when to use heap vs sorting

---

## 10. Backtracking

### Core Concepts

**Backtracking:** Build solutions incrementally, abandon when you detect it won't work.

**Template:**
```python
def backtrack(state, choices):
    if IS_COMPLETE(state):
        result.append(state.copy())  # found a solution
        return
    
    for choice in choices:
        if IS_VALID(choice, state):
            MAKE_CHOICE(state, choice)
            backtrack(state, remaining_choices)
            UNDO_CHOICE(state, choice)  # ← backtrack!
```

### Problems & Patterns (9 total)

| # | Problem | Pattern | Key Insight | Priority |
|---|---------|---------|-------------|----------|
| 71 | Subsets | Include/exclude each element | 2^n subsets | ★★★ |
| 72 | Combination Sum | Backtrack with target reduction | Can reuse elements | ★★ |
| 73 | Permutations | Swap or used set | n! permutations | ★★★ |
| 74 | Subsets II (with duplicates) | Sort + skip duplicates | Skip if nums[i] == nums[i-1] | ★ |
| 75 | Combination Sum II | Sort + skip duplicates | Can't reuse elements | ★ |
| 76 | Word Search | DFS + backtracking on grid | Mark visited, unmark on backtrack | ★★ |
| 77 | Palindrome Partitioning | Backtrack on partitions | Check each substring is palindrome | ★ |
| 78 | Letter Combinations of Phone | Backtrack through digit→letters map | Classic backtracking | ★ |
| 79 | N-Queens | Backtrack + validate placement | Track cols, diagonals in sets | ★ |

### Subsets (Fundamental Pattern)

```python
def subsets(nums):
    result = []
    
    def backtrack(start, current):
        result.append(current[:])  # add current subset
        
        for i in range(start, len(nums)):
            current.append(nums[i])      # include nums[i]
            backtrack(i + 1, current)
            current.pop()                # exclude nums[i] (backtrack)
    
    backtrack(0, [])
    return result
```

### Permutations

```python
def permutations(nums):
    result = []
    
    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return
        
        for num in nums:
            if num not in current:       # can't reuse
                current.append(num)
                backtrack(current)
                current.pop()
    
    backtrack([])
    return result
```

### Common Mistakes

- ❌ Appending reference: `result.append(current)` instead of `current[:]`
- ❌ Not undoing the choice (forgetting to pop/remove)
- ✅ Sort first when dealing with duplicates

### Revision Checklist

- [ ] Can write subsets and permutations from memory
- [ ] Understand the difference between combinations and permutations
- [ ] Know how to handle duplicates (sort + skip)

---

## 11. Graphs

### Core Concepts

**Graph:** Nodes connected by edges.
- **Directed:** Edges have direction (A → B)
- **Undirected:** Edges are bidirectional (A ↔ B)

**Representations:**
```python
# Adjacency list (most common)
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

# Or for numbered nodes
graph = [[] for _ in range(n)]
for u, v in edges:
    graph[u].append(v)
```

**Traversals:**
- **BFS:** Shortest path (unweighted), level-order
- **DFS:** Explore all paths, cycle detection, connected components

### Templates

```python
# BFS
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = {start}
    
    while queue:
        node = queue.popleft()
        # process node
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# DFS (recursive)
def dfs(graph, node, visited):
    visited.add(node)
    # process node
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

### Problems & Patterns (13 total)

| # | Problem | Algorithm | Key Insight | Priority |
|---|---------|-----------|-------------|----------|
| 80 | Number of Islands | BFS or DFS | Count connected components | ★★★ |
| 81 | Clone Graph | BFS/DFS + hash map | Map old → new nodes | ★★ |
| 82 | Max Area of Island | DFS | Track area while exploring | ★ |
| 83 | Pacific Atlantic Water Flow | Multi-source BFS/DFS | Start from ocean borders | ★★ |
| 84 | Surrounded Regions | DFS from borders | Capture only regions not touching border | ★ |
| 85 | Rotting Oranges | BFS (multi-source) | Process all rotten simultaneously | ★ |
| 86 | Walls and Gates | BFS (multi-source) | Start from all gates | ★ |
| 87 | Course Schedule | DFS (cycle detection) | 3-state coloring | ★★★ |
| 88 | Course Schedule II | Topological sort (Kahn's) | BFS with in-degrees | ★★★ |
| 89 | Redundant Connection | Union-Find | Find edge that creates cycle | ★★ |
| 90 | Number of Connected Components | Union-Find or DFS | Count components in undirected graph | ★★ |
| 91 | Graph Valid Tree | Union-Find or DFS | n nodes, n-1 edges, all connected | ★★ |
| 92 | Word Ladder | BFS (shortest path) | Each word is a node, edges = 1 char diff | ★★ |

### Number of Islands (Foundational)

```python
def num_islands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] == '0'):
            return
        
        grid[r][c] = '0'  # mark visited
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    
    return count
```

### Course Schedule (Cycle Detection)

```python
def can_finish(num_courses, prerequisites):
    graph = {i: [] for i in range(num_courses)}
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # 0 = unvisited, 1 = in current path, 2 = fully processed
    state = [0] * num_courses
    
    def has_cycle(node):
        if state[node] == 1:  # cycle detected!
            return True
        if state[node] == 2:  # already verified
            return False
        
        state[node] = 1  # mark as in current path
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
        state[node] = 2  # mark as fully processed
        return False
    
    return not any(has_cycle(i) for i in range(num_courses))
```

### Course Schedule II (Topological Sort - Kahn's Algorithm)

```python
def find_order(num_courses, prerequisites):
    graph = {i: [] for i in range(num_courses)}
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Start with courses that have no prerequisites
    queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for dependent in graph[course]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    # If we ordered all courses → no cycle
    return order if len(order) == num_courses else []
```

**Your Red Hat angle:** "This is exactly the rollout dependency problem — deploying services in the right order given their dependencies."

### Common Mistakes

- ❌ Not checking bounds in grid DFS
- ❌ Forgetting to mark visited (infinite loop!)
- ✅ For cycle detection, need 3 states, not 2

### Revision Checklist

- [ ] Can write BFS and DFS templates from memory
- [ ] Understand 3-state cycle detection
- [ ] Know Kahn's algorithm for topological sort

---

## 12. Advanced Graphs

### Union-Find (Disjoint Set)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

### Problems & Patterns (6 total)

| # | Problem | Algorithm | Priority |
|---|---------|-----------|----------|
| 93 | Redundant Connection | Union-Find | ★★ |
| 94 | Graph Valid Tree | Union-Find | ★★ |
| 95 | Number of Connected Components | Union-Find | ★★ |
| 96 | Accounts Merge | Union-Find + DFS | ★ |
| 97 | Min Cost to Connect All Points | Prim's or Kruskal's MST | ★ |
| 98 | Network Delay Time | Dijkstra's | ★ |

### Dijkstra's Algorithm (Shortest Path - Weighted)

```python
import heapq

def network_delay_time(times, n, k):
    graph = {i: [] for i in range(1, n+1)}
    for u, v, w in times:
        graph[u].append((v, w))
    
    dist = {i: float('inf') for i in range(1, n+1)}
    dist[k] = 0
    heap = [(0, k)]  # (distance, node)
    
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue  # already found better path
        
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    max_dist = max(dist.values())
    return max_dist if max_dist != float('inf') else -1
```

### Revision Checklist

- [ ] Can implement Union-Find from scratch
- [ ] Understand path compression and union by rank
- [ ] Know when to use Dijkstra vs BFS

---

## 13. 1-D Dynamic Programming

### Core Concepts

**Dynamic Programming:** Solve problems by breaking into overlapping subproblems.

**The Recipe:**
1. Define state: What does `dp[i]` represent?
2. Find recurrence: `dp[i] = f(dp[smaller])`
3. Set base case: `dp[0] = ?`
4. Fill table in order
5. Return `dp[target]`

### Problems & Patterns (12 total)

| # | Problem | Recurrence | Priority |
|---|---------|------------|----------|
| 99 | Climbing Stairs | dp[i] = dp[i-1] + dp[i-2] (Fibonacci) | ★★★ |
| 100 | Min Cost Climbing Stairs | dp[i] = cost[i] + min(dp[i-1], dp[i-2]) | ★★ |
| 101 | House Robber | dp[i] = max(dp[i-1], dp[i-2] + nums[i]) | ★★★ |
| 102 | House Robber II (circular) | Run twice: exclude first or last | ★★ |
| 103 | Longest Palindromic Substring | Expand around center OR 2D DP | ★★ |
| 104 | Palindromic Substrings | Count while checking each center | ★ |
| 105 | Decode Ways | dp[i] = dp[i-1] + dp[i-2] (if valid) | ★★ |
| 106 | Coin Change | dp[i] = min(dp[i-coin] + 1) | ★★★ |
| 107 | Maximum Product Subarray | Track max and min (for negatives) | ★★ |
| 108 | Word Break | dp[i] = any(dp[j] and s[j:i] in dict) | ★★★ |
| 109 | Longest Increasing Subsequence | dp[i] = max(dp[j] + 1) where nums[j] < nums[i] | ★★★ |
| 110 | Partition Equal Subset Sum | 0/1 Knapsack | ★ |

### House Robber (Classic Pattern)

```python
def rob(nums):
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    
    # Space-optimized: only need last 2 values
    prev2, prev1 = 0, 0
    for num in nums:
        current = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = current
    
    return prev1
```

**Why it works:** At each house, choose: rob it (prev2 + current) or skip it (prev1).

### Coin Change

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Longest Increasing Subsequence

```python
def length_of_lis(nums):
    if not nums: return 0
    
    dp = [1] * len(nums)
    
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

**Optimization:** Binary search with patience sorting → O(n log n)

### Common Mistakes

- ❌ Not initializing dp array correctly
- ❌ Forgetting base cases (dp[0])
- ✅ Check if you can space-optimize (only need last k values)

### Revision Checklist

- [ ] Can solve House Robber and Coin Change from memory
- [ ] Understand when to space-optimize (Fibonacci-like)
- [ ] Know the DP recipe (state, recurrence, base, fill, return)

---

## 14. 2-D Dynamic Programming

### Core Concepts

**2-D DP:** `dp[i][j]` represents state depending on two variables.

### Problems & Patterns (11 total)

| # | Problem | State | Recurrence | Priority |
|---|---------|-------|------------|----------|
| 111 | Unique Paths | dp[i][j] = paths to (i,j) | dp[i][j] = dp[i-1][j] + dp[i][j-1] | ★★ |
| 112 | Longest Common Subsequence | dp[i][j] = LCS of s1[:i], s2[:j] | If match: dp[i-1][j-1]+1, else max | ★★★ |
| 113 | Best Time to Buy/Sell (Cooldown) | State machine DP | 3 states: hold, sold, rest | ★★ |
| 114 | Coin Change 2 | dp[i][j] = ways to make j with first i coins | Include/exclude coin i | ★ |
| 115 | Target Sum | dp[i][sum] = ways to reach sum with i elements | DP on sum space | ★ |
| 116 | Interleaving String | dp[i][j] = can form s3[:i+j] | Check s1[i] or s2[j] matches | ★ |
| 117 | Longest Increasing Path in Matrix | DFS + memoization | Max path starting from each cell | ★ |
| 118 | Distinct Subsequences | dp[i][j] = count of t[:j] in s[:i] | Include/exclude s[i] | ★ |
| 119 | Edit Distance | dp[i][j] = ops to convert s1[:i] → s2[:j] | Insert, delete, replace | ★★ |
| 120 | Burst Balloons | dp[i][j] = max coins bursting (i,j) | Try each as last to burst | ★ |
| 121 | Regular Expression Matching | dp[i][j] = s[:i] matches p[:j] | Handle '.' and '*' | ★ |

### Longest Common Subsequence

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### Edit Distance (Levenshtein Distance)

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    
    # Base cases
    for i in range(m+1):
        dp[i][0] = i  # delete all
    for j in range(n+1):
        dp[0][j] = j  # insert all
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # no op needed
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # delete from word1
                    dp[i][j-1],    # insert into word1
                    dp[i-1][j-1]   # replace
                )
    
    return dp[m][n]
```

### Common Mistakes

- ❌ Off-by-one indexing (dp[i] vs input[i-1])
- ❌ Not initializing base cases (first row/column)
- ✅ Draw a small example table to understand the recurrence

### Revision Checklist

- [ ] Can solve LCS from memory
- [ ] Understand Edit Distance recurrence
- [ ] Know how to space-optimize (rolling array)

---

## 15. Greedy

### Core Concepts

**Greedy:** Make locally optimal choice at each step, hoping for global optimum.

**When does it work?** Problem has:
- Greedy choice property
- Optimal substructure

### Problems & Patterns (5 total)

| # | Problem | Greedy Choice | Priority |
|---|---------|---------------|----------|
| 122 | Maximum Subarray | Kadane's: reset if sum < 0 | ★★★ |
| 123 | Jump Game | Track max reachable | ★★ |
| 124 | Jump Game II | Greedy with levels | ★ |
| 125 | Gas Station | Track total and current surplus | ★ |
| 126 | Hand of Straights | Sort + greedy consume | ★ |

### Maximum Subarray (Kadane's Algorithm)

```python
def max_subarray(nums):
    max_sum = curr_sum = nums[0]
    
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    
    return max_sum
```

**Greedy choice:** If current sum is negative, start fresh from current element.

### Jump Game

```python
def can_jump(nums):
    max_reach = 0
    
    for i in range(len(nums)):
        if i > max_reach:
            return False  # can't reach i
        max_reach = max(max_reach, i + nums[i])
    
    return True
```

### Revision Checklist

- [ ] Can solve Maximum Subarray in under 2 minutes
- [ ] Understand why greedy works for Jump Game

---

## 16. Intervals

### Core Concepts

**Interval:** `[start, end]` representing a range.

**Key technique:** SORT FIRST (usually by start time).

### Problems & Patterns (6 total)

| # | Problem | Pattern | Priority |
|---|---------|---------|----------|
| 127 | Insert Interval | Linear scan + merge | ★★ |
| 128 | Merge Intervals | Sort + linear scan | ★★★ |
| 129 | Non-overlapping Intervals | Sort by end, greedy | ★★ |
| 130 | Meeting Rooms | Sort + check overlaps | ★ |
| 131 | Meeting Rooms II | Sort + heap OR sweep line | ★★★ |
| 132 | Minimum Interval to Include Query | Sort + heap | ★ |

### Merge Intervals

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  # overlaps
            last[1] = max(last[1], current[1])  # extend
        else:
            merged.append(current)  # no overlap
    
    return merged
```

### Meeting Rooms II (Min Rooms Needed)

```python
import heapq

def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[0])
    heap = []  # stores end times of ongoing meetings
    
    for start, end in intervals:
        # If earliest ending meeting ends before current starts
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # reuse room
        heapq.heappush(heap, end)
    
    return len(heap)  # heap size = rooms needed
```

### Common Mistakes

- ❌ Not sorting intervals first
- ❌ Comparing wrong values (start vs end)
- ✅ Remember to handle edge case: empty intervals

### Revision Checklist

- [ ] Can solve Merge Intervals from memory
- [ ] Understand Meeting Rooms II heap approach

---

## 17. Math & Geometry

### Problems & Patterns (8 total)

| # | Problem | Technique | Priority |
|---|---------|-----------|----------|
| 133 | Rotate Image | Transpose + reverse rows | ★★ |
| 134 | Spiral Matrix | Layer by layer | ★ |
| 135 | Set Matrix Zeroes | First row/col as markers | ★ |
| 136 | Happy Number | Cycle detection (slow/fast) | ★ |
| 137 | Plus One | Handle carry | ★ |
| 138 | Pow(x, n) | Binary exponentiation | ★★ |
| 139 | Multiply Strings | Grade-school multiplication | ★ |
| 140 | Detect Squares | Hash map of points | ★ |

### Rotate Image (90° Clockwise)

```python
def rotate(matrix):
    n = len(matrix)
    
    # Transpose
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reverse each row
    for row in matrix:
        row.reverse()
```

### Pow(x, n) — Binary Exponentiation

```python
def my_pow(x, n):
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n
    
    result = 1
    while n:
        if n % 2 == 1:
            result *= x
        x *= x
        n //= 2
    
    return result
```

**Why O(log n)?** We square x and halve n each iteration.

### Revision Checklist

- [ ] Can rotate matrix in-place
- [ ] Understand binary exponentiation

---

## 18. Bit Manipulation

### Core Concepts

**Bitwise Operators:**
- `&` (AND), `|` (OR), `^` (XOR), `~` (NOT)
- `<<` (left shift = multiply by 2), `>>` (right shift = divide by 2)

**Key Properties:**
- `x ^ x = 0` (XOR with self is 0)
- `x ^ 0 = x` (XOR with 0 is identity)
- `x & (x-1)` removes lowest set bit

### Problems & Patterns (7 total)

| # | Problem | Technique | Priority |
|---|---------|-----------|----------|
| 141 | Single Number | XOR all elements | ★★ |
| 142 | Number of 1 Bits | Brian Kernighan's | ★ |
| 143 | Counting Bits | DP: dp[i] = dp[i>>1] + (i&1) | ★ |
| 144 | Reverse Bits | Shift and build | ★ |
| 145 | Missing Number | XOR or sum formula | ★★ |
| 146 | Sum of Two Integers | Bit manipulation (no +/-) | ★ |
| 147 | Reverse Integer | Math with overflow check | ★ |

### Single Number

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num  # duplicates cancel out
    return result
```

### Number of 1 Bits (Hamming Weight)

```python
def hamming_weight(n):
    count = 0
    while n:
        n &= (n - 1)  # remove lowest set bit
        count += 1
    return count
```

### Revision Checklist

- [ ] Know XOR properties (x^x=0, x^0=x)
- [ ] Understand Brian Kernighan's algorithm

---

## FINAL QUICK REFERENCE

### Time Complexity Cheat Sheet

| Complexity | n = 10⁶ Operations | Good For |
|------------|-------------------|----------|
| O(1) | 1 | Hash map lookup |
| O(log n) | 20 | Binary search |
| O(n) | 10⁶ | Single pass |
| O(n log n) | 2×10⁷ | Sorting, heap ops |
| O(n²) | 10¹² | Only if n ≤ 1000 |
| O(2ⁿ) | 2¹⁰⁰⁶ | Only if n ≤ 20 |

### Space Complexity Common Cases

- **O(1):** Two pointers, Kadane's, greedy with variables
- **O(n):** Hash map, stack, queue, 1-D DP
- **O(n²):** 2-D DP, adjacency matrix
- **O(h):** Tree recursion (h = height)

### Pattern Recognition Speed Guide

```
"Find pair/exists" → Hash Map/Set
"Sorted array" → Binary Search or Two Pointers
"Subarray/substring" → Sliding Window
"Tree traversal" → DFS/BFS
"Graph dependencies" → Topological Sort
"Count ways" → DP
"All combinations" → Backtracking
"Top K" → Heap
"Shortest path (unweighted)" → BFS
"Shortest path (weighted)" → Dijkstra
```

### Common Mistakes to Avoid

1. ❌ Not checking edge cases (empty input, single element)
2. ❌ Off-by-one errors in loops/indices
3. ❌ Modifying list while iterating over it
4. ❌ Comparing object identity (is) vs equality (==)
5. ❌ Forgetting to mark visited in graphs (infinite loop)
6. ❌ Not handling negative numbers in binary search
7. ❌ Using list for membership checks (use set!)
8. ❌ Forgetting to copy list/dict when needed

---

## Your Interview Day Checklist

**The Night Before:**
- [ ] Skim this entire guide (90 min max)
- [ ] Review pattern recognition tables
- [ ] Sleep 8 hours!

**1 Hour Before:**
- [ ] Solve one easy warmup problem (Two Sum or Valid Palindrome)
- [ ] Review the templates (BFS, DFS, Binary Search, Sliding Window)
- [ ] Deep breaths. You've solved 150 problems. You're ready.

**During the Interview:**
- [ ] Repeat the problem back to clarify
- [ ] Ask about edge cases (empty input? duplicates? range?)
- [ ] Explain your approach BEFORE coding
- [ ] State time/space complexity
- [ ] Test with an example
- [ ] Communicate throughout!

---

## Congratulations!

You've completed NeetCode 150. That puts you in the top 5% of interview candidates in terms of preparation. Now it's about execution:

- **Google/Microsoft coding rounds:** You're ready. You've seen every pattern they'll ask.
- **System design:** You have your guide (`03_SYSTEM_DESIGN_GUIDE.md`)
- **OOP/LLD:** You have your guide (`02_OOP_LLD_GUIDE.py`)

The hard work is done. Now go crush those interviews! 🚀

---

*Last updated: 2026-10-07*
*Total problems: 150 ✓*
*Total patterns: 18*
*Hours invested: ~200+*

You've got this, Omkar. 💪
