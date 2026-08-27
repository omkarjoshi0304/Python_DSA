"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          GOOGLE SWE III — COMPLETE DSA MASTER LIST                         ║
║          Omkar Joshi — Rollouts Supervision, Google Cloud                  ║
║                                                                            ║
║   Every data structure, every must-solve question, the exact algorithm,    ║
║   and the optimization technique. Complete this list = confident for       ║
║   the coding round.                                                        ║
║                                                                            ║
║   Total: 75 problems across 12 data structures                            ║
║   Priority: ★★★ = MUST solve | ★★ = HIGH value | ★ = Good to know        ║
╚══════════════════════════════════════════════════════════════════════════════╝

HOW TO USE THIS FILE:
1. Go through each data structure section in order
2. Understand the "WHEN TO USE" and "KEY OPERATIONS" first
3. Solve each problem yourself BEFORE reading the solution approach
4. Check off problems as you complete them
5. Re-solve starred (★★★) problems from memory before your interview

After completing this list you will be able to:
- Identify which data structure fits any problem in < 60 seconds
- Know the optimal algorithm for the 75 most common Google patterns
- Explain time/space complexity for every solution
- Handle follow-up optimization questions from the interviewer
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  1. ARRAYS & STRINGS                                                       ║
# ║  Foundation of everything. 30-40% of Google questions involve arrays.       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Ordered collection of elements stored in contiguous memory.
      Strings are just arrays of characters.

KEY OPERATIONS:
    Access by index    → O(1)
    Search             → O(n)        [O(log n) if sorted]
    Insert at end      → O(1)        [amortized for dynamic arrays]
    Insert at middle   → O(n)        [must shift elements]
    Delete             → O(n)        [must shift elements]

WHEN TO USE:
    - You need fast access by position
    - Data is naturally sequential
    - You need to iterate through all elements

PYTHON ESSENTIALS:
    arr = [1, 2, 3]
    arr.append(4)         # O(1) amortized
    arr.pop()             # O(1) remove last
    arr.pop(0)            # O(n) remove first — use deque instead!
    arr.sort()            # O(n log n) in-place
    sorted(arr)           # O(n log n) returns new list
    arr[::-1]             # reverse
    len(arr)              # O(1)
    arr[1:3]              # slicing O(k)
"""

ARRAY_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 1: Two Sum
    # ──────────────────────────────────────────────────────────────
    "Two Sum": {
        "leetcode": 1,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Given array of integers and target, return indices of two numbers that add up to target.",
        "brute_force": "Check every pair with nested loops → O(n²) time, O(1) space",
        "optimal_algorithm": "Hash Map (one-pass)",
        "technique": """
            For each number, calculate complement = target - num.
            Check if complement exists in hash map.
            If yes → return both indices.
            If no → store current number and its index in hash map.
        """,
        "optimal_complexity": "O(n) time, O(n) space",
        "why_it_works": "Hash map gives O(1) lookup, turning O(n) inner loop into O(1)",
        "edge_cases": ["Same element used twice", "Negative numbers", "Multiple valid pairs"],
        "google_follow_up": "What if the array is sorted? → Use two pointers, O(1) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 2: Best Time to Buy and Sell Stock
    # ──────────────────────────────────────────────────────────────
    "Best Time to Buy and Sell Stock": {
        "leetcode": 121,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Given stock prices by day, find max profit from one buy and one sell.",
        "brute_force": "Check every buy-sell pair → O(n²)",
        "optimal_algorithm": "Single pass — track minimum price so far",
        "technique": """
            Keep track of min_price seen so far.
            At each day: profit = price - min_price.
            Update max_profit if this profit is better.
            Update min_price if current price is lower.
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "why_it_works": "To maximize profit, you always want to buy at the lowest point BEFORE the current day",
        "edge_cases": ["Prices only decrease (return 0)", "All same price", "Only 1 day"],
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 3: Product of Array Except Self
    # ──────────────────────────────────────────────────────────────
    "Product of Array Except Self": {
        "leetcode": 238,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Return array where each element is the product of all OTHER elements. No division allowed.",
        "brute_force": "For each element, multiply all others → O(n²)",
        "optimal_algorithm": "Prefix and Suffix products",
        "technique": """
            Pass 1 (left to right): build prefix products
                prefix[i] = product of all elements to the LEFT of i
            Pass 2 (right to left): multiply by suffix products
                suffix[i] = product of all elements to the RIGHT of i
            result[i] = prefix[i] * suffix[i]
        """,
        "optimal_complexity": "O(n) time, O(1) space (output array doesn't count)",
        "why_it_works": "product_except_self[i] = (everything left of i) × (everything right of i)",
        "edge_cases": ["Array contains zero", "Array contains multiple zeros", "Negative numbers"],
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 4: Maximum Subarray (Kadane's Algorithm)
    # ──────────────────────────────────────────────────────────────
    "Maximum Subarray": {
        "leetcode": 53,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find the contiguous subarray with the largest sum.",
        "brute_force": "Check all subarrays → O(n²)",
        "optimal_algorithm": "Kadane's Algorithm",
        "technique": """
            current_sum = max(num, current_sum + num)
            → At each position: "Is it better to extend the previous
               subarray or start fresh from here?"
            If current_sum > max_sum: update max_sum
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "why_it_works": "If previous subarray sum is negative, it can only hurt. Start fresh.",
        "edge_cases": ["All negative numbers", "Single element", "All positive"],
        "google_follow_up": "Return the actual subarray, not just the sum → track start and end indices",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 5: Container With Most Water
    # ──────────────────────────────────────────────────────────────
    "Container With Most Water": {
        "leetcode": 11,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Given heights, find two lines that form a container holding the most water.",
        "brute_force": "Check every pair → O(n²)",
        "optimal_algorithm": "Two Pointers (from both ends)",
        "technique": """
            left = 0, right = len-1
            area = min(height[left], height[right]) * (right - left)
            Move the SHORTER pointer inward.
            Why? Moving the taller one can never increase area
            (width shrinks, height still limited by shorter wall).
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "why_it_works": "Greedy: start wide, only move the pointer that COULD find a better answer",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 6: Merge Intervals
    # ──────────────────────────────────────────────────────────────
    "Merge Intervals": {
        "leetcode": 56,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Given list of intervals, merge all overlapping intervals.",
        "brute_force": "Compare every pair → O(n²)",
        "optimal_algorithm": "Sort + Linear Scan",
        "technique": """
            1. Sort intervals by start time
            2. Initialize merged = [first interval]
            3. For each interval:
               If it overlaps with last merged (start <= last_end):
                   Extend last merged's end = max(last_end, current_end)
               Else:
                   Add as new interval
        """,
        "optimal_complexity": "O(n log n) time [sorting], O(n) space",
        "why_it_works": "After sorting by start, overlapping intervals are adjacent. One pass merges them.",
        "edge_cases": ["No overlaps", "All overlap into one", "Nested intervals [1,10],[2,3]"],
        "google_follow_up": "Insert a new interval into sorted non-overlapping list → LC 57",
        "role_relevance": "ROLLOUTS: merge overlapping maintenance windows or deployment windows",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 7: Trapping Rain Water
    # ──────────────────────────────────────────────────────────────
    "Trapping Rain Water": {
        "leetcode": 42,
        "priority": "★★",
        "difficulty": "Hard",
        "problem": "Given elevation map, compute how much water can be trapped.",
        "brute_force": "For each position, find max_left and max_right → O(n²)",
        "optimal_algorithm": "Two Pointers",
        "technique": """
            left, right pointers from both ends.
            Track left_max and right_max.
            Water at position = min(left_max, right_max) - height[i]
            Move the pointer with the smaller max inward.
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "why_it_works": "Water level at any point is determined by the shorter of the two tallest walls on each side",
        "alternative": "Prefix max arrays: O(n) time, O(n) space — easier to understand",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 8: Valid Anagram
    # ──────────────────────────────────────────────────────────────
    "Valid Anagram": {
        "leetcode": 242,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Are two strings anagrams of each other?",
        "brute_force": "Sort both and compare → O(n log n)",
        "optimal_algorithm": "Character frequency count (Hash Map / Counter)",
        "technique": """
            from collections import Counter
            return Counter(s) == Counter(t)

            OR manual: count chars in s (+1), subtract chars in t (-1),
            check all counts are 0.
        """,
        "optimal_complexity": "O(n) time, O(1) space (fixed 26 lowercase chars)",
        "google_follow_up": "What if inputs contain Unicode? → Use hash map, space becomes O(n)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 9: Longest Consecutive Sequence
    # ──────────────────────────────────────────────────────────────
    "Longest Consecutive Sequence": {
        "leetcode": 128,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find length of longest consecutive element sequence. Must be O(n).",
        "brute_force": "Sort and scan → O(n log n)",
        "optimal_algorithm": "Hash Set + Smart Iteration",
        "technique": """
            Put all numbers in a set.
            For each number: only start counting if (num - 1) NOT in set
            (this means num is the START of a sequence).
            Then count up: num+1, num+2, ... while they exist in set.
        """,
        "optimal_complexity": "O(n) time, O(n) space",
        "why_it_works": "By only starting from sequence beginnings, each number is visited at most twice",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 10: Subarray Sum Equals K
    # ──────────────────────────────────────────────────────────────
    "Subarray Sum Equals K": {
        "leetcode": 560,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Find total number of contiguous subarrays whose sum equals k.",
        "brute_force": "Check all subarrays → O(n²)",
        "optimal_algorithm": "Prefix Sum + Hash Map",
        "technique": """
            prefix_sum = running sum as you iterate
            If prefix_sum - k exists in hash map, then there's a subarray
            summing to k ending at current position.

            Store: {prefix_sum: count of times we've seen it}
            Initialize: {0: 1} (empty prefix has sum 0)
        """,
        "optimal_complexity": "O(n) time, O(n) space",
        "why_it_works": "sum(i..j) = prefix[j] - prefix[i-1]. If prefix[j] - k = prefix[i-1], then sum(i..j) = k",
        "role_relevance": "ROLLOUTS: finding time windows where error count hits a threshold",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  2. HASH MAPS & HASH SETS                                                  ║
# ║  The single most useful data structure at Google interviews.                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Key-value store with O(1) average lookup, insert, delete.
      Hash Set is a Hash Map where you only care about keys (existence).

KEY OPERATIONS:
    Insert (dict[key] = val)   → O(1) average
    Lookup (key in dict)       → O(1) average
    Delete (del dict[key])     → O(1) average
    Iterate all keys           → O(n)

WHEN TO USE:
    - "Have I seen this before?"           → Hash Set
    - "How many times have I seen this?"   → Hash Map (Counter)
    - "Map this to that"                   → Hash Map
    - "Group things by property"           → defaultdict(list)
    - Need to reduce O(n) lookup to O(1)   → Hash Set/Map

PYTHON ESSENTIALS:
    d = {}                              # empty dict
    d = defaultdict(list)               # auto-creates empty list for new keys
    d = defaultdict(int)                # auto-creates 0 for new keys
    Counter("aabbc")                    # {'a': 2, 'b': 2, 'c': 1}
    s = set()                           # empty set
    s.add(x)                            # add element
    x in s                              # O(1) membership test
    s1 & s2, s1 | s2, s1 - s2          # intersection, union, difference
"""

HASHMAP_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 11: Group Anagrams
    # ──────────────────────────────────────────────────────────────
    "Group Anagrams": {
        "leetcode": 49,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Group strings that are anagrams of each other.",
        "brute_force": "Compare every pair → O(n² * k) where k = string length",
        "optimal_algorithm": "Hash Map with sorted string as key",
        "technique": """
            from collections import defaultdict
            groups = defaultdict(list)
            for s in strs:
                key = tuple(sorted(s))  # "eat" → ('a','e','t')
                groups[key].append(s)
            return list(groups.values())
        """,
        "optimal_complexity": "O(n * k log k) time, O(n * k) space",
        "optimization": "Instead of sorting, use character count tuple as key → O(n * k) time",
        "optimization_code": """
            key = tuple(Counter(s).items())  # or count array of 26 chars
        """,
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 12: Top K Frequent Elements
    # ──────────────────────────────────────────────────────────────
    "Top K Frequent Elements": {
        "leetcode": 347,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Return the k most frequent elements.",
        "brute_force": "Count frequencies, sort by frequency → O(n log n)",
        "optimal_algorithm": "Bucket Sort (best) or Heap",
        "technique": """
            BUCKET SORT approach:
            1. Count frequencies with Counter → O(n)
            2. Create buckets where index = frequency
               buckets[freq] = [elements with that frequency]
            3. Walk buckets from highest to lowest, collect k elements

            HEAP approach:
            1. Count frequencies → O(n)
            2. Use min-heap of size k → O(n log k)
               heapq.nlargest(k, count.keys(), key=count.get)
        """,
        "optimal_complexity": "O(n) time with bucket sort, O(n) space",
        "google_follow_up": "What if data is streaming? → Min-heap of size k, O(n log k)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 13: LRU Cache
    # ──────────────────────────────────────────────────────────────
    "LRU Cache": {
        "leetcode": 146,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Design a cache with O(1) get and put, evicting least recently used.",
        "optimal_algorithm": "Hash Map + Doubly Linked List",
        "technique": """
            Hash Map: key → node (for O(1) lookup)
            Doubly Linked List: maintains access order
                - Most recent at head
                - Least recent at tail

            get(key): move node to head, return value
            put(key, val):
                If exists: update value, move to head
                If new: add to head
                If over capacity: remove tail node + its hash map entry
        """,
        "optimal_complexity": "O(1) for both get and put",
        "python_shortcut": "OrderedDict does this built-in, but interviewers want manual implementation",
        "role_relevance": "ROLLOUTS: caching service health status, config lookups",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  3. TWO POINTERS                                                           ║
# ║  Technique (not a data structure) — but critical for Google.                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Use two variables (pointers) that traverse data, usually from
      opposite ends moving toward each other, or both from the start
      at different speeds.

WHEN TO USE:
    - Sorted array + finding pair/triplet       → opposite ends
    - Linked list + cycle detection              → slow/fast pointers
    - Removing duplicates in-place               → read/write pointers
    - Comparing/merging two sequences             → one pointer each

PATTERNS:
    Pattern A: left=0, right=end, move toward each other
    Pattern B: slow pointer, fast pointer (different speeds)
    Pattern C: read pointer + write pointer (in-place modification)
"""

TWO_POINTER_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 14: 3Sum
    # ──────────────────────────────────────────────────────────────
    "3Sum": {
        "leetcode": 15,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find all unique triplets that sum to zero.",
        "brute_force": "Three nested loops → O(n³)",
        "optimal_algorithm": "Sort + Fix one + Two Pointers for remaining two",
        "technique": """
            1. Sort the array → O(n log n)
            2. For each number i (fix it):
                 - Skip if same as previous (avoid duplicates)
                 - left = i+1, right = end
                 - If sum < 0: left++ (need bigger)
                 - If sum > 0: right-- (need smaller)
                 - If sum == 0: record, skip duplicates, move both
        """,
        "optimal_complexity": "O(n²) time, O(1) space (excluding output)",
        "why_it_works": "Sorting lets two pointers narrow the search space systematically",
        "edge_cases": ["All zeros [0,0,0]", "No valid triplets", "Duplicate handling"],
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 15: Valid Palindrome
    # ──────────────────────────────────────────────────────────────
    "Valid Palindrome": {
        "leetcode": 125,
        "priority": "★★",
        "difficulty": "Easy",
        "problem": "Is string a palindrome, considering only alphanumeric chars?",
        "optimal_algorithm": "Two Pointers from both ends",
        "technique": """
            left = 0, right = len-1
            Skip non-alphanumeric chars
            Compare s[left].lower() vs s[right].lower()
            If mismatch → False
            If pointers cross → True
        """,
        "optimal_complexity": "O(n) time, O(1) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 16: Move Zeroes
    # ──────────────────────────────────────────────────────────────
    "Move Zeroes": {
        "leetcode": 283,
        "priority": "★★",
        "difficulty": "Easy",
        "problem": "Move all zeros to end of array in-place, maintaining order.",
        "optimal_algorithm": "Read/Write two pointers",
        "technique": """
            write = 0  (where to place next non-zero)
            for read in range(n):
                if nums[read] != 0:
                    nums[write], nums[read] = nums[read], nums[write]
                    write += 1
        """,
        "optimal_complexity": "O(n) time, O(1) space",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  4. SLIDING WINDOW                                                          ║
# ║  Technique for subarray/substring optimization problems.                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: A window (subarray/substring) that expands and contracts
      as you iterate. Avoids recalculating everything from scratch.

WHEN TO USE:
    - "Find longest/shortest subarray/substring with property X"
    - "Find subarray with sum/count = K"
    - Contiguous elements with some constraint

TEMPLATE:
    left = 0
    for right in range(n):
        # ADD element at right to window state
        while WINDOW_IS_INVALID:
            # REMOVE element at left from window state
            left += 1
        # UPDATE answer (window [left..right] is valid)

TWO TYPES:
    Fixed size: window is always size k
    Variable size: window grows/shrinks based on condition
"""

SLIDING_WINDOW_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 17: Longest Substring Without Repeating Characters
    # ──────────────────────────────────────────────────────────────
    "Longest Substring Without Repeating Characters": {
        "leetcode": 3,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find length of longest substring without repeating characters.",
        "brute_force": "Check all substrings → O(n³)",
        "optimal_algorithm": "Sliding Window + Hash Set",
        "technique": """
            Expand right pointer, add chars to set.
            If duplicate found: shrink from left until no duplicate.
            Track max window size.

            Optimization: use hash map {char: last_index}
            to jump left pointer directly instead of shrinking one-by-one.
        """,
        "optimal_complexity": "O(n) time, O(min(n, alphabet_size)) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 18: Minimum Window Substring
    # ──────────────────────────────────────────────────────────────
    "Minimum Window Substring": {
        "leetcode": 76,
        "priority": "★★★",
        "difficulty": "Hard",
        "problem": "Find smallest substring of s containing all chars of t.",
        "brute_force": "Check all substrings → O(n²)",
        "optimal_algorithm": "Sliding Window + Two Counters",
        "technique": """
            1. Count required chars with Counter(t)
            2. Expand right: add char, update window count
            3. Track 'formed': how many unique chars meet required count
            4. When all chars met: shrink from left to minimize
            5. Track best (smallest) valid window
        """,
        "optimal_complexity": "O(n + m) time, O(n + m) space",
        "why_it_works": "Once window is valid, shrinking from left finds the minimum; then continue expanding",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 19: Longest Repeating Character Replacement
    # ──────────────────────────────────────────────────────────────
    "Longest Repeating Character Replacement": {
        "leetcode": 424,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Longest substring where you can replace at most k chars to make all same.",
        "optimal_algorithm": "Sliding Window + Frequency Count",
        "technique": """
            Window is valid if: window_size - max_frequency <= k
            (chars to replace = window size - count of most common char)

            Expand right, track char frequencies.
            If invalid: shrink from left.
            Key insight: max_frequency never needs to decrease —
            we only care about LONGER valid windows.
        """,
        "optimal_complexity": "O(n) time, O(1) space (26 chars max)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 20: Sliding Window Maximum
    # ──────────────────────────────────────────────────────────────
    "Sliding Window Maximum": {
        "leetcode": 239,
        "priority": "★★",
        "difficulty": "Hard",
        "problem": "Find max in each sliding window of size k.",
        "brute_force": "For each window, find max → O(n*k)",
        "optimal_algorithm": "Monotonic Deque",
        "technique": """
            Maintain a deque of indices in decreasing order of values.
            For each element:
            1. Remove indices outside window (left side of deque)
            2. Remove indices of smaller elements (right side of deque)
            3. Add current index
            4. deque[0] is always the max of current window
        """,
        "optimal_complexity": "O(n) time, O(k) space",
        "why_it_works": "Smaller elements before a larger one can never be the window max — discard them",
        "role_relevance": "ROLLOUTS: finding peak error rates in sliding time windows",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  5. BINARY SEARCH                                                           ║
# ║  Essential technique — not just for sorted arrays.                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Divide search space in half each step → O(log n).

WHEN TO USE:
    - Sorted array: find element, boundary, insertion point
    - Answer space: "What's the minimum/maximum X such that condition holds?"
    - Monotonic function: if f(x) is True for x >= k, find k

TWO TEMPLATES:

Template A — Find exact value:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1

Template B — Find boundary (leftmost True):
    left, right = lo, hi
    while left < right:
        mid = (left + right) // 2
        if condition(mid):
            right = mid       # mid might be answer, search left
        else:
            left = mid + 1    # mid too small, search right
    return left
"""

BINARY_SEARCH_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 21: Search in Rotated Sorted Array
    # ──────────────────────────────────────────────────────────────
    "Search in Rotated Sorted Array": {
        "leetcode": 33,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Search target in a sorted array that was rotated at some pivot.",
        "optimal_algorithm": "Modified Binary Search",
        "technique": """
            At each step, ONE half is always sorted.
            1. Find mid
            2. Determine which half is sorted:
               If nums[left] <= nums[mid]: left half is sorted
               Else: right half is sorted
            3. Check if target is in the sorted half:
               If yes: search there
               If no: search the other half
        """,
        "optimal_complexity": "O(log n) time, O(1) space",
        "why_it_works": "Even though array is rotated, one half is always properly sorted",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 22: Find Minimum in Rotated Sorted Array
    # ──────────────────────────────────────────────────────────────
    "Find Minimum in Rotated Sorted Array": {
        "leetcode": 153,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Find the minimum element in a rotated sorted array.",
        "optimal_algorithm": "Binary Search",
        "technique": """
            If nums[mid] > nums[right]: min is in right half → left = mid + 1
            Else: min is in left half (including mid) → right = mid
        """,
        "optimal_complexity": "O(log n) time, O(1) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 23: Koko Eating Bananas (Binary Search on Answer)
    # ──────────────────────────────────────────────────────────────
    "Koko Eating Bananas": {
        "leetcode": 875,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find minimum eating speed to finish all banana piles in h hours.",
        "optimal_algorithm": "Binary Search on Answer Space",
        "technique": """
            Answer space: speed can be 1 to max(piles)
            For each candidate speed: can she finish in h hours?
                hours_needed = sum(ceil(pile / speed) for pile in piles)
            Binary search for minimum speed where hours_needed <= h
        """,
        "optimal_complexity": "O(n log m) time where m = max(piles), O(1) space",
        "why_it_works": "If speed k works, all speeds > k also work. Monotonic → binary search.",
        "role_relevance": "ROLLOUTS: binary search on rollout parameters (batch size, rate limit)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 24: Search a 2D Matrix
    # ──────────────────────────────────────────────────────────────
    "Search a 2D Matrix": {
        "leetcode": 74,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Search for value in row-sorted, column-sorted 2D matrix.",
        "optimal_algorithm": "Treat as 1D sorted array",
        "technique": """
            Treat the m×n matrix as a sorted array of length m*n.
            Binary search on index 0..m*n-1.
            Convert index to row,col: row = idx // n, col = idx % n
        """,
        "optimal_complexity": "O(log(m*n)) time, O(1) space",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  6. STACKS                                                                  ║
# ║  Last-In-First-Out. Perfect for matching, nesting, "next greater" problems. ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: LIFO (Last In, First Out) data structure.

KEY OPERATIONS:
    Push     → O(1)
    Pop      → O(1)
    Peek     → O(1)
    isEmpty  → O(1)

WHEN TO USE:
    - Matching brackets/parentheses
    - "Next greater/smaller element" → Monotonic Stack
    - Undo/redo operations
    - Expression evaluation
    - DFS (iterative)
    - Function call tracking

PYTHON: Just use a list
    stack = []
    stack.append(x)    # push
    stack.pop()        # pop (returns element)
    stack[-1]          # peek
    len(stack) == 0    # isEmpty
"""

STACK_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 25: Valid Parentheses
    # ──────────────────────────────────────────────────────────────
    "Valid Parentheses": {
        "leetcode": 20,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Check if brackets string is valid: ()[]{} ",
        "optimal_algorithm": "Stack",
        "technique": """
            Push opening brackets onto stack.
            For closing bracket: check if top of stack is matching opener.
            If yes: pop. If no or stack empty: invalid.
            At end: stack must be empty.

            mapping = {')': '(', ']': '[', '}': '{'}
        """,
        "optimal_complexity": "O(n) time, O(n) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 26: Daily Temperatures
    # ──────────────────────────────────────────────────────────────
    "Daily Temperatures": {
        "leetcode": 739,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "For each day, find how many days until a warmer temperature.",
        "brute_force": "For each day, scan forward → O(n²)",
        "optimal_algorithm": "Monotonic Stack (decreasing)",
        "technique": """
            Stack stores INDICES of temperatures in decreasing order.
            For each new temperature:
                While stack top is COOLER than current:
                    Pop it — current day is its answer
                    result[popped_index] = current_index - popped_index
                Push current index
        """,
        "optimal_complexity": "O(n) time, O(n) space",
        "why_it_works": "Each element is pushed and popped at most once → amortized O(n)",
        "role_relevance": "ROLLOUTS: 'How long until metric recovers above threshold?'",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 27: Min Stack
    # ──────────────────────────────────────────────────────────────
    "Min Stack": {
        "leetcode": 155,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Design a stack that supports push, pop, top, and getMin in O(1).",
        "optimal_algorithm": "Two stacks: main stack + min-tracking stack",
        "technique": """
            Main stack: normal push/pop
            Min stack: push current minimum when main stack pushes
                       pop when main stack pops
            getMin: peek at min stack

            Key: min stack's top always reflects minimum of current stack state
        """,
        "optimal_complexity": "O(1) for all operations",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 28: Largest Rectangle in Histogram
    # ──────────────────────────────────────────────────────────────
    "Largest Rectangle in Histogram": {
        "leetcode": 84,
        "priority": "★★",
        "difficulty": "Hard",
        "problem": "Find the area of largest rectangle in histogram.",
        "optimal_algorithm": "Monotonic Stack (increasing)",
        "technique": """
            Stack stores indices in increasing order of heights.
            For each bar:
                While current bar is shorter than stack top:
                    Pop — this bar's max rectangle ends here
                    Width = current_index - new_stack_top - 1
                    Area = popped_height * width
                Push current index
            Process remaining stack elements
        """,
        "optimal_complexity": "O(n) time, O(n) space",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  7. QUEUES & DEQUES                                                         ║
# ║  First-In-First-Out. Foundation for BFS.                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: FIFO (First In, First Out) data structure.
      Deque = Double-Ended Queue (efficient at both ends).

KEY OPERATIONS:
    Queue:
        enqueue (add to back)   → O(1)
        dequeue (remove front)  → O(1)
    Deque:
        append/appendleft       → O(1)
        pop/popleft             → O(1)

WHEN TO USE:
    - BFS traversal (always!)
    - Level-order processing
    - Sliding window maximum (monotonic deque)
    - Task scheduling / FIFO processing

PYTHON:
    from collections import deque
    q = deque()
    q.append(x)       # add to right  → O(1)
    q.appendleft(x)   # add to left   → O(1)
    q.pop()            # remove right  → O(1)
    q.popleft()        # remove left   → O(1)

    NEVER use list.pop(0) — it's O(n)! Always use deque.popleft()
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  8. LINKED LISTS                                                            ║
# ║  Pointer-based sequential storage.                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Chain of nodes, each pointing to the next (and optionally previous).

KEY OPERATIONS:
    Access by index    → O(n)  [must traverse]
    Insert at head     → O(1)
    Insert at position → O(n) search + O(1) insert
    Delete             → O(n) search + O(1) delete

WHEN TO USE:
    - Frequent insertions/deletions at known positions
    - When you don't need random access
    - Building LRU Cache (doubly linked list)
    - Interview questions testing pointer manipulation

NODE DEFINITION:
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
"""

LINKED_LIST_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 29: Reverse Linked List
    # ──────────────────────────────────────────────────────────────
    "Reverse Linked List": {
        "leetcode": 206,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Reverse a singly linked list.",
        "optimal_algorithm": "Iterative — three pointers",
        "technique": """
            prev = None, curr = head
            While curr:
                next_temp = curr.next     # save next
                curr.next = prev          # reverse pointer
                prev = curr               # advance prev
                curr = next_temp          # advance curr
            return prev                   # new head
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "google_follow_up": "Reverse in groups of k → LC 25 (Hard)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 30: Merge Two Sorted Lists
    # ──────────────────────────────────────────────────────────────
    "Merge Two Sorted Lists": {
        "leetcode": 21,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Merge two sorted linked lists into one sorted list.",
        "optimal_algorithm": "Dummy head + compare and link",
        "technique": """
            dummy = ListNode(0)    # dummy head simplifies edge cases
            curr = dummy
            While both lists have nodes:
                Link the smaller node to curr
                Advance that list's pointer
            Link remaining nodes
            return dummy.next
        """,
        "optimal_complexity": "O(n + m) time, O(1) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 31: Linked List Cycle
    # ──────────────────────────────────────────────────────────────
    "Linked List Cycle": {
        "leetcode": 141,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Detect if a linked list has a cycle.",
        "optimal_algorithm": "Floyd's Tortoise and Hare (slow/fast pointers)",
        "technique": """
            slow moves 1 step, fast moves 2 steps.
            If cycle exists: they will meet.
            If no cycle: fast reaches None.

            To find cycle START (LC 142):
            After meeting, reset one pointer to head.
            Move both 1 step at a time. They meet at cycle start.
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "why_it_works": "In a cycle, fast gains 1 step per iteration. Eventually catches slow.",
        "role_relevance": "ROLLOUTS: detecting circular dependencies in service deployments",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 32: Merge K Sorted Lists
    # ──────────────────────────────────────────────────────────────
    "Merge K Sorted Lists": {
        "leetcode": 23,
        "priority": "★★",
        "difficulty": "Hard",
        "problem": "Merge k sorted linked lists into one sorted list.",
        "brute_force": "Merge two at a time → O(kN) where N = total nodes",
        "optimal_algorithm": "Min Heap (Priority Queue)",
        "technique": """
            import heapq
            Push the head of each list into a min-heap.
            Pop smallest, add to result.
            Push popped node's next into heap.
            Repeat until heap is empty.
        """,
        "optimal_complexity": "O(N log k) time, O(k) space",
        "alternative": "Divide and conquer merge (like merge sort) → same complexity",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  9. TREES                                                                   ║
# ║  Hierarchical data. Google LOVES tree problems.                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Hierarchical structure. Binary tree = each node has at most 2 children.
      BST = Binary Search Tree: left < root < right.

KEY OPERATIONS (BST):
    Search    → O(log n) average, O(n) worst (skewed)
    Insert    → O(log n) average
    Delete    → O(log n) average

TRAVERSALS (must know all):
    Inorder   (Left, Root, Right)   → sorted order for BST
    Preorder  (Root, Left, Right)   → copy/serialize tree
    Postorder (Left, Right, Root)   → delete tree, calculate sizes
    Level-order (BFS)               → process level by level

WHEN TO USE:
    - Hierarchical data (org chart, file system, service dependencies)
    - BST: when you need sorted data with fast search
    - Trie: prefix matching, autocomplete

RECURSIVE TEMPLATE:
    def solve(node):
        if not node:
            return BASE_CASE

        left_result = solve(node.left)
        right_result = solve(node.right)

        return COMBINE(node.val, left_result, right_result)
"""

TREE_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 33: Maximum Depth of Binary Tree
    # ──────────────────────────────────────────────────────────────
    "Maximum Depth of Binary Tree": {
        "leetcode": 104,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Find the maximum depth (height) of a binary tree.",
        "optimal_algorithm": "DFS Recursion",
        "technique": """
            def maxDepth(node):
                if not node: return 0
                return 1 + max(maxDepth(node.left), maxDepth(node.right))
        """,
        "optimal_complexity": "O(n) time, O(h) space (h = height, recursion stack)",
        "alternative": "BFS level-order: count levels → O(n) time, O(w) space (w = max width)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 34: Invert Binary Tree
    # ──────────────────────────────────────────────────────────────
    "Invert Binary Tree": {
        "leetcode": 226,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "Mirror/invert a binary tree.",
        "optimal_algorithm": "DFS Recursion — swap children",
        "technique": """
            def invertTree(node):
                if not node: return None
                node.left, node.right = node.right, node.left
                invertTree(node.left)
                invertTree(node.right)
                return node
        """,
        "optimal_complexity": "O(n) time, O(h) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 35: Binary Tree Level Order Traversal
    # ──────────────────────────────────────────────────────────────
    "Binary Tree Level Order Traversal": {
        "leetcode": 102,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Return values level by level (BFS).",
        "optimal_algorithm": "BFS with Queue",
        "technique": """
            queue = deque([root])
            result = []
            while queue:
                level_size = len(queue)       # nodes at this level
                level = []
                for _ in range(level_size):
                    node = queue.popleft()
                    level.append(node.val)
                    if node.left:  queue.append(node.left)
                    if node.right: queue.append(node.right)
                result.append(level)
        """,
        "optimal_complexity": "O(n) time, O(n) space",
        "role_relevance": "ROLLOUTS: processing deployment stages level by level",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 36: Validate Binary Search Tree
    # ──────────────────────────────────────────────────────────────
    "Validate Binary Search Tree": {
        "leetcode": 98,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Check if a binary tree is a valid BST.",
        "optimal_algorithm": "DFS with min/max bounds",
        "technique": """
            def isValidBST(node, low=-inf, high=inf):
                if not node: return True
                if node.val <= low or node.val >= high:
                    return False
                return (isValidBST(node.left, low, node.val) and
                        isValidBST(node.right, node.val, high))
        """,
        "optimal_complexity": "O(n) time, O(h) space",
        "common_mistake": "Only checking left < root < right for immediate children. Must check ALL ancestors.",
        "alternative": "Inorder traversal must produce strictly increasing sequence",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 37: Lowest Common Ancestor
    # ──────────────────────────────────────────────────────────────
    "Lowest Common Ancestor of BST": {
        "leetcode": 235,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find lowest common ancestor of two nodes in a BST.",
        "optimal_algorithm": "BST property exploitation",
        "technique": """
            If both nodes < root: LCA is in left subtree
            If both nodes > root: LCA is in right subtree
            Otherwise: root IS the LCA (split point)

            def lowestCommonAncestor(root, p, q):
                while root:
                    if p.val < root.val and q.val < root.val:
                        root = root.left
                    elif p.val > root.val and q.val > root.val:
                        root = root.right
                    else:
                        return root
        """,
        "optimal_complexity": "O(h) time, O(1) space",
        "variant": "LCA of Binary Tree (not BST) → LC 236: recursive DFS, O(n)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 38: Kth Smallest Element in BST
    # ──────────────────────────────────────────────────────────────
    "Kth Smallest Element in BST": {
        "leetcode": 230,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Find the kth smallest element in a BST.",
        "optimal_algorithm": "Inorder traversal (gives sorted order)",
        "technique": """
            Inorder traversal of BST = sorted order.
            Count nodes visited. When count == k, that's the answer.

            Iterative with stack (preferred — can stop early):
            stack = []
            while stack or root:
                while root:
                    stack.append(root)
                    root = root.left
                root = stack.pop()
                k -= 1
                if k == 0: return root.val
                root = root.right
        """,
        "optimal_complexity": "O(H + k) time, O(H) space where H = height",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 39: Binary Tree Maximum Path Sum
    # ──────────────────────────────────────────────────────────────
    "Binary Tree Maximum Path Sum": {
        "leetcode": 124,
        "priority": "★★",
        "difficulty": "Hard",
        "problem": "Find max sum path (doesn't need to pass through root).",
        "optimal_algorithm": "DFS — postorder with global max",
        "technique": """
            At each node, compute:
            1. Max gain from left subtree (0 if negative — don't take it)
            2. Max gain from right subtree (0 if negative)
            3. Path through this node = node.val + left_gain + right_gain
               → Update global max
            4. Return to parent: node.val + max(left_gain, right_gain)
               → Can only go one direction up to parent
        """,
        "optimal_complexity": "O(n) time, O(h) space",
        "why_it_works": "Each node considers: am I part of the best path? Return best single-direction path upward.",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 40: Serialize and Deserialize Binary Tree
    # ──────────────────────────────────────────────────────────────
    "Serialize and Deserialize Binary Tree": {
        "leetcode": 297,
        "priority": "★★",
        "difficulty": "Hard",
        "problem": "Convert tree to string and back.",
        "optimal_algorithm": "Preorder DFS with null markers",
        "technique": """
            Serialize: preorder DFS, use 'N' for null nodes
                "1,2,N,N,3,4,N,N,5,N,N"

            Deserialize: split by comma, use iterator/index
                Read value → create node
                Recurse left, then right
                'N' → return None
        """,
        "optimal_complexity": "O(n) for both operations",
        "role_relevance": "ROLLOUTS: serializing deployment state/config for transmission",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  10. GRAPHS                                                                 ║
# ║  MOST IMPORTANT for Rollouts Supervision — services are graphs.             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Nodes connected by edges. Can be directed/undirected, weighted/unweighted.

REPRESENTATIONS:
    Adjacency List: graph = {node: [neighbors]}    → O(V+E) space, preferred
    Adjacency Matrix: grid[i][j] = 1 if edge       → O(V²) space, dense graphs
    Edge List: [(u, v, weight), ...]                → O(E) space, for algorithms

KEY ALGORITHMS:
    BFS                  → Shortest path (unweighted), level-order
    DFS                  → Cycle detection, connected components, all paths
    Topological Sort     → Ordering with dependencies (CRITICAL for rollouts)
    Dijkstra             → Shortest path (weighted, non-negative)
    Union-Find           → Connected components, cycle detection (undirected)

WHEN TO USE:
    - Dependencies between services          → Directed graph
    - Network connectivity                   → Undirected graph
    - "Can I reach X from Y?"               → BFS/DFS
    - "What order to process?"              → Topological sort
    - "Are these connected?"                → Union-Find or BFS/DFS
    - "Shortest route?"                     → BFS (unweighted) / Dijkstra (weighted)
"""

GRAPH_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 41: Number of Islands
    # ──────────────────────────────────────────────────────────────
    "Number of Islands": {
        "leetcode": 200,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Count connected groups of '1's in a grid.",
        "optimal_algorithm": "BFS or DFS from each unvisited '1'",
        "technique": """
            For each cell with '1':
                count += 1
                BFS/DFS to mark all connected '1's as visited ('0')
            Return count

            BFS version with deque:
            queue = deque([(r, c)])
            while queue:
                row, col = queue.popleft()
                for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr, nc = row+dr, col+dc
                    if in_bounds and grid[nr][nc] == '1':
                        grid[nr][nc] = '0'
                        queue.append((nr, nc))
        """,
        "optimal_complexity": "O(m*n) time, O(m*n) space (queue worst case)",
        "role_relevance": "ROLLOUTS: finding isolated/disconnected service clusters",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 42: Clone Graph
    # ──────────────────────────────────────────────────────────────
    "Clone Graph": {
        "leetcode": 133,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Deep copy a graph.",
        "optimal_algorithm": "BFS/DFS with hash map (old → new node mapping)",
        "technique": """
            old_to_new = {}

            def clone(node):
                if node in old_to_new:
                    return old_to_new[node]
                copy = Node(node.val)
                old_to_new[node] = copy
                for neighbor in node.neighbors:
                    copy.neighbors.append(clone(neighbor))
                return copy
        """,
        "optimal_complexity": "O(V + E) time, O(V) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 43: Course Schedule (Cycle Detection)
    # ──────────────────────────────────────────────────────────────
    "Course Schedule": {
        "leetcode": 207,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Can all courses be finished given prerequisites? (Detect cycle in directed graph)",
        "optimal_algorithm": "DFS with 3-state coloring OR Kahn's Algorithm (BFS topological sort)",
        "technique": """
            DFS approach — 3 states per node:
            0 = unvisited, 1 = in current path, 2 = fully processed

            If we visit a node with state 1 → CYCLE (can't finish)

            Kahn's approach — BFS:
            Count in-degrees. Start with in-degree 0 nodes.
            Process: reduce neighbors' in-degree.
            If all processed → no cycle.
        """,
        "optimal_complexity": "O(V + E) time, O(V + E) space",
        "role_relevance": "DIRECTLY relevant — detecting circular dependencies in service rollouts",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 44: Course Schedule II (Topological Sort)
    # ──────────────────────────────────────────────────────────────
    "Course Schedule II": {
        "leetcode": 210,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Return valid order to take all courses (topological sort).",
        "optimal_algorithm": "Kahn's Algorithm (BFS-based topological sort)",
        "technique": """
            1. Build adjacency list + count in-degrees
            2. Queue all nodes with in-degree 0 (no prerequisites)
            3. Process queue:
               - Pop node, add to result
               - Reduce in-degree of all neighbors
               - If neighbor's in-degree becomes 0: add to queue
            4. If result has all nodes → valid order
               If not → cycle exists, impossible
        """,
        "optimal_complexity": "O(V + E) time, O(V + E) space",
        "role_relevance": "THIS IS THE ROLLOUTS PROBLEM — determining safe deployment order for dependent services",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 45: Pacific Atlantic Water Flow
    # ──────────────────────────────────────────────────────────────
    "Pacific Atlantic Water Flow": {
        "leetcode": 417,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Find cells where water can flow to both Pacific and Atlantic oceans.",
        "optimal_algorithm": "Multi-source BFS/DFS from ocean borders",
        "technique": """
            Instead of checking each cell → which ocean it reaches,
            REVERSE: start from each ocean, find which cells can reach it.

            BFS from Pacific border → set of reachable cells
            BFS from Atlantic border → set of reachable cells
            Answer = intersection
        """,
        "optimal_complexity": "O(m*n) time, O(m*n) space",
        "why_it_works": "Reversing the direction avoids redundant computation",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 46: Word Ladder
    # ──────────────────────────────────────────────────────────────
    "Word Ladder": {
        "leetcode": 127,
        "priority": "★★",
        "difficulty": "Hard",
        "problem": "Shortest transformation from beginWord to endWord, changing one letter at a time.",
        "optimal_algorithm": "BFS (shortest path in unweighted graph)",
        "technique": """
            Each word is a node. Edge exists if words differ by 1 letter.
            BFS from beginWord to endWord.

            Optimization: instead of comparing all word pairs O(n²),
            create pattern map: 'h*t' → ['hot', 'hat', 'hit']
            Each word generates len(word) patterns.
        """,
        "optimal_complexity": "O(n * m²) where n = words, m = word length",
        "optimization": "Bidirectional BFS → O(n * m) in practice",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 47: Graph Valid Tree
    # ──────────────────────────────────────────────────────────────
    "Graph Valid Tree": {
        "leetcode": 261,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Check if undirected graph is a valid tree (connected + no cycles).",
        "optimal_algorithm": "Union-Find OR DFS",
        "technique": """
            Tree conditions: n nodes, exactly n-1 edges, all connected.

            Union-Find approach:
            For each edge: union the two nodes.
            If they're already in the same set → CYCLE.
            At end: check if exactly 1 connected component.

            DFS approach:
            Start from node 0, visit all reachable nodes.
            If visited count == n and no cycles → valid tree.
        """,
        "optimal_complexity": "O(V + E) time",
        "role_relevance": "ROLLOUTS: validating service dependency graph structure",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  11. HEAPS (PRIORITY QUEUES)                                                ║
# ║  Efficient access to min/max element.                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Tree-based structure where parent is always smaller (min-heap)
      or larger (max-heap) than children.

KEY OPERATIONS:
    Insert          → O(log n)
    Extract min/max → O(log n)
    Peek min/max    → O(1)
    Build heap      → O(n)

WHEN TO USE:
    - "Find K largest/smallest"         → Min-heap of size k
    - "Find median of stream"           → Two heaps (max + min)
    - "Merge K sorted things"           → Min-heap
    - "Process by priority"             → Priority queue
    - "Next closest/smallest"           → Min-heap

PYTHON:
    import heapq                        # MIN-heap by default

    heapq.heappush(heap, val)          # push
    heapq.heappop(heap)                # pop smallest
    heap[0]                            # peek smallest

    # MAX-heap trick: negate values
    heapq.heappush(heap, -val)         # push negated
    -heapq.heappop(heap)              # pop and negate back

    heapq.nlargest(k, iterable)        # k largest
    heapq.nsmallest(k, iterable)       # k smallest
"""

HEAP_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 48: Kth Largest Element in Array
    # ──────────────────────────────────────────────────────────────
    "Kth Largest Element in Array": {
        "leetcode": 215,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find the kth largest element (not kth distinct).",
        "brute_force": "Sort and return nums[-k] → O(n log n)",
        "optimal_algorithm": "Min-heap of size k",
        "technique": """
            Maintain a min-heap of size k.
            For each element:
                If heap size < k: push it
                Else if element > heap[0]: replace heap top

            After processing all: heap[0] is kth largest.

            import heapq
            return heapq.nlargest(k, nums)[-1]
        """,
        "optimal_complexity": "O(n log k) time, O(k) space",
        "alternative": "Quickselect → O(n) average, O(n²) worst",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 49: Find Median from Data Stream
    # ──────────────────────────────────────────────────────────────
    "Find Median from Data Stream": {
        "leetcode": 295,
        "priority": "★★★",
        "difficulty": "Hard",
        "problem": "Design a structure that supports addNum and findMedian efficiently.",
        "optimal_algorithm": "Two Heaps (max-heap for lower half, min-heap for upper half)",
        "technique": """
            max_heap: stores smaller half (negate for max behavior)
            min_heap: stores larger half

            Balance: len difference <= 1

            addNum:
                Push to max_heap first (negate)
                Move max_heap top to min_heap (balance)
                If min_heap larger: move top back to max_heap

            findMedian:
                If same size: average of both tops
                If different: top of larger heap
        """,
        "optimal_complexity": "O(log n) add, O(1) median",
        "role_relevance": "ROLLOUTS: computing rolling median of latency metrics",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 50: Task Scheduler
    # ──────────────────────────────────────────────────────────────
    "Task Scheduler": {
        "leetcode": 621,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Find minimum intervals to execute tasks with cooldown between same tasks.",
        "optimal_algorithm": "Max-heap + Queue (for cooldown tracking)",
        "technique": """
            Greedy: always execute the task with highest remaining count.

            1. Count task frequencies
            2. Max-heap of frequencies
            3. Each tick: pop from heap, decrement, put in cooldown queue
            4. After cooldown expires: put back in heap
            5. Count total time ticks
        """,
        "optimal_complexity": "O(n) time where n = total tasks",
        "role_relevance": "ROLLOUTS: scheduling deployments with cooldown periods between services",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  12. DYNAMIC PROGRAMMING                                                    ║
# ║  The hardest pattern. Learn the recipe, not just the problems.              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Solving problems by breaking them into overlapping subproblems,
      solving each once, and storing results.

WHEN TO USE:
    - "Count the number of ways..."
    - "Find the minimum/maximum..."
    - "Is it possible to...?"  (where choices affect future choices)
    - "Find longest/shortest..."  (with dependencies between choices)
    - Problem has OPTIMAL SUBSTRUCTURE + OVERLAPPING SUBPROBLEMS

THE DP RECIPE (follow this every time):
    Step 1: Define state — what does dp[i] (or dp[i][j]) represent?
    Step 2: Find recurrence — dp[i] = f(dp[smaller values])
    Step 3: Set base cases — dp[0] = ???
    Step 4: Determine fill order — left to right? bottom to top?
    Step 5: Return answer — dp[n]? dp[-1]? max(dp)?

TWO APPROACHES:
    Top-down (memoization): recursion + cache → easier to think about
    Bottom-up (tabulation): fill table iteratively → usually faster

CATEGORIES:
    1D DP: dp[i] depends on dp[i-1], dp[i-2], etc.
    2D DP: dp[i][j] depends on dp[i-1][j], dp[i][j-1], etc.
    String DP: usually 2D, comparing two strings
    Decision DP: at each step, make a choice (take or skip)
"""

DP_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 51: Climbing Stairs
    # ──────────────────────────────────────────────────────────────
    "Climbing Stairs": {
        "leetcode": 70,
        "priority": "★★★",
        "difficulty": "Easy",
        "problem": "You can take 1 or 2 steps. How many ways to reach step n?",
        "state": "dp[i] = number of ways to reach step i",
        "recurrence": "dp[i] = dp[i-1] + dp[i-2]  (Fibonacci!)",
        "base_case": "dp[0] = 1, dp[1] = 1",
        "technique": """
            # Space-optimized: only need last two values
            prev2, prev1 = 1, 1
            for i in range(2, n + 1):
                current = prev1 + prev2
                prev2 = prev1
                prev1 = current
            return prev1
        """,
        "optimal_complexity": "O(n) time, O(1) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 52: House Robber
    # ──────────────────────────────────────────────────────────────
    "House Robber": {
        "leetcode": 198,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Max money robbing non-adjacent houses.",
        "state": "dp[i] = max money from first i houses",
        "recurrence": "dp[i] = max(dp[i-1], dp[i-2] + nums[i])  (skip or rob current)",
        "base_case": "dp[0] = nums[0], dp[1] = max(nums[0], nums[1])",
        "technique": """
            At each house: "Is it better to skip this house (keep dp[i-1])
            or rob it (dp[i-2] + current value)?"

            prev2, prev1 = 0, 0
            for num in nums:
                current = max(prev1, prev2 + num)
                prev2 = prev1
                prev1 = current
            return prev1
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "google_follow_up": "Houses in a circle (House Robber II, LC 213): run twice, exclude first or last",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 53: Coin Change
    # ──────────────────────────────────────────────────────────────
    "Coin Change": {
        "leetcode": 322,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Minimum coins to make amount.",
        "state": "dp[i] = minimum coins needed to make amount i",
        "recurrence": "dp[i] = min(dp[i - coin] + 1) for each coin",
        "base_case": "dp[0] = 0",
        "technique": """
            dp = [float('inf')] * (amount + 1)
            dp[0] = 0
            for i in range(1, amount + 1):
                for coin in coins:
                    if coin <= i:
                        dp[i] = min(dp[i], dp[i - coin] + 1)
            return dp[amount] if dp[amount] != float('inf') else -1
        """,
        "optimal_complexity": "O(amount * len(coins)) time, O(amount) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 54: Longest Increasing Subsequence
    # ──────────────────────────────────────────────────────────────
    "Longest Increasing Subsequence": {
        "leetcode": 300,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find length of longest strictly increasing subsequence.",
        "state": "dp[i] = length of LIS ending at index i",
        "recurrence": "dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]",
        "base_case": "dp[i] = 1 (every element is a subsequence of length 1)",
        "technique": """
            dp = [1] * len(nums)
            for i in range(1, len(nums)):
                for j in range(i):
                    if nums[j] < nums[i]:
                        dp[i] = max(dp[i], dp[j] + 1)
            return max(dp)
        """,
        "optimal_complexity": "O(n²) time, O(n) space",
        "optimization": "Binary search approach with patience sorting → O(n log n)",
        "role_relevance": "ROLLOUTS: finding longest chain of compatible version upgrades",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 55: Word Break
    # ──────────────────────────────────────────────────────────────
    "Word Break": {
        "leetcode": 139,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Can string be segmented into dictionary words?",
        "state": "dp[i] = True if s[:i] can be segmented",
        "recurrence": "dp[i] = any(dp[j] and s[j:i] in wordSet for j in range(i))",
        "base_case": "dp[0] = True (empty string)",
        "technique": """
            word_set = set(wordDict)
            dp = [False] * (len(s) + 1)
            dp[0] = True
            for i in range(1, len(s) + 1):
                for j in range(i):
                    if dp[j] and s[j:i] in word_set:
                        dp[i] = True
                        break
            return dp[len(s)]
        """,
        "optimal_complexity": "O(n² * m) time where m = max word length, O(n) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 56: Unique Paths
    # ──────────────────────────────────────────────────────────────
    "Unique Paths": {
        "leetcode": 62,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Count paths from top-left to bottom-right (only move right/down).",
        "state": "dp[i][j] = number of paths to reach cell (i, j)",
        "recurrence": "dp[i][j] = dp[i-1][j] + dp[i][j-1]  (from above + from left)",
        "base_case": "dp[0][j] = 1, dp[i][0] = 1  (only one way along edges)",
        "technique": """
            # Space optimization: only need previous row
            dp = [1] * n
            for i in range(1, m):
                for j in range(1, n):
                    dp[j] += dp[j-1]
            return dp[-1]
        """,
        "optimal_complexity": "O(m*n) time, O(n) space with optimization",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 57: Longest Common Subsequence
    # ──────────────────────────────────────────────────────────────
    "Longest Common Subsequence": {
        "leetcode": 1143,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find length of longest subsequence common to two strings.",
        "state": "dp[i][j] = LCS of text1[:i] and text2[:j]",
        "recurrence": """
            If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
            Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        """,
        "base_case": "dp[0][j] = 0, dp[i][0] = 0",
        "technique": """
            dp = [[0] * (n+1) for _ in range(m+1)]
            for i in range(1, m+1):
                for j in range(1, n+1):
                    if text1[i-1] == text2[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            return dp[m][n]
        """,
        "optimal_complexity": "O(m*n) time, O(m*n) space",
        "role_relevance": "ROLLOUTS: computing config diffs between versions",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 58: Edit Distance
    # ──────────────────────────────────────────────────────────────
    "Edit Distance": {
        "leetcode": 72,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Minimum insertions, deletions, replacements to convert word1 to word2.",
        "state": "dp[i][j] = min operations to convert word1[:i] to word2[:j]",
        "recurrence": """
            If chars match: dp[i][j] = dp[i-1][j-1]       (no operation needed)
            Else: dp[i][j] = 1 + min(
                dp[i-1][j],      # delete from word1
                dp[i][j-1],      # insert into word1
                dp[i-1][j-1]     # replace
            )
        """,
        "base_case": "dp[i][0] = i, dp[0][j] = j",
        "optimal_complexity": "O(m*n) time, O(m*n) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 59: Decode Ways
    # ──────────────────────────────────────────────────────────────
    "Decode Ways": {
        "leetcode": 91,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Count ways to decode a number string (1→A, 2→B, ..., 26→Z).",
        "state": "dp[i] = number of ways to decode s[:i]",
        "recurrence": """
            If s[i-1] != '0': dp[i] += dp[i-1]         (single digit decode)
            If s[i-2:i] is between '10' and '26': dp[i] += dp[i-2]  (two digit)
        """,
        "base_case": "dp[0] = 1",
        "optimal_complexity": "O(n) time, O(1) space with two variables",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  13. BACKTRACKING                                                           ║
# ║  Systematic exploration of all possibilities with pruning.                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Build solutions incrementally, abandon (backtrack) when you detect
      a solution won't work. DFS on the solution space tree.

WHEN TO USE:
    - "Find ALL possible..."       → Generate all combinations/permutations
    - "Find ANY valid..."          → Find one solution satisfying constraints
    - Constraint satisfaction       → Sudoku, N-Queens
    - Combinatorial search         → Subsets, partitions

TEMPLATE:
    def backtrack(state, choices):
        if IS_COMPLETE(state):
            result.append(state.copy())
            return

        for choice in choices:
            if IS_VALID(choice, state):
                MAKE_CHOICE(state, choice)
                backtrack(state, remaining_choices)
                UNDO_CHOICE(state, choice)    ← the "backtrack" step
"""

BACKTRACKING_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 60: Subsets
    # ──────────────────────────────────────────────────────────────
    "Subsets": {
        "leetcode": 78,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Generate all subsets of a set.",
        "optimal_algorithm": "Backtracking (include/exclude each element)",
        "technique": """
            def backtrack(start, current):
                result.append(current[:])      # add current subset
                for i in range(start, len(nums)):
                    current.append(nums[i])     # include
                    backtrack(i + 1, current)
                    current.pop()               # exclude (backtrack)
        """,
        "optimal_complexity": "O(n * 2^n) time, O(n) space (recursion depth)",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 61: Permutations
    # ──────────────────────────────────────────────────────────────
    "Permutations": {
        "leetcode": 46,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Generate all permutations of an array.",
        "optimal_algorithm": "Backtracking with used set",
        "technique": """
            def backtrack(current):
                if len(current) == len(nums):
                    result.append(current[:])
                    return
                for num in nums:
                    if num not in current:      # or use 'used' set
                        current.append(num)
                        backtrack(current)
                        current.pop()
        """,
        "optimal_complexity": "O(n! * n) time",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 62: Combination Sum
    # ──────────────────────────────────────────────────────────────
    "Combination Sum": {
        "leetcode": 39,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Find all combinations of candidates that sum to target (can reuse).",
        "optimal_algorithm": "Backtracking with target reduction",
        "technique": """
            def backtrack(start, current, remaining):
                if remaining == 0:
                    result.append(current[:])
                    return
                for i in range(start, len(candidates)):
                    if candidates[i] > remaining:
                        break                    # pruning
                    current.append(candidates[i])
                    backtrack(i, current, remaining - candidates[i])
                    current.pop()
        """,
        "optimal_complexity": "Exponential, but pruning makes it practical",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 63: Word Search
    # ──────────────────────────────────────────────────────────────
    "Word Search": {
        "leetcode": 79,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Can the word be found in the grid by adjacent cells?",
        "optimal_algorithm": "DFS/Backtracking on grid",
        "technique": """
            For each cell matching word[0]:
                DFS exploring all 4 directions
                Mark cell as visited (modify grid or use set)
                If word found → True
                Unmark cell (backtrack)
        """,
        "optimal_complexity": "O(m * n * 4^L) where L = word length",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  14. UNION-FIND (DISJOINT SET)                                              ║
# ║  Efficiently track connected components.                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Data structure that tracks which elements belong to the same group.
      Two operations: union (merge groups) and find (which group?).

KEY OPERATIONS:
    Find(x)       → O(α(n)) ≈ O(1) with path compression
    Union(x, y)   → O(α(n)) ≈ O(1) with union by rank

WHEN TO USE:
    - "Are X and Y connected?"
    - "How many connected components?"
    - Cycle detection in undirected graphs
    - Merging groups incrementally

TEMPLATE:
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
            if px == py: return False  # already connected
            if self.rank[px] < self.rank[py]: px, py = py, px
            self.parent[py] = px
            if self.rank[px] == self.rank[py]: self.rank[px] += 1
            return True
"""

UNION_FIND_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 64: Number of Connected Components
    # ──────────────────────────────────────────────────────────────
    "Number of Connected Components": {
        "leetcode": 323,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Count connected components in undirected graph.",
        "optimal_algorithm": "Union-Find",
        "technique": """
            Initialize: n components (each node is its own group)
            For each edge: union the two nodes
            If union succeeds: components -= 1
            Return components
        """,
        "optimal_complexity": "O(E * α(V)) ≈ O(E) time",
        "role_relevance": "ROLLOUTS: how many independent service groups exist?",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 65: Redundant Connection
    # ──────────────────────────────────────────────────────────────
    "Redundant Connection": {
        "leetcode": 684,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Find the edge that creates a cycle in a tree.",
        "optimal_algorithm": "Union-Find — the edge that fails to union",
        "technique": """
            Process edges one by one.
            For each edge: try to union.
            If both nodes already in same component → THIS edge creates cycle.
            Return it.
        """,
        "optimal_complexity": "O(n * α(n)) ≈ O(n) time",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  15. GREEDY ALGORITHMS                                                      ║
# ║  Make locally optimal choice at each step.                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Make the best local choice at each step, hoping it leads to global optimum.

WHEN TO USE:
    - Scheduling/interval problems
    - "Minimum number of X to cover Y"
    - When greedy choice property holds (local optimal → global optimal)
    - Often involves sorting first

HOW TO VERIFY: Can you prove that choosing greedily never makes
               the overall solution worse?
"""

GREEDY_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 66: Meeting Rooms II
    # ──────────────────────────────────────────────────────────────
    "Meeting Rooms II": {
        "leetcode": 253,
        "priority": "★★★",
        "difficulty": "Medium",
        "problem": "Find minimum meeting rooms needed for all meetings.",
        "optimal_algorithm": "Sort + Min-Heap OR Event-based sweep",
        "technique": """
            HEAP approach:
            1. Sort by start time
            2. Min-heap tracks end times of ongoing meetings
            3. For each meeting:
               If earliest ending meeting ends before this starts:
                   Reuse room (pop from heap)
               Push current meeting's end time
            4. Heap size = rooms needed

            EVENT approach:
            1. Create events: (time, +1 for start, -1 for end)
            2. Sort events
            3. Running sum = concurrent meetings
            4. Max running sum = rooms needed
        """,
        "optimal_complexity": "O(n log n) time, O(n) space",
        "role_relevance": "ROLLOUTS: how many parallel rollout slots do we need?",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 67: Jump Game
    # ──────────────────────────────────────────────────────────────
    "Jump Game": {
        "leetcode": 55,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Can you reach the last index? Each element = max jump from that position.",
        "optimal_algorithm": "Greedy — track farthest reachable position",
        "technique": """
            max_reach = 0
            for i in range(len(nums)):
                if i > max_reach: return False  # can't reach this position
                max_reach = max(max_reach, i + nums[i])
            return True
        """,
        "optimal_complexity": "O(n) time, O(1) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 68: Non-overlapping Intervals
    # ──────────────────────────────────────────────────────────────
    "Non-overlapping Intervals": {
        "leetcode": 435,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Minimum intervals to remove to make rest non-overlapping.",
        "optimal_algorithm": "Greedy — sort by end time, keep earliest ending",
        "technique": """
            Sort by end time.
            Keep track of last non-overlapping end.
            For each interval:
                If starts before last end: remove it (count += 1)
                Else: update last end
        """,
        "optimal_complexity": "O(n log n) time, O(1) space",
        "why_it_works": "Keeping intervals that end earliest leaves maximum room for future intervals",
        "role_relevance": "ROLLOUTS: resolving conflicting maintenance windows",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  16. TRIES                                                                  ║
# ║  Prefix tree for string operations.                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
WHAT: Tree where each node represents a character. Path from root to
      node spells a prefix.

KEY OPERATIONS:
    Insert     → O(m) where m = word length
    Search     → O(m)
    StartsWith → O(m)

WHEN TO USE:
    - Autocomplete / prefix matching
    - Spell checker
    - IP routing (longest prefix match)
    - Word search in grid with dictionary
"""

TRIE_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 69: Implement Trie
    # ──────────────────────────────────────────────────────────────
    "Implement Trie": {
        "leetcode": 208,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Implement insert, search, and startsWith.",
        "technique": """
            class TrieNode:
                def __init__(self):
                    self.children = {}      # char → TrieNode
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

                def startsWith(self, prefix):
                    return self._find(prefix) is not None

                def _find(self, text):
                    node = self.root
                    for char in text:
                        if char not in node.children:
                            return None
                        node = node.children[char]
                    return node
        """,
        "optimal_complexity": "O(m) for each operation",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 70: Word Search II
    # ──────────────────────────────────────────────────────────────
    "Word Search II": {
        "leetcode": 212,
        "priority": "★",
        "difficulty": "Hard",
        "problem": "Find all words from dictionary in a grid.",
        "optimal_algorithm": "Trie + DFS Backtracking",
        "technique": """
            1. Build Trie from word list
            2. DFS from each cell, following Trie branches
            3. If reach end-of-word node → found a word
            4. Prune: if no Trie branch → stop exploring
        """,
        "optimal_complexity": "O(m * n * 4^L) worst case, but Trie prunes heavily",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  17. BIT MANIPULATION (Good to know, less frequent at Google)               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

BIT_PROBLEMS = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 71: Single Number
    # ──────────────────────────────────────────────────────────────
    "Single Number": {
        "leetcode": 136,
        "priority": "★★",
        "difficulty": "Easy",
        "problem": "Every element appears twice except one. Find it.",
        "optimal_algorithm": "XOR all elements",
        "technique": """
            result = 0
            for num in nums:
                result ^= num    # XOR: same numbers cancel out
            return result
        """,
        "optimal_complexity": "O(n) time, O(1) space",
        "why_it_works": "a XOR a = 0, a XOR 0 = a. Duplicates cancel, single remains.",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 72: Number of 1 Bits
    # ──────────────────────────────────────────────────────────────
    "Number of 1 Bits": {
        "leetcode": 191,
        "priority": "★",
        "difficulty": "Easy",
        "problem": "Count set bits (1s) in binary representation.",
        "optimal_algorithm": "Brian Kernighan's algorithm",
        "technique": """
            count = 0
            while n:
                n &= (n - 1)    # removes lowest set bit
                count += 1
            return count
        """,
        "optimal_complexity": "O(k) where k = number of set bits",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  18. ADDITIONAL HIGH-VALUE GOOGLE PROBLEMS                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

ADDITIONAL_GOOGLE_FAVORITES = {
    # ──────────────────────────────────────────────────────────────
    # PROBLEM 73: Rotate Image (Matrix)
    # ──────────────────────────────────────────────────────────────
    "Rotate Image": {
        "leetcode": 48,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Rotate n×n matrix 90 degrees clockwise in-place.",
        "technique": """
            Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
            Step 2: Reverse each row

            for i in range(n):
                for j in range(i+1, n):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            for row in matrix:
                row.reverse()
        """,
        "optimal_complexity": "O(n²) time, O(1) space",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 74: Design Hit Counter
    # ──────────────────────────────────────────────────────────────
    "Design Hit Counter": {
        "leetcode": 362,
        "priority": "★★",
        "difficulty": "Medium",
        "problem": "Count hits in the past 5 minutes.",
        "optimal_algorithm": "Queue (deque) or circular array",
        "technique": """
            Deque approach:
            hit(timestamp): append timestamp
            getHits(timestamp): remove timestamps older than 300s, return len

            Circular array approach (O(1) space):
            times[300], hits[300]
            Bucket = timestamp % 300
        """,
        "optimal_complexity": "O(1) amortized per operation",
        "role_relevance": "ROLLOUTS: counting errors in a rolling time window for health checks",
    },

    # ──────────────────────────────────────────────────────────────
    # PROBLEM 75: Alien Dictionary (Topological Sort)
    # ──────────────────────────────────────────────────────────────
    "Alien Dictionary": {
        "leetcode": 269,
        "priority": "★★★",
        "difficulty": "Hard",
        "problem": "Given sorted alien words, derive the character ordering.",
        "optimal_algorithm": "Build directed graph from adjacent words + Topological Sort",
        "technique": """
            1. Compare adjacent words character by character
            2. First difference gives us an edge: char_a → char_b
            3. Build directed graph of character ordering
            4. Topological sort on the graph
            5. If cycle → invalid ordering
        """,
        "optimal_complexity": "O(C) where C = total chars across all words",
        "role_relevance": "ROLLOUTS: deriving deployment order from partial ordering constraints",
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  SUMMARY: THE 75-PROBLEM CHECKLIST                                          ║
# ║  Check off each problem as you complete it.                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
PROGRESS TRACKER (mark [x] when solved, [r] when re-solved from memory):

ARRAYS & STRINGS (10 problems)
[ ] 1.  Two Sum (LC 1) — Hash Map
[ ] 2.  Best Time to Buy/Sell Stock (LC 121) — Track min
[ ] 3.  Product of Array Except Self (LC 238) — Prefix/Suffix
[ ] 4.  Maximum Subarray (LC 53) — Kadane's
[ ] 5.  Container With Most Water (LC 11) — Two Pointers
[ ] 6.  Merge Intervals (LC 56) — Sort + Sweep
[ ] 7.  Trapping Rain Water (LC 42) — Two Pointers
[ ] 8.  Valid Anagram (LC 242) — Counter
[ ] 9.  Longest Consecutive Sequence (LC 128) — Hash Set
[ ] 10. Subarray Sum Equals K (LC 560) — Prefix Sum + Hash Map

HASH MAPS (3 problems)
[ ] 11. Group Anagrams (LC 49) — Hash Map + Sort Key
[ ] 12. Top K Frequent Elements (LC 347) — Bucket Sort / Heap
[ ] 13. LRU Cache (LC 146) — Hash Map + Doubly Linked List

TWO POINTERS (3 problems)
[ ] 14. 3Sum (LC 15) — Sort + Two Pointers
[ ] 15. Valid Palindrome (LC 125) — Two Pointers
[ ] 16. Move Zeroes (LC 283) — Read/Write Pointers

SLIDING WINDOW (4 problems)
[ ] 17. Longest Substring Without Repeating (LC 3) — Window + Set
[ ] 18. Minimum Window Substring (LC 76) — Window + Counters
[ ] 19. Longest Repeating Char Replacement (LC 424) — Window + Freq
[ ] 20. Sliding Window Maximum (LC 239) — Monotonic Deque

BINARY SEARCH (4 problems)
[ ] 21. Search in Rotated Sorted Array (LC 33) — Modified BS
[ ] 22. Find Min in Rotated Sorted Array (LC 153) — BS
[ ] 23. Koko Eating Bananas (LC 875) — BS on Answer
[ ] 24. Search a 2D Matrix (LC 74) — Flatten + BS

STACKS (4 problems)
[ ] 25. Valid Parentheses (LC 20) — Stack
[ ] 26. Daily Temperatures (LC 739) — Monotonic Stack
[ ] 27. Min Stack (LC 155) — Two Stacks
[ ] 28. Largest Rectangle in Histogram (LC 84) — Monotonic Stack

LINKED LISTS (4 problems)
[ ] 29. Reverse Linked List (LC 206) — Three Pointers
[ ] 30. Merge Two Sorted Lists (LC 21) — Dummy Head
[ ] 31. Linked List Cycle (LC 141) — Floyd's Slow/Fast
[ ] 32. Merge K Sorted Lists (LC 23) — Min Heap

TREES (8 problems)
[ ] 33. Max Depth of Binary Tree (LC 104) — DFS
[ ] 34. Invert Binary Tree (LC 226) — DFS Swap
[ ] 35. Level Order Traversal (LC 102) — BFS Queue
[ ] 36. Validate BST (LC 98) — DFS + Bounds
[ ] 37. Lowest Common Ancestor BST (LC 235) — BST Property
[ ] 38. Kth Smallest in BST (LC 230) — Inorder
[ ] 39. Binary Tree Max Path Sum (LC 124) — Postorder DFS
[ ] 40. Serialize/Deserialize Tree (LC 297) — Preorder + Null Markers

GRAPHS (7 problems)
[ ] 41. Number of Islands (LC 200) — BFS/DFS
[ ] 42. Clone Graph (LC 133) — DFS + Hash Map
[ ] 43. Course Schedule (LC 207) — Cycle Detection
[ ] 44. Course Schedule II (LC 210) — Topological Sort
[ ] 45. Pacific Atlantic Water Flow (LC 417) — Multi-source BFS
[ ] 46. Word Ladder (LC 127) — BFS Shortest Path
[ ] 47. Graph Valid Tree (LC 261) — Union-Find / DFS

HEAPS (3 problems)
[ ] 48. Kth Largest Element (LC 215) — Min Heap of size k
[ ] 49. Find Median from Stream (LC 295) — Two Heaps
[ ] 50. Task Scheduler (LC 621) — Max Heap + Queue

DYNAMIC PROGRAMMING (9 problems)
[ ] 51. Climbing Stairs (LC 70) — Fibonacci DP
[ ] 52. House Robber (LC 198) — Decision DP
[ ] 53. Coin Change (LC 322) — Unbounded Knapsack DP
[ ] 54. Longest Increasing Subsequence (LC 300) — 1D DP
[ ] 55. Word Break (LC 139) — String DP
[ ] 56. Unique Paths (LC 62) — 2D Grid DP
[ ] 57. Longest Common Subsequence (LC 1143) — 2D String DP
[ ] 58. Edit Distance (LC 72) — 2D String DP
[ ] 59. Decode Ways (LC 91) — 1D DP

BACKTRACKING (4 problems)
[ ] 60. Subsets (LC 78) — Include/Exclude
[ ] 61. Permutations (LC 46) — Used Set
[ ] 62. Combination Sum (LC 39) — Target Reduction
[ ] 63. Word Search (LC 79) — Grid DFS + Backtrack

UNION-FIND (2 problems)
[ ] 64. Connected Components (LC 323) — Union-Find
[ ] 65. Redundant Connection (LC 684) — Cycle via Union-Find

GREEDY (3 problems)
[ ] 66. Meeting Rooms II (LC 253) — Sort + Heap
[ ] 67. Jump Game (LC 55) — Greedy Max Reach
[ ] 68. Non-overlapping Intervals (LC 435) — Sort by End

TRIES (2 problems)
[ ] 69. Implement Trie (LC 208) — Trie Node + Children Map
[ ] 70. Word Search II (LC 212) — Trie + DFS

BIT MANIPULATION (2 problems)
[ ] 71. Single Number (LC 136) — XOR
[ ] 72. Number of 1 Bits (LC 191) — Brian Kernighan's

BONUS GOOGLE FAVORITES (3 problems)
[ ] 73. Rotate Image (LC 48) — Transpose + Reverse
[ ] 74. Design Hit Counter (LC 362) — Deque / Circular Array
[ ] 75. Alien Dictionary (LC 269) — Graph + Topo Sort
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  QUICK REFERENCE: WHICH ALGORITHM FOR WHICH SIGNAL?                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
COMPLEXITY CHEAT SHEET — Know these cold for the interview:

O(1)        → Hash map lookup, array access, stack/queue operations
O(log n)    → Binary search, balanced BST operations
O(n)        → Single pass, hash map build, linear scan
O(n log n)  → Sorting (merge sort, Tim sort), heap operations on n items
O(n²)       → Nested loops, simple DP, brute force pairs
O(2^n)      → Subsets, backtracking without pruning
O(n!)       → Permutations

SPACE COMPLEXITY:
O(1)        → Two pointers, Kadane's, greedy with variables
O(n)        → Hash map, stack, queue, 1D DP
O(n²)       → 2D DP, adjacency matrix
O(h)        → Tree recursion (h = height, log n for balanced, n for skewed)

THE OPTIMIZATION LADDER (common follow-up sequence):
    Brute force O(n²) or O(n³)
    → Sort first? O(n log n)
    → Hash map? O(n) time, O(n) space
    → Two pointers? O(n) time, O(1) space
    → Can we precompute? Prefix sums / products
    → Can we binary search on the answer? O(n log range)
    → Dynamic programming? Trade time for space

WHEN INTERVIEWER SAYS "CAN YOU DO BETTER?":
    Look at your solution and ask:
    1. Am I doing redundant work? → Cache/memoize it
    2. Am I scanning when I could look up? → Use hash map
    3. Am I sorting when I don't need full order? → Use heap for top-k
    4. Am I checking all pairs when order helps? → Sort + two pointers
    5. Am I recomputing overlapping subproblems? → DP
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PATTERN RECOGNITION DECISION TREE                                          ║
# ║  Use this during the interview to quickly identify the right approach.      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
START HERE → Read the problem

Is the input SORTED (or can sorting help)?
├── YES → Is it "find target"? → BINARY SEARCH
│       → Is it "find pair/triplet"? → TWO POINTERS (from both ends)
│       → Is it "merge/overlap"? → SORT + LINEAR SCAN
│
├── NO → Continue below

Is it about SUBARRAY or SUBSTRING?
├── YES → Is it "longest/shortest with constraint"? → SLIDING WINDOW
│       → Is it "sum equals k"? → PREFIX SUM + HASH MAP
│       → Is it "maximum sum"? → KADANE'S ALGORITHM
│
├── NO → Continue below

Is it about a TREE?
├── YES → Is it "height/depth/balance"? → DFS RECURSION
│       → Is it "level by level"? → BFS WITH QUEUE
│       → Is it "sorted property"? → BST: INORDER TRAVERSAL
│       → Is it "path from root"? → DFS WITH RUNNING STATE
│
├── NO → Continue below

Is it about a GRAPH / GRID / CONNECTIONS?
├── YES → Is it "shortest path (unweighted)"? → BFS
│       → Is it "all paths / explore all"? → DFS
│       → Is it "ordering with dependencies"? → TOPOLOGICAL SORT
│       → Is it "connected components"? → UNION-FIND or BFS/DFS
│       → Is it "cycle detection"? → DFS (directed) / UNION-FIND (undirected)
│
├── NO → Continue below

Is it "find / count / optimize" with CHOICES AFFECTING FUTURE?
├── YES → Is it "count ways"? → DYNAMIC PROGRAMMING
│       → Is it "min/max cost"? → DYNAMIC PROGRAMMING
│       → Is it "is it possible"? → DP or GREEDY
│
├── NO → Continue below

Is it "generate all / find all valid"?
├── YES → BACKTRACKING
│
├── NO → Continue below

Is it about FREQUENCY / EXISTENCE / GROUPING?
├── YES → HASH MAP / HASH SET

Is it about TOP K / STREAMING / PRIORITY?
├── YES → HEAP (PRIORITY QUEUE)

Does it involve MATCHING / NESTING?
├── YES → STACK
"""


if __name__ == "__main__":
    total_problems = (
        len(ARRAY_PROBLEMS) + len(HASHMAP_PROBLEMS) + len(TWO_POINTER_PROBLEMS) +
        len(SLIDING_WINDOW_PROBLEMS) + len(BINARY_SEARCH_PROBLEMS) +
        len(STACK_PROBLEMS) + len(LINKED_LIST_PROBLEMS) + len(TREE_PROBLEMS) +
        len(GRAPH_PROBLEMS) + len(HEAP_PROBLEMS) + len(DP_PROBLEMS) +
        len(BACKTRACKING_PROBLEMS) + len(UNION_FIND_PROBLEMS) +
        len(GREEDY_PROBLEMS) + len(TRIE_PROBLEMS) + len(BIT_PROBLEMS) +
        len(ADDITIONAL_GOOGLE_FAVORITES)
    )

    print(f"GOOGLE SWE III DSA MASTER LIST")
    print(f"Total problems: {total_problems}")
    print(f"\nData Structures & Patterns covered:")
    print(f"  1.  Arrays & Strings      — {len(ARRAY_PROBLEMS)} problems")
    print(f"  2.  Hash Maps & Sets       — {len(HASHMAP_PROBLEMS)} problems")
    print(f"  3.  Two Pointers           — {len(TWO_POINTER_PROBLEMS)} problems")
    print(f"  4.  Sliding Window         — {len(SLIDING_WINDOW_PROBLEMS)} problems")
    print(f"  5.  Binary Search          — {len(BINARY_SEARCH_PROBLEMS)} problems")
    print(f"  6.  Stacks                 — {len(STACK_PROBLEMS)} problems")
    print(f"  7.  Linked Lists           — {len(LINKED_LIST_PROBLEMS)} problems")
    print(f"  8.  Trees                  — {len(TREE_PROBLEMS)} problems")
    print(f"  9.  Graphs                 — {len(GRAPH_PROBLEMS)} problems")
    print(f"  10. Heaps                  — {len(HEAP_PROBLEMS)} problems")
    print(f"  11. Dynamic Programming    — {len(DP_PROBLEMS)} problems")
    print(f"  12. Backtracking           — {len(BACKTRACKING_PROBLEMS)} problems")
    print(f"  13. Union-Find             — {len(UNION_FIND_PROBLEMS)} problems")
    print(f"  14. Greedy                 — {len(GREEDY_PROBLEMS)} problems")
    print(f"  15. Tries                  — {len(TRIE_PROBLEMS)} problems")
    print(f"  16. Bit Manipulation       — {len(BIT_PROBLEMS)} problems")
    print(f"  17. Google Favorites       — {len(ADDITIONAL_GOOGLE_FAVORITES)} problems")
    print(f"\nStart with ★★★ problems first. Good luck, Omkar!")
