"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          OOP + LOW-LEVEL DESIGN (LLD) INTERVIEW MASTER GUIDE               ║
║          Omkar Joshi — Google / Microsoft prep                             ║
║                                                                            ║
║  This round tests: Can you model a real-world problem as clean classes?    ║
║  Not DSA (algorithms), not HLD (servers/databases/scale) — this is about   ║
║  CLASS DESIGN: objects, relationships, interfaces, and extensibility.      ║
╚══════════════════════════════════════════════════════════════════════════════╝

WHAT THIS ROUND ACTUALLY EVALUATES:
    1. Do you know core OOP principles and can apply them (not just define them)?
    2. Can you translate ambiguous requirements into classes/interfaces?
    3. Is your design extensible? (What if we add a new payment type tomorrow?)
    4. Do you use design patterns appropriately (not shoehorned in)?
    5. Can you write actual working class skeletons, not just boxes on a diagram?
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PART 1: THE FOUR PILLARS OF OOP (Know cold — always the opening question)   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
1. ENCAPSULATION
   Bundling data + methods together, hiding internal state from outside access.
   "Protect the object's internal state; expose only what's necessary."

2. ABSTRACTION
   Hiding complex implementation details behind a simple interface.
   "You know WHAT a car does (drive, brake). You don't need to know HOW the
    engine works internally to drive it."

3. INHERITANCE
   A class can inherit attributes/methods from a parent class.
   "A Dog IS-A Animal. Dog inherits Animal's traits, adds its own."

4. POLYMORPHISM
   Same interface, different implementations depending on the object type.
   "Different shapes all have area(), but each computes it differently."
"""

FOUR_PILLARS_CODE = '''
from abc import ABC, abstractmethod

# ── ENCAPSULATION ──
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance          # double underscore = "private" (name-mangled)

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):                # controlled access via method
        return self.__balance
    # External code CANNOT do account.__balance = 999999 directly


# ── ABSTRACTION ──
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass                                # caller doesn't know/care HOW payment works

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Charging ${amount} to credit card")

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Charging ${amount} via PayPal")


# ── INHERITANCE ──
class Animal:
    def __init__(self, name):
        self.name = name
    def make_sound(self):
        raise NotImplementedError

class Dog(Animal):                         # Dog IS-A Animal
    def make_sound(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def make_sound(self):
        return f"{self.name} says Meow!"


# ── POLYMORPHISM ──
animals = [Dog("Rex"), Cat("Whiskers")]
for animal in animals:
    print(animal.make_sound())             # same method call, different behavior
    # Rex says Woof!
    # Whiskers says Meow!
'''


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PART 2: SOLID PRINCIPLES (Interviewers WILL ask you to name and apply these) ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
S — Single Responsibility Principle
    A class should have ONE reason to change.
    BAD: A User class that handles user data AND sends emails AND logs to DB.
    GOOD: User, EmailService, UserRepository — each with one job.

O — Open/Closed Principle
    Open for extension, closed for modification.
    You should be able to ADD new behavior without changing existing code.
    Example: Adding a new PaymentMethod shouldn't require editing PaymentProcessor.
    → This is why we use interfaces/abstract base classes + polymorphism.

L — Liskov Substitution Principle
    Subclasses must be substitutable for their base class without breaking things.
    CLASSIC VIOLATION: Square extends Rectangle, but setWidth() behaves
    differently — breaks code expecting Rectangle behavior.

I — Interface Segregation Principle
    Don't force a class to implement methods it doesn't need.
    BAD: One fat "Worker" interface with work() and eat() —
         a Robot worker shouldn't be forced to implement eat().
    GOOD: Split into Workable and Eatable interfaces.

D — Dependency Inversion Principle
    Depend on abstractions, not concrete implementations.
    BAD: class Car: def __init__(self): self.engine = GasEngine()
    GOOD: class Car: def __init__(self, engine: Engine): self.engine = engine
    → This enables testing with mocks and swapping implementations easily.
"""

SOLID_CODE_EXAMPLE = '''
# DEPENDENCY INVERSION — a favorite interview probe
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class EmailSender(NotificationSender):
    def send(self, message: str):
        print(f"Email: {message}")

class SMSSender(NotificationSender):
    def send(self, message: str):
        print(f"SMS: {message}")

class NotificationService:
    def __init__(self, sender: NotificationSender):   # depends on ABSTRACTION
        self.sender = sender

    def notify(self, message: str):
        self.sender.send(message)

# Usage: swap implementations without changing NotificationService
service = NotificationService(EmailSender())
service.notify("Hello!")
service = NotificationService(SMSSender())   # easy to swap
'''


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PART 3: DESIGN PATTERNS — THE 10 YOU MUST KNOW                             ║
# ║  Don't just memorize definitions — know WHEN to use each and WHY.            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

DESIGN_PATTERNS = {
    # ─────────────────────────────────────────────
    "Singleton": {
        "category": "Creational",
        "priority": "★★★",
        "when_to_use": "Exactly ONE instance needed globally (config manager, logger, connection pool)",
        "why": "Prevents multiple conflicting instances of a shared resource",
        "code": '''
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Usage
a = Singleton()
b = Singleton()
assert a is b   # same object
        ''',
        "interview_trap": "Interviewers may ask: 'Is this thread-safe?' → mention locks needed for multithreaded use",
    },

    # ─────────────────────────────────────────────
    "Factory Method": {
        "category": "Creational",
        "priority": "★★★",
        "when_to_use": "Object creation logic is complex or depends on runtime input; you want to decouple 'what to create' from 'how it's used'",
        "why": "Client code doesn't need to know concrete classes — only the interface",
        "code": '''
class Shape(ABC):
    @abstractmethod
    def draw(self): pass

class Circle(Shape):
    def draw(self): return "Drawing Circle"

class Square(Shape):
    def draw(self): return "Drawing Square"

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str) -> Shape:
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        raise ValueError("Unknown shape")

shape = ShapeFactory.create_shape("circle")
print(shape.draw())
        ''',
        "role_relevance": "ROLLOUTS/AI TRUST: creating different validator/redactor instances based on config",
    },

    # ─────────────────────────────────────────────
    "Builder": {
        "category": "Creational",
        "priority": "★★",
        "when_to_use": "Object has MANY optional parameters/constructor is getting unwieldy",
        "why": "Avoids telescoping constructors (Class(a, b, None, None, True, None, ...))",
        "code": '''
class Pizza:
    def __init__(self):
        self.toppings = []
        self.size = None

    def __str__(self):
        return f"{self.size} pizza with {self.toppings}"

class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size):
        self.pizza.size = size
        return self                      # enables chaining

    def add_topping(self, topping):
        self.pizza.toppings.append(topping)
        return self

    def build(self):
        return self.pizza

pizza = (PizzaBuilder()
         .set_size("Large")
         .add_topping("Cheese")
         .add_topping("Mushroom")
         .build())
        ''',
    },

    # ─────────────────────────────────────────────
    "Observer": {
        "category": "Behavioral",
        "priority": "★★★",
        "when_to_use": "One-to-many dependency — when one object changes, all dependents should be notified",
        "why": "Decouples the subject from its observers",
        "code": '''
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

class Observer(ABC):
    @abstractmethod
    def update(self, event): pass

class Logger(Observer):
    def update(self, event):
        print(f"Logging event: {event}")

class AlertSystem(Observer):
    def update(self, event):
        print(f"Alerting on: {event}")

subject = Subject()
subject.attach(Logger())
subject.attach(AlertSystem())
subject.notify("Deployment failed")   # both observers react
        ''',
        "role_relevance": "ROLLOUTS: monitoring system notifying multiple alerting/logging subsystems on rollout events",
    },

    # ─────────────────────────────────────────────
    "Strategy": {
        "category": "Behavioral",
        "priority": "★★★",
        "when_to_use": "Multiple interchangeable algorithms for the same task, selectable at runtime",
        "why": "Avoids giant if/elif chains; each algorithm is isolated and testable",
        "code": '''
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): pass

class QuickSort(SortStrategy):
    def sort(self, data): return sorted(data)   # simplified

class BubbleSort(SortStrategy):
    def sort(self, data):
        data = data.copy()
        n = len(data)
        for i in range(n):
            for j in range(n - i - 1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy.sort(data)

sorter = Sorter(QuickSort())
print(sorter.sort([3, 1, 2]))
        ''',
        "role_relevance": "ROLLOUTS: swapping rollout strategies (canary vs blue-green) at runtime",
    },

    # ─────────────────────────────────────────────
    "Decorator": {
        "category": "Structural",
        "priority": "★★",
        "when_to_use": "Add behavior to objects dynamically without modifying their class",
        "why": "Avoids subclass explosion when combining multiple optional behaviors",
        "code": '''
class Coffee(ABC):
    @abstractmethod
    def cost(self): pass

class SimpleCoffee(Coffee):
    def cost(self): return 2.0

class MilkDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self):
        return self._coffee.cost() + 0.5

class SugarDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self):
        return self._coffee.cost() + 0.2

coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))
print(coffee.cost())   # 2.7 — layered behavior
        ''',
    },

    # ─────────────────────────────────────────────
    "Adapter": {
        "category": "Structural",
        "priority": "★★",
        "when_to_use": "Making incompatible interfaces work together (e.g., integrating a 3rd-party library)",
        "why": "Lets you use existing code with a new interface without modifying the original",
        "code": '''
class OldPrinter:
    def print_old(self, text):
        print(f"[OLD] {text}")

class NewPrinterInterface(ABC):
    @abstractmethod
    def print(self, text): pass

class PrinterAdapter(NewPrinterInterface):
    def __init__(self, old_printer: OldPrinter):
        self.old_printer = old_printer

    def print(self, text):
        self.old_printer.print_old(text)   # adapts old interface to new

adapter = PrinterAdapter(OldPrinter())
adapter.print("Hello")   # works with new interface
        ''',
        "role_relevance": "Directly relevant to your Red Hat work — adapting FAISS/Solr vector stores to a common interface",
    },

    # ─────────────────────────────────────────────
    "Command": {
        "category": "Behavioral",
        "priority": "★★",
        "when_to_use": "Encapsulate a request as an object — enables undo/redo, queuing, logging of operations",
        "why": "Decouples the object invoking the operation from the one performing it",
        "code": '''
class Command(ABC):
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def undo(self): pass

class Light:
    def turn_on(self): print("Light ON")
    def turn_off(self): print("Light OFF")

class TurnOnCommand(Command):
    def __init__(self, light): self.light = light
    def execute(self): self.light.turn_on()
    def undo(self): self.light.turn_off()

class RemoteControl:
    def __init__(self):
        self.history = []

    def press(self, command: Command):
        command.execute()
        self.history.append(command)

    def press_undo(self):
        if self.history:
            self.history.pop().undo()
        ''',
        "role_relevance": "ROLLOUTS: encapsulating rollback operations as commands",
    },

    # ─────────────────────────────────────────────
    "State": {
        "category": "Behavioral",
        "priority": "★★★",
        "when_to_use": "Object behavior changes based on internal state (state machines)",
        "why": "Avoids giant if/elif on a 'status' field scattered across the codebase",
        "code": '''
class RolloutState(ABC):
    @abstractmethod
    def advance(self, context): pass

class CanaryState(RolloutState):
    def advance(self, context):
        print("Canary healthy, promoting to Rolling")
        context.state = RollingState()

class RollingState(RolloutState):
    def advance(self, context):
        print("Rolling complete, promoting to Complete")
        context.state = CompleteState()

class CompleteState(RolloutState):
    def advance(self, context):
        print("Already complete")

class Rollout:
    def __init__(self):
        self.state = CanaryState()

    def advance(self):
        self.state.advance(self)
        ''',
        "role_relevance": "THIS IS THE ROLLOUT SYSTEM PATTERN — canary → rolling → complete state machine",
    },

    # ─────────────────────────────────────────────
    "Facade": {
        "category": "Structural",
        "priority": "★",
        "when_to_use": "Provide a simple interface to a complex subsystem",
        "why": "Hides complexity of multiple interacting classes behind one simple API",
        "code": '''
class CPU:
    def freeze(self): print("CPU frozen")
    def jump(self, pos): print(f"Jump to {pos}")
    def execute(self): print("Executing")

class Memory:
    def load(self, pos, data): print(f"Loading {data} at {pos}")

class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()

    def start(self):                       # simple interface
        self.cpu.freeze()
        self.memory.load(0, "boot data")
        self.cpu.jump(0)
        self.cpu.execute()

computer = ComputerFacade()
computer.start()    # caller doesn't deal with CPU/Memory directly
        ''',
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PART 4: THE LLD INTERVIEW FRAMEWORK — Use this structure EVERY TIME         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
Most candidates fail LLD not because they don't know OOP, but because they
jump straight to coding without gathering requirements. Follow this framework:

STEP 1: CLARIFY REQUIREMENTS (3-5 min) — DON'T SKIP THIS
    - "What are the core features we need to support?"
    - "What's explicitly OUT of scope?"
    - "Any specific constraints? (concurrency, persistence, scale)"
    - Write down a short feature list before touching classes.

STEP 2: IDENTIFY CORE ENTITIES / NOUNS (3-5 min)
    - Extract the nouns from the problem: "ParkingLot has Spots, Vehicles, Tickets"
    - These become your candidate classes.
    - Identify relationships: IS-A (inheritance) vs HAS-A (composition)

STEP 3: DEFINE RELATIONSHIPS & INTERFACES (5 min)
    - Draw out class relationships (verbally or on whiteboard/doc)
    - Identify what should be abstract (interface) vs concrete
    - Ask: "What's likely to change or be extended?" → make THAT flexible

STEP 4: WRITE CLASS SKELETONS (15-20 min)
    - Start with class names, key attributes, method signatures
    - Add methods incrementally, explaining as you go
    - Use design patterns WHERE THEY FIT NATURALLY (don't force them)

STEP 5: WALK THROUGH A SCENARIO (5 min)
    - Trace through your design with a concrete example
    - "A car enters, requests a spot, gets assigned, ticket created..."
    - This catches gaps in your design

STEP 6: DISCUSS EXTENSIBILITY / TRADE-OFFS (5 min)
    - "What if we added electric vehicle charging spots?"
    - "What if pricing rules become more complex?"
    - Show your design handles change gracefully (Open/Closed Principle)
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PART 5: THE 12 CLASSIC LLD PROBLEMS — Practice these end-to-end             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

LLD_PROBLEMS = {
    # ─────────────────────────────────────────────
    "Parking Lot System": {
        "priority": "★★★",
        "core_entities": ["ParkingLot", "ParkingSpot", "Vehicle", "Ticket", "PaymentProcessor"],
        "key_design_decisions": """
            - Vehicle types (Car, Motorcycle, Truck) → inheritance from base Vehicle
            - Spot types (Compact, Large, Handicapped) → Strategy for spot-matching
            - ParkingLot manages spots, uses Factory to find available spot
            - Ticket tracks entry time, spot, vehicle → used for fee calculation
            - Fee calculation → Strategy pattern (hourly, flat-rate, etc.)
        """,
        "patterns_used": ["Factory (spot assignment)", "Strategy (fee calculation)", "Singleton (ParkingLot instance)"],
        "extensibility_probe": "What if we add EV charging spots? → New SpotType + Strategy, no core changes needed",
    },

    # ─────────────────────────────────────────────
    "Elevator System": {
        "priority": "★★★",
        "core_entities": ["Elevator", "ElevatorController", "Request", "Floor", "Button"],
        "key_design_decisions": """
            - Elevator has state: IDLE, MOVING_UP, MOVING_DOWN, DOOR_OPEN
              → STATE PATTERN fits perfectly
            - ElevatorController decides which elevator responds to a request
              (scheduling algorithm — e.g., nearest elevator, SCAN algorithm)
            - Requests: internal (button pressed inside) vs external (floor call)
        """,
        "patterns_used": ["State (elevator status)", "Observer (notify floor displays)", "Strategy (scheduling algorithm)"],
        "extensibility_probe": "What if we add express elevators (skip certain floors)? → New scheduling Strategy",
    },

    # ─────────────────────────────────────────────
    "Library Management System": {
        "priority": "★★",
        "core_entities": ["Book", "BookItem", "Library", "Member", "Librarian", "Reservation"],
        "key_design_decisions": """
            - Book (metadata) vs BookItem (physical copy) — important distinction!
            - Member can borrow, reserve, return books
            - Track due dates, fines for late returns
            - Search: by title, author, ISBN → could use a simple index/hash map
        """,
        "patterns_used": ["Observer (notify when reserved book available)", "Factory (creating different member types)"],
    },

    # ─────────────────────────────────────────────
    "Vending Machine": {
        "priority": "★★★",
        "core_entities": ["VendingMachine", "Product", "Inventory", "PaymentProcessor", "State"],
        "key_design_decisions": """
            - Classic STATE PATTERN interview question:
              States: Idle, HasMoney, Dispensing, OutOfStock
            - Each state defines valid transitions
              (can't dispense product without payment first)
        """,
        "patterns_used": ["State (machine status)", "Strategy (payment methods)"],
        "sample_code": '''
class VendingMachineState(ABC):
    @abstractmethod
    def insert_coin(self, machine): pass
    @abstractmethod
    def select_product(self, machine): pass
    @abstractmethod
    def dispense(self, machine): pass

class IdleState(VendingMachineState):
    def insert_coin(self, machine):
        print("Coin accepted")
        machine.state = HasMoneyState()
    def select_product(self, machine):
        print("Insert coin first")
    def dispense(self, machine):
        print("Insert coin first")

class HasMoneyState(VendingMachineState):
    def insert_coin(self, machine):
        print("Already has coin")
    def select_product(self, machine):
        print("Product selected")
        machine.state = DispensingState()
    def dispense(self, machine):
        print("Select product first")

class DispensingState(VendingMachineState):
    def insert_coin(self, machine):
        print("Please wait, dispensing")
    def select_product(self, machine):
        print("Already dispensing")
    def dispense(self, machine):
        print("Dispensing product...")
        machine.state = IdleState()

class VendingMachine:
    def __init__(self):
        self.state = IdleState()
        ''',
    },

    # ─────────────────────────────────────────────
    "Movie Ticket Booking System (BookMyShow)": {
        "priority": "★★★",
        "core_entities": ["Movie", "Show", "Screen", "Theater", "Seat", "Booking", "Payment"],
        "key_design_decisions": """
            - CONCURRENCY IS THE KEY CHALLENGE: two users booking the same seat
              simultaneously → need locking mechanism (pessimistic lock on seat,
              or optimistic with version numbers)
            - Seat has states: AVAILABLE, LOCKED (temp hold), BOOKED
            - Booking has expiry — if payment not completed in N minutes,
              release the lock (State pattern again)
        """,
        "patterns_used": ["State (seat status)", "Observer (notify on booking confirm)", "Singleton (theater inventory)"],
        "interview_trap": "Interviewers WILL probe concurrency — mention locks, or 'reserve then confirm' 2-phase flow",
    },

    # ─────────────────────────────────────────────
    "LRU Cache (Design, not just algorithm)": {
        "priority": "★★★",
        "core_entities": ["LRUCache", "Node (doubly linked list)", "HashMap"],
        "key_design_decisions": """
            - This overlaps with DSA round but LLD interviewers want to see
              clean class design: separate Node class, clear get/put methods
            - Discuss thread-safety if asked: where would locks go?
        """,
        "patterns_used": ["N/A — pure data structure design"],
        "note": "You already have full implementation in 00_MASTER_DSA_LIST.py Problem 13",
    },

    # ─────────────────────────────────────────────
    "Chess Game": {
        "priority": "★★",
        "core_entities": ["Board", "Piece (King, Queen, Rook...)", "Player", "Move", "Game"],
        "key_design_decisions": """
            - Piece is abstract base class, each piece type overrides
              valid_moves() → POLYMORPHISM at its finest
            - Board tracks state, validates moves are legal
            - Game manages turns, check/checkmate detection
        """,
        "patterns_used": ["Strategy/Polymorphism (piece movement rules)", "Command (move history for undo)"],
    },

    # ─────────────────────────────────────────────
    "Rate Limiter": {
        "priority": "★★★",
        "core_entities": ["RateLimiter", "RateLimitStrategy", "Bucket/Window"],
        "key_design_decisions": """
            - Multiple algorithms possible: Token Bucket, Sliding Window,
              Fixed Window, Leaky Bucket → STRATEGY PATTERN
            - Per-user vs global rate limiting → key design decision
        """,
        "patterns_used": ["Strategy (algorithm choice)"],
        "role_relevance": "OVERLAPS WITH SYSTEM DESIGN — directly relevant to rollout/API throttling",
        "sample_code": '''
class RateLimitStrategy(ABC):
    @abstractmethod
    def allow_request(self, user_id): pass

class TokenBucketStrategy(RateLimitStrategy):
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = {}       # user_id -> current tokens
        self.refill_rate = refill_rate

    def allow_request(self, user_id):
        tokens = self.tokens.get(user_id, self.capacity)
        if tokens > 0:
            self.tokens[user_id] = tokens - 1
            return True
        return False

class RateLimiter:
    def __init__(self, strategy: RateLimitStrategy):
        self.strategy = strategy

    def is_allowed(self, user_id):
        return self.strategy.allow_request(user_id)
        ''',
    },

    # ─────────────────────────────────────────────
    "Splitwise (Expense Sharing)": {
        "priority": "★★",
        "core_entities": ["User", "Expense", "Group", "Balance", "SplitStrategy"],
        "key_design_decisions": """
            - Split types: Equal, Exact, Percentage → STRATEGY PATTERN
            - Balance sheet: who owes whom how much (graph-like structure)
            - Simplify debts algorithm (minimize transactions) — DSA + LLD overlap
        """,
        "patterns_used": ["Strategy (split calculation)", "Observer (notify group members)"],
    },

    # ─────────────────────────────────────────────
    "Notification System": {
        "priority": "★★★",
        "core_entities": ["NotificationService", "NotificationChannel", "User", "Template"],
        "key_design_decisions": """
            - Multiple channels: Email, SMS, Push → STRATEGY or simple polymorphism
            - Users have preferences on which channels to use
            - Template system for message formatting (Factory for template creation)
        """,
        "patterns_used": ["Strategy (channel selection)", "Observer (event-driven notifications)", "Factory (template creation)"],
        "role_relevance": "DIRECTLY relevant to ROLLOUTS/AI TRUST: alerting system for rollout failures across channels",
    },

    # ─────────────────────────────────────────────
    "Logging Framework": {
        "priority": "★★",
        "core_entities": ["Logger", "LogLevel", "LogAppender (Console/File/Network)", "LogFormatter"],
        "key_design_decisions": """
            - Chain of Responsibility for log level filtering
            - Multiple appenders can be active simultaneously (Observer-like)
            - Singleton for global logger instance
        """,
        "patterns_used": ["Singleton", "Chain of Responsibility", "Strategy (formatting)"],
        "role_relevance": "DIRECTLY relevant to your ELK stack experience at Red Hat",
    },

    # ─────────────────────────────────────────────
    "File System / Directory Structure": {
        "priority": "★★",
        "core_entities": ["FileSystemNode (abstract)", "File", "Directory"],
        "key_design_decisions": """
            - CLASSIC COMPOSITE PATTERN: Directory contains FileSystemNodes
              (which can be Files OR other Directories) — recursive structure
            - Operations like get_size() recurse naturally through composite
        """,
        "patterns_used": ["Composite (core pattern for this problem)"],
        "sample_code": '''
class FileSystemNode(ABC):
    @abstractmethod
    def get_size(self): pass

class File(FileSystemNode):
    def __init__(self, name, size):
        self.name = name
        self.size = size
    def get_size(self):
        return self.size

class Directory(FileSystemNode):
    def __init__(self, name):
        self.name = name
        self.children = []       # list of FileSystemNode (File or Directory)

    def add(self, node: FileSystemNode):
        self.children.append(node)

    def get_size(self):
        return sum(child.get_size() for child in self.children)   # recursive
        ''',
    },
}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PART 6: PYTHON-SPECIFIC OOP GOTCHAS INTERVIEWERS PROBE                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
Since you'll code in Python, know these — interviewers use them to test depth:

1. "What's the difference between __init__ and __new__?"
   __new__ creates the instance (rarely overridden except Singleton/metaclasses)
   __init__ initializes it after creation

2. "What's a classmethod vs staticmethod vs instance method?"
   instance method: self, operates on instance data
   @classmethod: cls, operates on class-level data, can be used as alt constructor
   @staticmethod: no self/cls, just lives in the class namespace for organization

3. "How does Python handle multiple inheritance?"
   MRO (Method Resolution Order) — C3 linearization algorithm
   class D(B, C): ... → Python checks D, then B, then C, then their parents

4. "What's duck typing?"
   "If it walks like a duck and quacks like a duck, it's a duck."
   Python doesn't require explicit interfaces — if an object has the right
   methods, it can be used interchangeably (relevant vs Java/C# formal interfaces)

5. "Abstract classes in Python?"
   Use `abc` module: ABC base class + @abstractmethod decorator
   Prevents instantiation of the abstract class directly

6. "Composition vs Inheritance — when to choose which?"
   Favor composition when relationship is HAS-A (Car has an Engine)
   Use inheritance when relationship is truly IS-A (Dog is an Animal)
   RULE OF THUMB: "Favor composition over inheritance" (classic GoF principle)
   Inheritance creates tight coupling; composition is more flexible
"""

OOP_GOTCHA_CODE = '''
# CLASSMETHOD AS ALTERNATE CONSTRUCTOR (commonly asked to demonstrate)
class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    @classmethod
    def margherita(cls):
        return cls(["mozzarella", "tomato"])       # alternate constructor

    @staticmethod
    def validate_ingredient(name):
        return name in ["cheese", "tomato", "mozzarella", "basil"]

pizza = Pizza.margherita()          # no need to know constructor details


# COMPOSITION OVER INHERITANCE EXAMPLE
# BAD (inheritance for code reuse, not IS-A relationship):
class Bird:
    def fly(self): pass
class Penguin(Bird):               # Penguin IS-A Bird, but CAN'T fly! Violates LSP
    def fly(self): raise Exception("Penguins can't fly")

# GOOD (composition):
class FlyBehavior(ABC):
    @abstractmethod
    def fly(self): pass

class CanFly(FlyBehavior):
    def fly(self): print("Flying!")

class CannotFly(FlyBehavior):
    def fly(self): print("Can't fly")

class Bird:
    def __init__(self, fly_behavior: FlyBehavior):
        self.fly_behavior = fly_behavior     # HAS-A fly behavior

    def perform_fly(self):
        self.fly_behavior.fly()

sparrow = Bird(CanFly())
penguin = Bird(CannotFly())        # no exception, no violated contract
'''


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PART 7: COMMON INTERVIEW QUESTIONS (Rapid-fire — be ready to answer fast)    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
"""
Q: Difference between abstraction and encapsulation?
A: Abstraction hides COMPLEXITY (what vs how). Encapsulation hides DATA
   (bundling + access control). Abstraction is about design; encapsulation
   is about implementation/protection.

Q: Can you have an abstract class with no abstract methods?
A: Yes in Python — ABC just prevents direct instantiation.

Q: What is method overloading vs overriding?
A: Overloading = same method name, different signatures (Python doesn't
   support this natively — use default args or *args).
   Overriding = subclass redefines a parent's method with same signature.

Q: What's a mixin?
A: A class designed to be combined with others via multiple inheritance,
   providing a specific piece of reusable functionality (not meant to
   stand alone). E.g., JSONSerializableMixin adding to_json() to any class.

Q: Diamond problem in multiple inheritance?
A: When two parent classes have a common ancestor, ambiguity in method
   resolution arises. Python resolves via MRO (C3 linearization).

Q: When would you use composition over inheritance?
A: When the relationship isn't truly IS-A, when you need runtime flexibility
   (swap behavior), or to avoid deep/fragile inheritance hierarchies.

Q: What's the difference between an interface and an abstract class?
   (Python doesn't have true interfaces, but conceptually:)
A: Abstract class can have some implemented methods + shared state.
   Interface (Protocol in Python) is a pure contract — no implementation.
   Python uses ABC for both; formally, `typing.Protocol` gives structural
   interfaces (duck-typing-friendly).
"""


if __name__ == "__main__":
    print("OOP + LLD MASTER GUIDE")
    print(f"\\nDesign Patterns covered: {len(DESIGN_PATTERNS)}")
    for name, info in DESIGN_PATTERNS.items():
        print(f"  {info['priority']} {name:20s} ({info['category']})")

    print(f"\\nLLD Problems covered: {len(LLD_PROBLEMS)}")
    for name, info in LLD_PROBLEMS.items():
        print(f"  {info['priority']} {name}")
