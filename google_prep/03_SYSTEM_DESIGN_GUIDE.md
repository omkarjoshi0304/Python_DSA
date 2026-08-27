# SYSTEM DESIGN INTERVIEW MASTER GUIDE
**Omkar Joshi — Google L3 / Microsoft IC2 Prep**

> This guide is tailored to YOUR resume. You've already built production systems at Red Hat — the interview is about articulating what you know, not learning from scratch.

---

## Your Competitive Advantage

Most IC2/L3 candidates have *studied* system design. You've **shipped production systems**:
- ✅ RAG pipelines with vector databases at enterprise scale
- ✅ Kubernetes Operators reconciling distributed AI infrastructure
- ✅ LLM-as-judge evaluation pipelines
- ✅ MCP security guardrails enforcing compliance
- ✅ Monitoring with ELK/Prometheus/Grafana

**Strategy:** Lead with what you've built. When asked "design X," connect it to systems you've actually operated.

---

## PART 1: The Interview Framework (Use This Every Time)

### The 45-Minute Structure

```
Min 0-5:   Requirements Gathering (ASK, don't assume)
Min 5-10:  High-level architecture (boxes and arrows)
Min 10-30: Deep dive (2-3 components the interviewer picks)
Min 30-40: Scaling, failure modes, trade-offs
Min 40-45: Monitoring, ops, and wrap-up
```

### Requirements Gathering Template (Memorize This)

**Always start by asking these 4 categories:**

1. **Functional Requirements**
   - "What are the core features we need to support?"
   - "What's explicitly OUT of scope for this design?"
   - Example: "For the deployment system, are we handling just code deploys or also config/data migrations?"

2. **Non-Functional Requirements (Scale)**
   - "How many users/requests/records?"
   - "What's our target latency? (p50, p99?)"
   - "What availability target? (99.9%? 99.99%?)"
   - Example: "Are we talking 100 services or 10,000 services?"

3. **Constraints**
   - "Are there existing systems we must integrate with?"
   - "Any compliance/security requirements?"
   - "Single region or multi-region?"

4. **Success Metrics**
   - "How do we know the system is working well?"
   - Example for rollouts: "Zero bad deploys reaching 100% traffic? MTTD < 5 min?"

**Pro tip:** Write down the answers. Interviewers notice when you refer back to requirements mid-design.

---

## PART 2: The Building Blocks (Know These Cold)

Every system is built from ~12 components. Master these:

| Component | Purpose | When to Use | Your Experience |
|---|---|---|---|
| **Load Balancer** | Distribute traffic across servers | Always for horizontal scaling | Your K8s Operators provision these |
| **API Gateway** | Entry point: auth, rate limit, routing | When you need centralized control | Relevant to AI API throttling |
| **Application Servers** | Business logic | Core of most systems | Your lightspeed-service |
| **Cache (Redis/Memcached)** | Fast read access | Reduce DB load, speed up reads | Your RAG system likely caches embeddings |
| **Message Queue (Kafka/Pub-Sub)** | Async processing, event streaming | Decouple components, handle spikes | Relevant to rollout event pipelines |
| **Database** | Persistent storage | Always | PostgreSQL in your stack |
| **Object Storage (S3)** | Files, blobs, logs | Large unstructured data | Where your rag-content likely lives |
| **CDN** | Serve static content from edge | Global low-latency reads | Less relevant to backend roles |
| **Vector Database** | Nearest-neighbor search | RAG, recommendation | **You built this at Red Hat** |
| **Monitoring (Prometheus/Grafana)** | Metrics, alerting | Always | **You built this at Red Hat** |
| **Service Mesh (Istio)** | Inter-service comms, traffic mgmt | Microservices at scale | Your K8s env likely uses this |
| **Workflow Orchestrator** | Multi-step pipelines | Complex workflows | Your Operator is a reconciliation loop |

---

## PART 3: Core Concepts (Interview Favorites)

### 1. Scaling: Vertical vs Horizontal

```
Vertical: Bigger machine (more CPU/RAM)
  ✓ Simple
  ✗ Has limits (can't buy infinite RAM)
  ✗ Single point of failure

Horizontal: More machines
  ✓ Unlimited scaling
  ✓ No single point of failure
  ✗ Complexity: load balancing, data partitioning, consistency
  → This is what Google/Microsoft do. Always the answer at scale.
```

**Your angle:** "At Red Hat, we scaled lightspeed horizontally using K8s pods with HPA (Horizontal Pod Autoscaler), letting the Operator reconcile desired vs actual replicas."

### 2. CAP Theorem (Always Gets Asked)

```
You can only pick 2 of 3:
  C - Consistency: Every read gets the latest write
  A - Availability: Every request gets a response (no downtime)
  P - Partition tolerance: System works despite network failures

In practice, P is mandatory (networks WILL fail).
So the real choice: CP or AP?

CP (Consistency + Partition tolerance):
  → "I'd rather return an error than stale data"
  → Use cases: Banking, config management, **deployment systems**
  → Example: etcd, Spanner

AP (Availability + Partition tolerance):
  → "I'd rather return slightly stale data than no data"
  → Use cases: Social feeds, caching, analytics
  → Example: Cassandra, DynamoDB
```

**Your angle for Google Rollouts:** "Deployment config must be CP — serving stale rollout state could deploy the wrong version to production. Better to fail safe than serve incorrect data."

**Your angle for Microsoft AI Trust:** "AI guardrail rules should be CP — we'd rather block a request than serve unvalidated AI output."

### 3. Database Choices

| Type | Use When | Trade-off | Your Experience |
|---|---|---|---|
| **SQL (PostgreSQL, MySQL)** | Need ACID, complex queries, joins | Harder to scale horizontally | Your Llama Stack uses PostgreSQL |
| **NoSQL (MongoDB, Cassandra)** | High write throughput, flexible schema | Limited query flexibility | |
| **Vector DB (FAISS, Pinecone, Solr)** | Semantic search, embeddings | Specialized use case | **Your RAG pipelines** |
| **Time-series (Prometheus, InfluxDB)** | Metrics, logs over time | Read-heavy, aggregation-focused | **Your monitoring stack** |

**Your angle:** "For the RAG pipeline at Red Hat, we used PostgreSQL for structured metadata (documents, users) and a vector store (FAISS/Solr) for embedding search. This hybrid approach gave us ACID guarantees where needed while enabling fast nearest-neighbor retrieval."

### 4. Consistency Models

```
Strong Consistency: Read always returns latest write
  → Slower (coordination overhead)
  → PostgreSQL with serializable isolation

Eventual Consistency: Reads may temporarily return stale data
  → Faster (no coordination)
  → DNS, Cassandra, DynamoDB

Read-your-own-writes: You see your own updates immediately
  → Middle ground
  → Common in social apps (you see your own post instantly)
```

### 5. Caching Strategies

```
Cache-Aside (Lazy Loading):
  On read: check cache → if miss, load from DB, populate cache
  ✓ Only caches what's accessed
  ✗ Cache misses are slow

Write-Through:
  On write: update DB AND cache synchronously
  ✓ Cache always fresh
  ✗ Slower writes

Write-Behind (Write-Back):
  On write: update cache, asynchronously update DB
  ✓ Fast writes
  ✗ Risk of data loss if cache fails before DB sync
```

**Cache Invalidation (the hard problem):**
- TTL (Time To Live): expire after N seconds
- Event-driven: invalidate on writes
- LRU eviction: drop least recently used when full

---

## PART 4: Designs You MUST Be Able to Draw

These are the 6 systems most likely to be asked, mapped to YOUR experience.

---

### Design 1: ★★★ Canary Deployment / Rollout System

**Why this is critical:** Directly maps to Google Rollouts Supervision role.

**Requirements to clarify:**
- Scale: how many services? how many regions?
- SLO: what error rate increase triggers rollback?
- Human-in-loop or fully automated?

**High-level architecture:**

```
┌─────────────┐
│  Developer  │ triggers rollout
└──────┬──────┘
       ↓
┌──────────────────┐       ┌─────────────────────┐
│  Rollout API     │──────→│  Rollout Controller │
│  (REST endpoint) │       │  (state machine)    │
└──────────────────┘       └─────────┬───────────┘
                                     │
                ┌────────────────────┼──────────────────┐
                ↓                    ↓                  ↓
         ┌──────────┐         ┌──────────┐      ┌──────────┐
         │ Region 1 │         │ Region 2 │      │ Region N │
         │ 1%→5%→.. │         │ waiting  │      │ waiting  │
         └─────┬────┘         └──────────┘      └──────────┘
               │
         ┌─────┴─────┐
         │  Service  │
         │   Mesh    │  ← traffic splitting (Istio)
         └─────┬─────┘
               │
    ┌──────────┴──────────┐
    ↓                     ↓
┌────────┐           ┌────────┐
│ v1.0   │           │ v1.1   │  ← old + new running simultaneously
│ 99 pods│           │ 1 pod  │
└────────┘           └────────┘
    │                     │
    └──────────┬──────────┘
               ↓
      ┌────────────────┐       ┌──────────────┐
      │ Metrics        │──────→│  Decision    │
      │ Pipeline       │       │  Engine      │
      │ (Prometheus)   │       │ (auto promote│
      └────────────────┘       │  or rollback)│
                               └──────────────┘
```

**Deep dive components:**

1. **Rollout Controller (State Machine)**
   ```
   States: CREATED → CANARY → ROLLING → COMPLETE
   Stages: 1% → 5% → 25% → 50% → 100%
   Bake time: 30 min at each stage before promoting
   Storage: etcd or Spanner (needs strong consistency!)
   ```

2. **Traffic Splitting (Service Mesh)**
   ```
   How to route only 1% to new version?
   - Istio VirtualService with weighted routing
   - Or: K8s Deployment with 1 new pod per 99 old pods
   
   Your angle: "At Red Hat, our K8s Operator reconciled pod counts 
   to achieve desired replica distribution."
   ```

3. **Metrics Pipeline**
   ```
   What to measure:
   - Error rate: 5xx responses / total requests
   - Latency: p50, p95, p99
   - Resource usage: CPU, memory
   
   Compare: Canary metrics vs Baseline (current prod)
   
   Key insight: Don't just check "is error rate < 1%"
   Check: "is canary error rate WORSE than baseline?"
   Because baseline might already be at 0.5%.
   
   Your angle: "Similar to our LLM-as-judge evaluation pipeline — 
   we compare new RAG pipeline against baseline on faithfulness 
   and answer correctness metrics."
   ```

4. **Decision Engine (Auto-rollback logic)**
   ```
   Rules:
   - If error_rate(canary) > error_rate(baseline) + threshold: ROLLBACK
   - If latency_p99(canary) > latency_p99(baseline) * 1.2: ROLLBACK
   - If no issues after bake time: PROMOTE
   
   Default to rollback on uncertainty (safety first).
   
   Your angle: "Like our MCP validators at Red Hat — when in doubt, 
   reject. Better to block a good deploy than ship a bad one."
   ```

**Failure modes:**
- "What if metrics pipeline goes down during rollout?"
  → PAUSE rollout. Never promote blind. Alert on-call.
- "What if a rollout looks fine at 1% but breaks at 50%?"
  → Some bugs are load-dependent (race conditions, resource exhaustion).
     That's why we have multiple stages with bake time.
- "What if two services need to roll out together?"
  → Dependency tracking. Build a DAG of service dependencies.
     Use topological sort to determine safe rollout order.
     **Your angle:** "Exactly like Course Schedule II (LC 210) — detecting 
     cycles and ordering nodes."

**Scaling:**
- Multi-region: roll out to one canary region first (e.g., us-west-test), then expand region by region
- Thousands of services: shard the Rollout Controller by service or use a distributed work queue

---

### Design 2: ★★★ RAG (Retrieval-Augmented Generation) System

**Why this is critical:** You literally built this at Red Hat. This is your strongest system design answer.

**Requirements:**
- Query volume: 100 QPS? 10K QPS?
- Corpus size: 10K docs? 10M docs?
- Latency target: <500ms end-to-end?
- Security: can users see all docs or need filtering?

**High-level architecture:**

```
┌──────────┐
│  User    │ asks question
└────┬─────┘
     ↓
┌─────────────────┐
│   API Gateway   │  (auth, rate limit)
└────┬────────────┘
     ↓
┌─────────────────┐
│  Query Service  │
└────┬────────────┘
     │
     ├──→ (1) Generate embedding
     │        │
     │        ↓
     │   ┌──────────────┐
     │   │  LLM / Embed │
     │   │   Service    │
     │   └──────────────┘
     │
     ├──→ (2) Retrieve context
     │        │
     │        ↓
     │   ┌──────────────┐      ┌─────────────┐
     │   │ Vector DB    │←─────│  Document   │
     │   │ (FAISS/Solr) │      │  Indexer    │
     │   └──────────────┘      └─────────────┘
     │
     └──→ (3) Generate answer
              │
              ↓
         ┌──────────────┐
         │ LLM Service  │
         │ (GPT/Llama)  │
         └──────────────┘
              │
              ↓
         ┌──────────────┐
         │ MCP Validate │ ← guardrails!
         └──────────────┘
              │
              ↓
         Return to user
```

**Deep dive:**

1. **Vector Database**
   ```
   Why vector DB: enables semantic search (not just keyword matching)
   
   Options:
   - FAISS: fast, in-memory, single-node → your choice for dev/test
   - Solr with vector plugin: distributed, prod-ready
   - Pinecone/Weaviate: managed, scales automatically
   
   Your angle: "At Red Hat, we used FAISS for local dev and Solr-based 
   Offline Knowledge Portal (OKP) for production because it integrated 
   with our existing OpenStack docs infrastructure."
   
   Trade-off: FAISS is faster but single-node. Solr is distributed but 
   adds operational complexity.
   ```

2. **Document Ingestion Pipeline**
   ```
   ┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────────┐
   │Raw Docs  │──────→│ Chunk    │──────→│ Embed    │──────→│ Index    │
   │(SME notes│       │(512 token│       │(vector)  │       │(vector DB│
   │ Markdown)│       │  chunks) │       │          │       │         )│
   └──────────┘       └──────────┘       └──────────┘       └──────────┘
   
   Chunking strategy matters!
   - Too small: lose context
   - Too large: retrieval becomes noisy
   - Your choice: 512 tokens with 50-token overlap (sliding window)
   
   Your angle: "We automated this in lightspeed-rag-content with a CI 
   pipeline that re-indexes on every commit to the docs repo."
   ```

3. **MCP Guardrails (Security Layer)**
   ```
   Before returning AI output:
   - Question validator: is query allowed? (no jailbreaks, PII requests)
   - Redactor: strip sensitive info from context/answer
   - Summarizer: ensure answer fits token limits
   
   Your angle: "At Red Hat, we enforced these at the provider level 
   in lightspeed-providers to ensure zero compliance violations even 
   if the LLM hallucinated sensitive info."
   
   Why provider-level: enforcement happens BEFORE output reaches user, 
   not as post-processing (defense in depth).
   ```

4. **LLM-as-Judge Evaluation**
   ```
   How to know if RAG is working?
   
   Metrics:
   - Faithfulness: does answer reflect retrieved context? (not hallucinated)
   - Context recall: did we retrieve the right docs?
   - Context precision: how much retrieved context was actually used?
   - Answer correctness: compared to ground truth (if available)
   
   Your angle: "We built an automated eval pipeline that runs on every 
   rag-content update, scoring with an LLM judge. This catches regressions 
   before they reach production — integrated into CI/CD as a quality gate."
   
   Implementation: GPT-4 as judge with structured scoring rubric.
   ```

**Failure modes:**
- "Vector DB down?"
  → Fallback to keyword search (Elasticsearch). Degraded but available.
- "LLM service rate-limited?"
  → Queue requests, show "please wait" to user. Or use cheaper/faster model for overflow.
- "Retrieved context is wrong?"
  → This is the hardest problem. Improve with better chunking, hybrid search (vector + keyword), or query rewriting.

**Scaling:**
- 10K QPS: horizontally scale query service, shard vector DB, cache embeddings (same query → same embedding)
- Multi-region: replicate vector DB to each region for low latency

---

### Design 3: ★★ Monitoring & Alerting System

**Why this is critical:** Both roles care deeply about observability. You've built this.

**Requirements:**
- How many services to monitor?
- Metric granularity: per-second? per-minute?
- Alert latency: how fast must we detect issues?
- Retention: how long to store metrics?

**High-level architecture:**

```
┌─────────────┐  metrics      ┌──────────────────┐
│  Services   │──────────────→│  Metrics         │
│  (emit      │   (push/pull) │  Collection      │
│   metrics)  │               │  (Prometheus)    │
└─────────────┘               └────────┬─────────┘
                                       │
                                       ↓ scrape & store
                              ┌────────────────────┐
                              │  Time-Series DB    │
                              │  (Prometheus TSDB) │
                              └────────┬───────────┘
                                       │
                   ┌───────────────────┼───────────────────┐
                   ↓                   ↓                   ↓
            ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
            │  Alerting    │   │  Dashboards  │   │  Long-term   │
            │  (Alert Mgr) │   │  (Grafana)   │   │  Storage     │
            └──────┬───────┘   └──────────────┘   │  (Thanos/    │
                   │                               │   Cortex)    │
                   ↓                               └──────────────┘
            ┌──────────────┐
            │  Incident    │
            │  Management  │
            │  (PagerDuty) │
            └──────────────┘
```

**Deep dive:**

1. **Metrics Collection**
   ```
   Push vs Pull:
   
   PUSH (services send metrics):
     ✓ Simple for services
     ✗ Collector can be overwhelmed
     → Use: StatsD, CloudWatch
   
   PULL (Prometheus scrapes services):
     ✓ Collector controls rate
     ✓ Service discovery built-in (K8s)
     ✗ Services must expose /metrics endpoint
     → Your choice at Red Hat (Prometheus)
   
   Your angle: "Prometheus pull model fit our K8s environment — the 
   Operator auto-configured scrape targets via service discovery, 
   no manual config needed when scaling pods."
   ```

2. **Alerting Rules**
   ```
   Example rule (PromQL):
   
   ALERT HighErrorRate
     IF rate(http_requests_total{status=~"5.."}[5m]) > 0.05
     FOR 10m
     LABELS { severity="critical" }
     ANNOTATIONS {
       summary="High error rate on {{ $labels.service }}"
     }
   
   Key: the FOR clause prevents flapping (must be true for 10min).
   
   Your angle: "For rollout monitoring, we'd compare canary vs baseline:
   rate(errors{version='canary'}) > rate(errors{version='stable'}) * 1.2"
   ```

3. **Alert Routing (Fan-out)**
   ```
   Different severity → different channels:
   - Critical: PagerDuty (wakes someone up)
   - Warning: Slack
   - Info: Email
   
   Grouping: batch related alerts (don't send 100 separate pages 
   for 100 pods crashing — send 1 alert: "pod crash rate high")
   
   Silencing: during deployments, silence expected alerts
   ```

**Failure modes:**
- "Prometheus server down?"
  → Run multiple Prometheus instances, federated setup
- "Alert storm (1000s of alerts)?"
  → Grouping + rate limiting. Alert on "alert rate too high" (meta-alert)
- "Metrics storage full?"
  → Retention policy (keep 30 days locally, archive to object storage)

**Scaling:**
- Use Thanos or Cortex for multi-cluster aggregation
- Shard by service or region

---

### Design 4: ★★ Rate Limiter

**Why this is critical:** Overlaps with OOP round (you have code in `02_OOP_LLD_GUIDE.py`) but system design adds distributed angle.

**Algorithms to know:**

1. **Token Bucket**
   ```
   Bucket holds N tokens, refills at R tokens/second.
   Request consumes 1 token. If bucket empty → reject.
   
   Allows bursts (up to N) but rate-limited long-term.
   ```

2. **Sliding Window**
   ```
   Track timestamps of last N requests.
   On new request: count requests in last T seconds.
   If count < limit → allow, else reject.
   
   More accurate but more expensive (need to store timestamps).
   ```

**Distributed rate limiting:**

```
┌─────────┐       ┌─────────┐       ┌─────────┐
│ Server1 │       │ Server2 │       │ Server3 │
└────┬────┘       └────┬────┘       └────┬────┘
     │                 │                 │
     └─────────────────┼─────────────────┘
                       ↓
                ┌──────────────┐
                │    Redis     │  ← centralized counter
                │  (atomic ops)│
                └──────────────┘

Commands:
  INCR user:123:count
  EXPIRE user:123:count 60

If count > limit → reject
```

**Trade-off:**
- Centralized (Redis): accurate but single point of failure, network latency
- Local (in-memory): fast but can't enforce global limits across servers

**Your angle:** "For API throttling in the AI system, we'd use Redis with atomic INCR to enforce per-user limits globally, ensuring one user can't overwhelm the LLM service even if requests hit different pods."

---

### Design 5: ★ Distributed Task Scheduler

**Requirements:**
- How many tasks/second?
- Do tasks have dependencies?
- Do tasks need to run exactly once or at-least-once?

**High-level:**

```
┌──────────┐       ┌──────────────┐       ┌──────────┐
│ Clients  │──────→│  Task Queue  │──────→│ Workers  │
│          │       │  (Kafka/SQS) │       │ (N pods) │
└──────────┘       └──────────────┘       └──────────┘
                                                 │
                                                 ↓
                                          ┌──────────┐
                                          │  Result  │
                                          │  Store   │
                                          └──────────┘
```

**Key decisions:**
- Queue: Kafka (high throughput, replay) vs SQS (managed, simpler)
- Workers: stateless, auto-scale based on queue depth
- Idempotency: tasks may run >1x due to retries → must be idempotent

**Your angle (Kubernetes Operator):** "The reconciliation loop in our lightspeed-operator is essentially a task scheduler — K8s watches for events (create/update/delete), queues reconciliation tasks, and workers (operator pods) process them idempotently."

---

### Design 6: ★ Notification System

**Your angle:** Directly maps to rollout alerting.

**Requirements:**
- Channels: Email, SMS, Slack, Push?
- Volume: 100 notifications/sec? 100K/sec?
- User preferences: can users opt-out of channels?

**High-level:**

```
┌────────────┐       ┌────────────────┐
│  Trigger   │──────→│ Notification   │
│  (event)   │       │ Service        │
└────────────┘       └────────┬───────┘
                              │
         ┌────────────────────┼────────────────┐
         ↓                    ↓                ↓
  ┌──────────┐        ┌──────────┐     ┌──────────┐
  │  Email   │        │   SMS    │     │  Slack   │
  │ Provider │        │ Provider │     │ Provider │
  └──────────┘        └──────────┘     └──────────┘

Template: "Deployment {{ service }} failed in {{ region }}"
Preferences: Check user's channel preferences before sending
Retry: If SMS fails, retry with backoff, eventually DLQ
```

**Your angle:** "For rollout failures, we'd publish an event to a message queue (Pub/Sub), the notification service consumes it, expands the template with rollout metadata, and fans out to configured channels — similar to our MCP architecture where events flow through a provider layer."

---

## PART 5: Your Resume → System Design Talking Points

Map every project on your CV to a system design talking point:

| Resume Item | System Design Hook |
|---|---|
| **RAG pipelines with vector DBs** | "When you asked about search, this is exactly what I built at Red Hat — here's how we chose FAISS vs Solr..." |
| **Kubernetes Operator** | "This is a distributed reconciliation loop — essentially event-driven task scheduling with retries and state management..." |
| **LLM-as-judge eval pipeline** | "For quality gates, we used LLM scoring in CI/CD — same pattern as A/B testing in rollouts: compare metrics before promoting..." |
| **MCP security guardrails** | "When you mentioned content moderation, this maps directly to our provider-level validators — defense in depth, fail-safe defaults..." |
| **ELK/Prometheus/Grafana** | "For monitoring, we used Prometheus pull model with Grafana dashboards — here's how we handled multi-cluster aggregation..." |
| **TLS/SSL upstream contribution** | "For security, I contributed TLS config to the PostgreSQL storage layer — defense in depth, encrypt at rest and in transit..." |
| **Drone HitL failover** | "This taught me state machines and graceful degradation — same pattern as rollout states: canary → rolling → complete, with safe fallbacks..." |

**Strategy:** Every time the interviewer asks "have you built something like this?" — the answer is YES, and you can point to your resume.

---

## PART 6: Common Follow-up Questions

### "How would you scale this to 10x traffic?"
Template answer:
1. Horizontal scaling (add more servers)
2. Identify bottlenecks (DB? Cache? CPU?)
3. Shard/partition if needed (by user ID, region, etc.)
4. Add caching layer
5. Async processing for non-critical paths

### "What if [component X] fails?"
Always talk about:
- **Redundancy** (multiple instances)
- **Graceful degradation** (serve cached/stale data rather than failing completely)
- **Monitoring** (alert when failure detected)
- **Automatic recovery** (retry, circuit breaker, failover)

Your angle: "Like our MCP validators — if validation service is down, we fail closed (reject request) rather than serve unvalidated AI output. Safety over availability."

### "How would you monitor this?"
Always mention:
- **Golden signals**: Latency, Traffic, Errors, Saturation
- **Metrics**: specific to the system (e.g., rollout error rate delta)
- **Alerts**: critical vs warning, routing
- **Dashboards**: what the on-call engineer sees

Your angle: "I'd use Prometheus for metrics collection with Grafana dashboards, similar to our Red Hat stack. For rollouts, key metrics are error rate, latency p99, and rollback rate."

---

## PART 7: Dos and Don'ts

### ✅ DO

- **Start with requirements** — never jump straight to drawing
- **Think out loud** — the interviewer is evaluating your thought process, not just the final diagram
- **Draw diagrams** — even in virtual interviews, use a shared doc/whiteboard
- **Acknowledge trade-offs** — "We could use X, which is faster, or Y, which is more consistent..."
- **Connect to your experience** — "This is similar to what I built at Red Hat when..."
- **Ask for feedback mid-design** — "Does this approach make sense so far?"
- **Be honest about what you don't know** — "I haven't used Cassandra in production, but I understand it's AP with eventual consistency..."

### ❌ DON'T

- **Don't assume requirements** — "Should we support multi-region?" not "We'll do multi-region"
- **Don't over-engineer** — L3/IC2 design doesn't need to handle Google-scale immediately
- **Don't memorize one design and try to fit every problem to it**
- **Don't go deep on irrelevant details** — if interviewer hasn't asked about caching, don't spend 10 min on cache invalidation strategies
- **Don't say "I'd just use AWS service X"** — show you understand what's under the hood
- **Don't panic if you get stuck** — ask clarifying questions to get unstuck

---

## PART 8: Practice Plan

1. **Draw these 6 systems from memory** (without looking at this guide):
   - Canary deployment system
   - RAG pipeline
   - Monitoring & alerting
   - Rate limiter
   - Distributed task scheduler
   - Notification system

2. **For each, practice explaining out loud** as if to an interviewer

3. **Prepare your "experience hooks"** — for each system, have a 30-second story from your Red Hat work ready

4. **Mock interview yourself** — set a 45-min timer, pick a system, go through the full framework

---

## PART 9: Resources

**Books:**
- "Designing Data-Intensive Applications" by Martin Kleppmann (THE bible)
- "System Design Interview" by Alex Xu (Vol 1 & 2)

**YouTube:**
- ByteByteGo (Alex Xu's channel) — animated system design
- System Design Interview channel

**Practice:**
- Draw each system on paper/whiteboard
- Explain to a friend or record yourself
- Time yourself (45 min strict limit)

---

## Final Advice

**You're not being tested on "have you memorized every distributed system pattern."**

**You're being tested on:**
1. Can you gather requirements thoughtfully?
2. Can you reason about trade-offs?
3. Can you articulate what you've actually built?
4. Can you think about failure modes and scale?

**Your Red Hat experience gives you real production systems to reference.** Most candidates study theory; you've shipped code. Use that advantage.

When in doubt, connect back to what you know. "This reminds me of our RAG pipeline where we had to balance latency vs accuracy..." is infinitely better than trying to fake expertise in a system you've never touched.

Good luck! 🚀
