"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  RATE LIMITER — 5 ALGORITHMS FROM SCRATCH                                  ║
║  Omkar Joshi — Google / Microsoft System Design Prep                       ║
║                                                                            ║
║  A Rate Limiter controls HOW MANY requests a user/client can make          ║
║  in a given time window. Prevents abuse, protects downstream services.     ║
╚══════════════════════════════════════════════════════════════════════════════╝

INTERVIEW CHEAT SHEET — Which algorithm to mention when:

┌─────────────────────────┬──────────────────────────────────────────────────┐
│ Algorithm               │ Best For                                         │
├─────────────────────────┼──────────────────────────────────────────────────┤
│ Token Bucket            │ Allows bursts. Smooths rate long-term.           │
│                         │ Use: API rate limiting with burst tolerance.     │
├─────────────────────────┼──────────────────────────────────────────────────┤
│ Leaky Bucket            │ Strict constant output rate. No bursts.          │
│                         │ Use: Network traffic shaping.                    │
├─────────────────────────┼──────────────────────────────────────────────────┤
│ Fixed Window Counter    │ Simple, cheap. Boundary exploit possible.        │
│                         │ Use: Quick prototypes, non-critical limits.      │
├─────────────────────────┼──────────────────────────────────────────────────┤
│ Sliding Window Log      │ Most accurate. Expensive memory.                 │
│                         │ Use: When accuracy is critical (finance/payments)│
├─────────────────────────┼──────────────────────────────────────────────────┤
│ Sliding Window Counter  │ Best balance: accurate, memory-efficient.        │
│                         │ Use: Production systems (Redis-based approach).  │
└─────────────────────────┴──────────────────────────────────────────────────┘
"""

import time
import threading
from collections import deque


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ALGORITHM 1: TOKEN BUCKET                                                  ║
# ║  Most common in real systems (AWS API Gateway, Stripe, etc.)                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
HOW IT WORKS:
    Imagine a bucket that holds tokens.
    - Tokens are added at a fixed REFILL RATE (e.g., 10 tokens/second)
    - Bucket has a max CAPACITY (e.g., 100 tokens) — prevents infinite accumulation
    - Each request consumes 1 token
    - If bucket is empty → reject request
    - If bucket has tokens → allow request, consume 1 token

VISUAL:
    Tokens added → [■■■■■□□□□□] Bucket (capacity=10, current=5)
    Request comes → consumes 1 → [■■■■□□□□□□]
    Burst allowed → can use all 10 tokens at once if bucket is full

KEY PROPERTY: Allows BURSTS up to bucket capacity.
              Long-term average rate = refill_rate.

WHEN TO USE:
    - APIs where occasional bursts are acceptable
    - "Up to 100 requests at once, but no more than 10/sec on average"

TIME/SPACE: O(1) per request, O(1) per user (just 2 values to store)
"""

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity:    Max tokens in bucket (controls burst size)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity          # start full
        self.last_refill_time = time.time()
        self._lock = threading.Lock()   # thread-safe for concurrent requests

    def _refill(self):
        """Add tokens based on time elapsed since last refill."""
        now = time.time()
        elapsed = now - self.last_refill_time
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill_time = now

    def allow_request(self) -> bool:
        with self._lock:
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False                # bucket empty — reject


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ALGORITHM 2: LEAKY BUCKET                                                  ║
# ║  Enforces strict constant output rate (no bursts allowed)                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
HOW IT WORKS:
    Imagine a bucket with a hole at the bottom that leaks at a fixed rate.
    - Requests enter the bucket from the top
    - Requests are processed at a CONSTANT LEAK RATE from the bottom
    - Bucket has a max CAPACITY (queue size)
    - If bucket is full → reject new request (overflow)

VISUAL:
    Requests → [■■■■■] Bucket (queue of pending requests)
                  ↓
              LEAK RATE: 1 request every 100ms (constant output)

KEY PROPERTY: OUTPUT is always constant rate, regardless of input pattern.
              Bursts are queued, not rejected immediately (up to capacity).

vs Token Bucket:
    Token Bucket: allows burst processing immediately
    Leaky Bucket:  queues burst, processes at constant rate

WHEN TO USE:
    - Network traffic shaping
    - "Process exactly N requests per second, queue the rest"

TIME/SPACE: O(1) per request check, O(capacity) space for queue
"""

class LeakyBucket:
    def __init__(self, capacity: int, leak_rate: float):
        """
        Args:
            capacity:  Max requests that can be queued
            leak_rate: Requests processed per second (constant output rate)
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.queue_size = 0             # current pending requests
        self.last_leak_time = time.time()
        self._lock = threading.Lock()

    def _leak(self):
        """Remove processed requests based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_leak_time
        leaked = elapsed * self.leak_rate
        self.queue_size = max(0, self.queue_size - leaked)
        self.last_leak_time = now

    def allow_request(self) -> bool:
        with self._lock:
            self._leak()
            if self.queue_size < self.capacity:
                self.queue_size += 1
                return True             # queued successfully
            return False                # bucket full — reject (overflow)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ALGORITHM 3: FIXED WINDOW COUNTER                                          ║
# ║  Simplest algorithm. Has a known flaw — boundary exploit.                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
HOW IT WORKS:
    - Divide time into fixed windows (e.g., each window = 1 minute)
    - Track a counter per window per user
    - Allow up to LIMIT requests per window
    - Counter resets when window rolls over

VISUAL:
    Window 1:        Window 2:         Window 3:
    |----60s----|    |----60s----|     |----60s----|
    [■■■■■■■■□□]     [■□□□□□□□□□]     [■■□□□□□□□□]
      8/10 used        1/10 used         2/10 used

THE FLAW — Boundary Attack:
    Limit = 10/minute, Windows at :00-:59 and :60-:119

    User sends 10 requests at :59 → allowed (Window 1 has 10)
    User sends 10 requests at :60 → allowed (Window 2 starts fresh)

    Result: 20 requests in 2 seconds! The window boundary can be exploited.

WHEN TO USE:
    - Simple internal tools where precision isn't critical
    - When you need dead-simple implementation and understand the trade-off

TIME/SPACE: O(1) per request, O(1) per user (just counter + window start)
"""

class FixedWindowCounter:
    def __init__(self, limit: int, window_size: float):
        """
        Args:
            limit:       Max requests allowed per window
            window_size: Window duration in seconds
        """
        self.limit = limit
        self.window_size = window_size
        self.counts = {}                # user_id → (count, window_start)
        self._lock = threading.Lock()

    def allow_request(self, user_id: str) -> bool:
        with self._lock:
            now = time.time()
            if user_id not in self.counts:
                self.counts[user_id] = (0, now)

            count, window_start = self.counts[user_id]

            # Check if we're in a new window
            if now - window_start >= self.window_size:
                count = 0               # reset counter
                window_start = now      # new window starts

            if count < self.limit:
                self.counts[user_id] = (count + 1, window_start)
                return True
            return False                # limit hit for this window


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ALGORITHM 4: SLIDING WINDOW LOG                                            ║
# ║  Most accurate. Fixes the boundary flaw. Memory-heavy.                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
HOW IT WORKS:
    - Store the EXACT TIMESTAMP of every request in a log (deque)
    - On each new request:
        1. Remove all timestamps older than WINDOW_SIZE seconds ago
        2. Count remaining timestamps
        3. If count < LIMIT → allow and add current timestamp
        4. If count >= LIMIT → reject

VISUAL:
    Window slides with time:

    Now = 100s, Window = 60s, Limit = 5
    Log: [45s, 55s, 70s, 85s, 95s]  ← 5 timestamps within last 60s

    New request at 100s:
    - Remove timestamps < 40s: nothing removed
    - Count = 5, which equals limit → REJECT

    At 110s:
    - Remove timestamps < 50s: remove [45s]
    - Count = 4 < limit=5 → ALLOW, add 110s
    - Log: [55s, 70s, 85s, 95s, 110s]

KEY PROPERTY: Perfectly accurate. No boundary exploit possible.
              The window SLIDES continuously with time.

THE TRADE-OFF: Must store every timestamp → O(N) memory per user
               where N = max requests in the window

WHEN TO USE:
    - When accuracy is critical (financial APIs, payment systems)
    - Low volume systems where memory is not a constraint

TIME/SPACE: O(N) per request (removing old entries), O(N) space per user
            where N = number of requests in the window
"""

class SlidingWindowLog:
    def __init__(self, limit: int, window_size: float):
        """
        Args:
            limit:       Max requests allowed in any window_size second window
            window_size: Size of the sliding window in seconds
        """
        self.limit = limit
        self.window_size = window_size
        self.logs = {}                  # user_id → deque of timestamps
        self._lock = threading.Lock()

    def allow_request(self, user_id: str) -> bool:
        with self._lock:
            now = time.time()
            if user_id not in self.logs:
                self.logs[user_id] = deque()

            log = self.logs[user_id]
            window_start = now - self.window_size

            # Remove timestamps that are outside the window
            while log and log[0] <= window_start:
                log.popleft()

            if len(log) < self.limit:
                log.append(now)         # record this request's timestamp
                return True
            return False                # too many requests in this window


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ALGORITHM 5: SLIDING WINDOW COUNTER (HYBRID)                               ║
# ║  Best balance of accuracy and memory. Used in production (Redis).            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
HOW IT WORKS:
    Combines Fixed Window (memory efficient) with a sliding calculation
    to approximate the true sliding window count.

    For a new request at time T:
    - Current window count = actual requests in current window
    - Previous window count = actual requests in previous window

    Weighted estimation of requests in sliding window:
        overlap = time_position_in_current_window / window_size
        estimated_count = (prev_count * (1 - overlap)) + current_count

    WHY THIS WORKS:
        If you're 30% into the current window, then ~70% of the previous
        window's requests are still inside your 1-minute sliding window.

        So: estimated = prev * 0.70 + current

VISUAL:
    Prev window [0-60s]: 8 requests
    Curr window [60-120s]: 3 requests
    Now = 75s (25% into current window, 75% of prev window overlaps)

    Estimated = 8 * (1 - 0.25) + 3 = 8 * 0.75 + 3 = 6 + 3 = 9 requests

vs Sliding Window Log:
    Log: stores every timestamp → O(N) memory
    Counter: stores just 2 integers per window → O(1) memory
    Accuracy: Counter is an approximation (~0.003% error in practice)

WHEN TO USE:
    - PRODUCTION systems at scale (this is what Redis + Cloudflare use)
    - When you need good accuracy without storing every timestamp
    - High-volume APIs

TIME/SPACE: O(1) per request, O(1) per user (just 2 counters)
"""

class SlidingWindowCounter:
    def __init__(self, limit: int, window_size: float):
        """
        Args:
            limit:       Max estimated requests in any sliding window
            window_size: Window size in seconds
        """
        self.limit = limit
        self.window_size = window_size
        # user_id → {curr_count, prev_count, curr_window_start}
        self.state = {}
        self._lock = threading.Lock()

    def allow_request(self, user_id: str) -> bool:
        with self._lock:
            now = time.time()

            if user_id not in self.state:
                self.state[user_id] = {
                    "curr_count": 0,
                    "prev_count": 0,
                    "curr_window_start": now
                }

            s = self.state[user_id]
            elapsed = now - s["curr_window_start"]

            # If we've moved past the current window
            if elapsed >= self.window_size:
                if elapsed >= 2 * self.window_size:
                    # Jumped over more than 1 window — prev is also stale
                    s["prev_count"] = 0
                else:
                    s["prev_count"] = s["curr_count"]
                s["curr_count"] = 0
                s["curr_window_start"] = now
                elapsed = 0

            # What fraction of current window has elapsed?
            overlap_fraction = elapsed / self.window_size

            # Estimate requests in the sliding window
            estimated = (s["prev_count"] * (1 - overlap_fraction)) + s["curr_count"]

            if estimated < self.limit:
                s["curr_count"] += 1
                return True
            return False                # estimated count too high — reject


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PER-USER RATE LIMITER WRAPPER                                              ║
# ║  Real systems apply limits PER USER, not globally.                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

class PerUserRateLimiter:
    """
    Wraps any rate limiter algorithm to apply limits per user/API key.
    Each user gets their own independent rate limit bucket.

    In a real distributed system, the buckets would live in Redis so
    all server instances share the same state per user.
    """
    def __init__(self, algorithm_class, limit: int, window_size: float, **kwargs):
        self.algorithm_class = algorithm_class
        self.limit = limit
        self.window_size = window_size
        self.kwargs = kwargs
        self.limiters = {}              # user_id → limiter instance
        self._lock = threading.Lock()

    def allow_request(self, user_id: str) -> bool:
        with self._lock:
            if user_id not in self.limiters:
                self.limiters[user_id] = self.algorithm_class(
                    self.limit, self.window_size, **self.kwargs
                )
        # Call without the global lock (each user's limiter has its own lock)
        return self.limiters[user_id].allow_request()


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DISTRIBUTED RATE LIMITER — Redis-based (for System Design interviews)      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
In production, rate limiters must work across MULTIPLE server instances.
If server A and server B each have their own in-memory limiter, a user
can bypass the limit by splitting requests across both servers.

SOLUTION: Centralized state in Redis.

Redis implementation of Sliding Window Counter:

    def allow_request_redis(user_id, limit, window_size):
        now = time.time()
        key_curr = f"rl:{user_id}:{int(now // window_size)}"
        key_prev = f"rl:{user_id}:{int(now // window_size) - 1}"

        pipe = redis.pipeline()
        pipe.incr(key_curr)                     # increment current window
        pipe.expire(key_curr, window_size * 2)  # auto-cleanup after 2 windows
        pipe.get(key_prev)                       # get previous window count
        curr_count, _, prev_count = pipe.execute()

        prev_count = int(prev_count or 0)
        overlap = (now % window_size) / window_size
        estimated = prev_count * (1 - overlap) + int(curr_count)

        if estimated > limit:
            redis.decr(key_curr)  # undo the increment
            return False
        return True

WHY REDIS:
    - Atomic operations (INCR, DECR) prevent race conditions
    - TTL (expire) auto-cleans old keys
    - Single source of truth across all servers
    - Can handle 100K+ operations/second
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DEMO AND TESTING                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def demo_algorithm(name: str, limiter, num_requests: int):
    """Send num_requests rapidly and count how many are allowed."""
    allowed = 0
    rejected = 0
    for i in range(num_requests):
        if hasattr(limiter, 'allow_request'):
            # Handle both per-user and direct limiters
            try:
                result = limiter.allow_request("user_1")
            except TypeError:
                result = limiter.allow_request()
        if result:
            allowed += 1
        else:
            rejected += 1
    print(f"{name:30s} | Sent: {num_requests:3d} | Allowed: {allowed:3d} | Rejected: {rejected:3d}")


def compare_all_algorithms():
    print("=" * 75)
    print("  RATE LIMITER COMPARISON")
    print("  Sending 20 rapid requests with limit=5 per 1 second window")
    print("=" * 75)
    print(f"{'Algorithm':30s} | {'Sent':>5} | {'Allowed':>8} | {'Rejected':>8}")
    print("-" * 75)

    NUM_REQUESTS = 20
    LIMIT = 5
    WINDOW = 1.0  # 1 second

    algorithms = [
        ("Token Bucket",           TokenBucket(capacity=LIMIT, refill_rate=LIMIT)),
        ("Leaky Bucket",           LeakyBucket(capacity=LIMIT, leak_rate=LIMIT)),
        ("Fixed Window Counter",   FixedWindowCounter(limit=LIMIT, window_size=WINDOW)),
        ("Sliding Window Log",     SlidingWindowLog(limit=LIMIT, window_size=WINDOW)),
        ("Sliding Window Counter", SlidingWindowCounter(limit=LIMIT, window_size=WINDOW)),
    ]

    for name, limiter in algorithms:
        allowed, rejected = 0, 0
        for _ in range(NUM_REQUESTS):
            # For algorithms that take user_id
            if isinstance(limiter, (FixedWindowCounter, SlidingWindowLog, SlidingWindowCounter)):
                result = limiter.allow_request("user_1")
            else:
                result = limiter.allow_request()
            if result:
                allowed += 1
            else:
                rejected += 1
        print(f"{name:30s} | {NUM_REQUESTS:>5} | {allowed:>8} | {rejected:>8}")


def demo_boundary_flaw():
    """
    Demonstrate the Fixed Window boundary exploit:
    A user can send 2x the limit around a window boundary.
    """
    print("\n" + "=" * 60)
    print("  FIXED WINDOW FLAW: BOUNDARY EXPLOIT DEMO")
    print("  Limit: 5/second window")
    print("=" * 60)

    WINDOW = 2.0  # 2 second window for easier demo
    limiter = FixedWindowCounter(limit=5, window_size=WINDOW)

    print("\nPhase 1: Send 5 requests near end of window 1")
    for i in range(5):
        result = limiter.allow_request("attacker")
        print(f"  Request {i+1}: {'✓ ALLOWED' if result else '✗ REJECTED'}")

    print("\n  → Sleeping until window boundary...")
    time.sleep(WINDOW)

    print("\nPhase 2: Send 5 MORE requests at start of window 2")
    for i in range(5):
        result = limiter.allow_request("attacker")
        print(f"  Request {i+1}: {'✓ ALLOWED' if result else '✗ REJECTED'}")

    print("\n  Result: 10 requests allowed in a 2-second window (2x the limit!)")
    print("  This is the boundary exploit. Sliding window algorithms fix this.")


def demo_token_burst():
    """Show that Token Bucket allows bursts."""
    print("\n" + "=" * 60)
    print("  TOKEN BUCKET: BURST ALLOWED")
    print("  Capacity: 5, Refill: 1/sec")
    print("=" * 60)

    limiter = TokenBucket(capacity=5, refill_rate=1)

    print("\nBurst: 5 immediate requests (bucket starts full):")
    for i in range(7):
        result = limiter.allow_request()
        print(f"  Request {i+1}: {'✓ ALLOWED' if result else '✗ REJECTED'}")

    print("\n  → First 5 allowed (burst), then rejected until tokens refill")


if __name__ == "__main__":
    compare_all_algorithms()
    demo_boundary_flaw()
    demo_token_burst()

    print("\n" + "=" * 60)
    print("  QUICK REVISION TABLE")
    print("=" * 60)
    print("""
  Algorithm              Memory    Accuracy   Allows Burst?
  ─────────────────────────────────────────────────────────
  Token Bucket           O(1)      Medium     YES (up to capacity)
  Leaky Bucket           O(N)      High       NO (strict output rate)
  Fixed Window Counter   O(1)      Low        NO (boundary flaw)
  Sliding Window Log     O(N)      Highest    NO
  Sliding Window Counter O(1)      High       NO
  ─────────────────────────────────────────────────────────
  N = number of requests in window
    """)

    print("  INTERVIEW RECOMMENDATION:")
    print("  For most system design interviews, propose:")
    print("  1. Sliding Window Counter (accurate, memory-efficient, Redis-friendly)")
    print("  2. OR Token Bucket (if bursts are acceptable)")
    print("  Mention the trade-offs of all 5 to show depth of knowledge.")
