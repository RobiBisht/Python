"""
PYTHON OOP - COMPLETE NOTES (rearranged + missing topics added)

Order of topics:
  1.  Class & Object basics
  2.  Constructor, self, __str__ / __repr__
  3.  Instance vs Class variables, classmethod, staticmethod
  4.  Encapsulation (public / protected / private, getters-setters, @property)
  5.  Inheritance (single, multilevel, hierarchical, multiple, diamond)
  6.  super() and Method Resolution Order (MRO)
  7.  Polymorphism (duck typing, overriding, "overloading", operator overloading)
  8.  Abstraction (ABC, abstractmethod)
  9.  Composition (HAS-A) vs Inheritance (IS-A)
  10. Extras: isinstance / issubclass, __del__, __eq__, __len__, @dataclass
  11. Iterators, Generators (yield), Context Managers (with)

Run the file top to bottom - every section prints its own heading.
"""


def heading(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


# ============================================================
# 1. CLASS & OBJECT BASICS
# ============================================================
heading("1. CLASS & OBJECT BASICS")

# class  = blueprint / template
# object = actual thing created from the blueprint (an "instance")
class Dog:
    def bark(self):              # method = function inside a class
        print("Woof!")

d1 = Dog()      # creating an object (instantiation)
d2 = Dog()      # many objects can come from one class
d1.bark()
d2.bark()
print(type(d1))          # <class '__main__.Dog'>
print(d1 is d2)          # False -> two separate objects in memory


# ============================================================
# 2. CONSTRUCTOR, self, __str__ / __repr__
# ============================================================
heading("2. CONSTRUCTOR, self, __str__")

class Student:
    # __init__ is the constructor: runs automatically when an object is created.
    # 'self' = the object currently being worked on (Python passes it for you).
    def __init__(self, name, roll_no):
        self.name = name         # instance variables (different for each object)
        self.roll_no = roll_no
        print("Inside constructor for", name)

    def show(self):
        print("Student name:", self.name, "| Roll:", self.roll_no)

    # __str__  -> what print(obj) shows (human friendly)
    def __str__(self):
        return f"Student({self.name}, {self.roll_no})"

    # __repr__ -> developer friendly text (shown in the console / lists)
    def __repr__(self):
        return f"Student(name={self.name!r}, roll_no={self.roll_no!r})"

s1 = Student("Rahul", 1)
s2 = Student("Neha", 2)
s1.show()
print(s2)               # uses __str__
print([s1, s2])         # uses __repr__ for items inside a list

# Passing a CLASS itself as an argument (classes are objects in Python too)
def create_object(class_name):
    print("class address:", class_name, "| id:", id(class_name))
    obj = class_name("Amit", 3)     # same as Student("Amit", 3)
    obj.show()

create_object(Student)


# ============================================================
# 3. INSTANCE vs CLASS VARIABLES, classmethod, staticmethod
# ============================================================
heading("3. CLASS MEMBERS")

class ICICIBANK:
    # ---- Class variables: ONE copy shared by all objects ----
    bankName = "ICICI"
    ROI = 4

    def __init__(self, accNo, name, balance):
        # ---- Instance variables: separate copy for every object ----
        self.accNo = accNo
        self.name = name
        self.balance = balance

    # Instance method: works with 'self' (one particular object)
    def details(self):
        print("Account No:", self.accNo, "| Name:", self.name,
              "| Balance:", self.balance)

    # Class method: works with 'cls' (the class), can change class variables
    @classmethod
    def changeROI(cls, new_roi):
        cls.ROI = new_roi

    # Static method: no self / cls. Just a utility function kept inside the class
    @staticmethod
    def validAmount(amount):
        return amount > 0

robi = ICICIBANK(101, "Robi", 10000)
neha = ICICIBANK(102, "Neha", 20000)
robi.details()
neha.details()

print(robi.__dict__)              # instance variables live in this dictionary

# Changing a class variable through the CLASS -> affects everyone
print("ROI before:", robi.ROI, neha.ROI)
ICICIBANK.changeROI(6)
print("ROI after :", robi.ROI, neha.ROI)

# Assigning through an OBJECT creates a NEW instance variable (shadowing)
robi.bankName = "HDFC"
print(robi.bankName, "|", neha.bankName, "|", ICICIBANK.bankName)
print(robi.__dict__)              # now contains bankName too

print(ICICIBANK.validAmount(0))       # False
print(ICICIBANK.validAmount(500))     # True


# ============================================================
# 4. ENCAPSULATION  (data hiding + controlled access)
# ============================================================
heading("4. ENCAPSULATION")

class Account:
    def __init__(self, balance):
        self.owner = "Public"        # public     -> accessible anywhere
        self._branch = "Mumbai"      # protected  -> convention only: "please don't touch"
        self.__balance = balance     # private    -> name-mangled to _Account__balance

    # Getter / setter methods give controlled access to the private data
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Invalid / insufficient")

    def get_balance(self):
        return self.__balance

    # @property = the Pythonic way: access like an attribute, but runs code
    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            print("Balance cannot be negative")
        else:
            self.__balance = value

acc = Account(1000)
acc.deposit(500)
print("Balance:", acc.get_balance())

try:
    print(acc.__balance)              # AttributeError - hidden by name mangling
except AttributeError as e:
    print("Error:", e)

print(acc._Account__balance)          # still reachable (Python only "mangles" the name)

acc.balance = 2000                    # goes through the property setter
acc.balance = -5                      # rejected by the setter
print(acc.balance)                    # goes through the property getter


# ============================================================
# 5. INHERITANCE  (IS-A relationship)
# ============================================================
heading("5. INHERITANCE")

# ---- 5a. Single inheritance ----
class Person:
    def __init__(self, name):
        self.name = name

    def show(self):
        print("Name:", self.name)

class Employee(Person):                # Employee IS-A Person
    def __init__(self, name, salary):
        super().__init__(name)         # call parent constructor
        self.salary = salary

    def display(self):
        print("Name:", self.name, "| Salary:", self.salary)

emp = Employee("Robi", 50000)
emp.show()                             # inherited from Person
emp.display()

# ---- 5b. Multilevel inheritance:  Data -> Mysum -> Myavg ----
class Data:
    def __init__(self):
        print("inside data constructor")
        self.a = 0
        self.b = 0

    def getA(self):
        return self.a

    def getB(self):
        return self.b

    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def Display(self):
        print("a =", self.a)
        print("b =", self.b)

class Mysum(Data):
    def __init__(self):
        super().__init__()             # runs Data.__init__ first
        print("inside mysum constructor")
        self.c = 0

    def total(self):
        self.c = self.a + self.b

    def Display(self):                 # overriding + extending parent's Display
        super().Display()
        print("sum =", self.c)

class Myavg(Mysum):
    def __init__(self):
        super().__init__()             # runs Mysum.__init__ (which runs Data.__init__)
        print("inside myavg constructor")
        self.d = 0

    def aavg(self):
        self.d = self.c / 2

    def Display(self):
        super().Display()
        print("avg =", self.d)

obj = Myavg()                          # constructors run: Data -> Mysum -> Myavg
print(obj.getA(), obj.getB())
obj.setA(10)
obj.setB(20)
obj.total()
obj.aavg()
obj.Display()

# ---- 5c. Hierarchical inheritance: one parent, many children ----
class A:
    def m1(self):
        print("in m1")

class B(A):
    def m2(self):
        print("in m2")

class C(A):
    def m3(self):
        print("in m3")

class D(A):
    def m4(self):
        print("in m4")

obj = C()
obj.m3()
obj.m1()                               # C gets m1 from A
print(hasattr(obj, "m2"))              # False -> siblings do NOT share methods

# ---- 5d. Multiple inheritance: one child, many (unrelated) parents ----
class A1:
    def m1(self):
        print("in m1")

class B1:
    def m2(self):
        print("in m2")

class C1:
    def m3(self):
        print("in m3")

class D1(A1, C1, B1):                  # D1 gets methods of all three
    def m4(self):
        print("in m4")

obj = D1()
obj.m1()
obj.m2()
obj.m3()
obj.m4()


# ============================================================
# 6. super() AND METHOD RESOLUTION ORDER (MRO)
# ============================================================
heading("6. MRO (diamond problem)")

class A:
    def m1(self):
        print("in m1 of A")

class B(A):
    def m1(self):                      # overrides A.m1
        print("in m1 of B")

class C(A):
    def m3(self):
        print("in m3")

class D(B, C):                         # DIAMOND:  D -> B -> C -> A
    def m4(self):
        print("in m4")

obj = D()
obj.m1()          # B.m1 wins - Python searches D, then B, then C, then A
obj.m3()
obj.m4()

# obj.m2() would raise AttributeError - no class in the chain defines m2
try:
    obj.m2()
except AttributeError as e:
    print("Error:", e)

# MRO = the exact order Python searches for a method (left-to-right, parents after children)
print([cls.__name__ for cls in D.__mro__])      # ['D', 'B', 'C', 'A', 'object']

# super() follows the MRO, so with multiple inheritance it calls the NEXT class in the MRO
class X:
    def hello(self):
        print("X.hello")

class Y(X):
    def hello(self):
        print("Y.hello")
        super().hello()

class Z(X):
    def hello(self):
        print("Z.hello")
        super().hello()

class W(Y, Z):
    def hello(self):
        print("W.hello")
        super().hello()

W().hello()       # W -> Y -> Z -> X  (each class runs exactly once)


# ============================================================
# 7. POLYMORPHISM  (one interface, many forms)
# ============================================================
heading("7. POLYMORPHISM")

# ---- 7a. Duck typing: "if it has send(), I can use it" - no common parent needed ----
class Email:
    def Send(self):
        print("Email sent")

class SMS:
    def Send(self):
        print("SMS sent")

class Whatsapp:
    def Send(self):
        print("Whatsapp sent")

def Notify(classnickname):
    obj = classnickname()              # classnickname is just a name for the class passed in
    obj.Send()                         # works for ANY class that has Send()

Notify(Email)
Notify(SMS)
Notify(Whatsapp)

# ---- 7b. Method overriding (runtime polymorphism) ----
class Animal:
    def sound(self):
        print("Animal makes sound")

class Cat(Animal):
    def sound(self):                   # same name, new behaviour
        print("Cat meows")

class Cow(Animal):
    def sound(self):
        print("Cow moos")

for pet in (Animal(), Cat(), Cow()):   # same call, different result per object type
    pet.sound()

# ---- 7c. Method overloading ----
# Python does NOT support classic overloading: a later def with the same name
# REPLACES the earlier one, so only the last m1(a, b) survives.
def m1(a):
    print("in m1 with a")

def m1():
    print("in m1")

def m1(a, b):
    print("in m1 with a and b")

m1(10, 20)             # only the last definition exists
# m1(10)               # would raise TypeError

# Python's way to get "overloading": default arguments or *args
def add(a, b=0, c=0):
    return a + b + c

print(add(1), add(1, 2), add(1, 2, 3))

def add_all(*args):                    # any number of arguments
    return sum(args)

print(add_all(1, 2, 3, 4, 5))

# ---- 7d. Operator overloading (dunder / magic methods) ----
class Marks:
    def __init__(self, marks):
        self.marks = marks

    def __add__(self, other):          # obj1 + obj2
        return Marks(self.marks + other.marks)

    def __sub__(self, other):          # obj1 - obj2
        return Marks(self.marks - other.marks)

    def __eq__(self, other):           # obj1 == obj2
        return self.marks == other.marks

    def __lt__(self, other):           # obj1 < obj2
        return self.marks < other.marks

    def __str__(self):
        return f"Marks({self.marks})"

m_a = Marks(50)
m_b = Marks(70)
print(m_a + m_b)                       # Marks(120)
print(m_b - m_a)                       # Marks(20)
print(m_a == m_b, m_a < m_b)           # False True


# ============================================================
# 8. ABSTRACTION  (hide details, show only what's essential)
# ============================================================
heading("8. ABSTRACTION")

from abc import ABC, abstractmethod

# Abstract class: cannot be instantiated; it is a contract for its children.
class Bank(ABC):
    @abstractmethod
    def Roi(self):                     # child classes MUST implement this
        pass

    def welcome(self):                 # concrete method inside an abstract class is fine
        print("Welcome to the bank")

# Concrete classes: implement every abstract method
class SBI(Bank):
    def Roi(self):
        print("8 %")

    def loan(self):                    # extra method only SBI has
        print("sbi loan")

class ICICI(Bank):
    def Roi(self):
        print("10 %")

class HDFC(Bank):
    def Roi(self):
        print("12 %")

for bank in (SBI(), ICICI(), HDFC()):
    bank.Roi()                         # abstraction + polymorphism together

SBI().loan()

try:
    b = Bank()                         # not allowed
except TypeError as e:
    print("Error:", e)

# Abstract class with a shape example (abstract method with data)
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

print("Area:", Rectangle(10, 5).area())


# ============================================================
# 9. COMPOSITION (HAS-A) vs INHERITANCE (IS-A)
# ============================================================
heading("9. COMPOSITION")

# Composition: one class holds objects of other classes as its parts.
# Rule of thumb: Car IS-A Vehicle (inheritance), Car HAS-A Engine (composition).
class Battery:
    def __init__(self):
        print("Inside Battery constructor")

    def status(self):
        print("Battery is 100%")

class Mobile:
    def __init__(self):
        print("Inside Mobile constructor")
        self.battery = Battery()       # HAS-A relationship

    def work(self):
        self.battery.status()          # delegate work to the part
        print("Mobile is working")

Mobile().work()

class Science:
    def teach(self):
        print("Learning Science")

class Commerce:
    def teach(self):
        print("Learning Commerce")

class Arts:
    def teach(self):
        print("Learning Arts")

class College:                         # College HAS-A Science, Commerce, Arts
    def __init__(self):
        self.departments = [Science(), Commerce(), Arts()]

    def run(self):
        for dept in self.departments:
            dept.teach()               # polymorphism again

College().run()


# ============================================================
# 10. EXTRAS
# ============================================================
heading("10. EXTRAS")

# ---- isinstance / issubclass ----
print(isinstance(emp, Employee))       # True
print(isinstance(emp, Person))         # True  (child object IS-A parent too)
print(issubclass(Employee, Person))    # True
print(issubclass(Person, Employee))    # False

# ---- More useful dunder methods ----
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __len__(self):                 # len(obj)
        return len(self.songs)

    def __getitem__(self, i):          # obj[i] (also makes it iterable)
        return self.songs[i]

    def __call__(self):                # obj()  -> object behaves like a function
        print("Playing", len(self), "songs")

p = Playlist(["a", "b", "c"])
print(len(p), p[0])
p()

# ---- Destructor: runs when the object is deleted / garbage collected ----
class Temp:
    def __init__(self):
        print("Object created")

    def __del__(self):
        print("Object destroyed")

t = Temp()
del t                                  # triggers __del__

# ---- @dataclass: auto-generates __init__, __repr__, __eq__ ----
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int = 0                         # default value

pt = Point(3, 4)
print(pt)                              # Point(x=3, y=4)
print(pt == Point(3, 4))               # True

# ---- Object attributes helpers ----
setattr(pt, "x", 99)                   # set attribute by name
print(getattr(pt, "x"))                # get attribute by name
print(hasattr(pt, "z"))                # False

# ============================================================
# 11. ITERATORS, GENERATORS & CONTEXT MANAGERS
# ============================================================
heading("11. ITERATORS, GENERATORS & CONTEXT MANAGERS")

# ---- 11a. __eq__ and __len__ together ----
class Cart:
    def __init__(self, items):
        self.items = items

    def __eq__(self, other):           # c1 == c2 -> compare by CONTENT, not by memory address
        return self.items == other.items

    def __len__(self):                 # len(c1)
        return len(self.items)

c1 = Cart(["apple", "banana"])
c2 = Cart(["apple", "banana"])
c3 = Cart(["apple"])

print(c1 == c2)        # True  -> custom __eq__ (without it, this would be False: different objects)
print(c1 == c3)        # False
print(c1 is c2)        # False -> 'is' checks identity, '==' checks equality
print(len(c1))         # 2     -> custom __len__


# ---- 11b. ITERATORS: __iter__ and __next__ ----
# Iterable = anything you can loop over (list, str, dict, your own class).
# Iterator = the object that hands out values one at a time.
# A class becomes an iterator when it has:
#     __iter__()  -> returns the iterator (usually self)
#     __next__()  -> returns the next value, raises StopIteration when finished
class CountUpTo:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self                    # the object itself is the iterator

    def __next__(self):
        if self.current > self.limit:
            raise StopIteration        # tells the for loop "no more values"
        value = self.current
        self.current += 1
        return value

# A for loop secretly does this:
#   it = iter(obj)            -> calls obj.__iter__()
#   while True: next(it)      -> calls obj.__next__() until StopIteration
for num in CountUpTo(5):
    print(num, end=" ")
print()

# Doing the same steps manually:
it = CountUpTo(3)
print(next(it), next(it), next(it))    # 1 2 3
try:
    next(it)                           # 4th call -> StopIteration
except StopIteration:
    print("Iterator exhausted")

# NOTE: this iterator is single-use. Its state (self.current) lives in the object,
# so a second loop over the SAME object gives nothing.
used = CountUpTo(3)
print(list(used))                      # [1, 2, 3]
print(list(used))                      # []  -> already exhausted


# ---- 11c. GENERATORS: yield ----
# A function containing 'yield' is a generator function. Calling it does NOT run the body;
# it returns a generator object (an iterator). Each next() runs the code until the next
# 'yield', hands back that value, then PAUSES and remembers where it stopped.
# Same result as the CountUpTo class, in 5 lines instead of 12.
def count_up_to_generator(limit):
    current = 1
    while current <= limit:
        yield current                  # pause here, resume on the next next()
        current += 1

gen = count_up_to_generator(3)
print(gen)                             # <generator object ...>
print(next(gen), next(gen), next(gen)) # 1 2 3

for num in count_up_to_generator(5):
    print(num, end=" ")
print()

def fibonacci_generator(count):
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b

for num in fibonacci_generator(10):
    print(num, end=" ")
print()

# Why generators? They are LAZY: values are produced one at a time, so they use
# almost no memory even for huge sequences (a list would build everything up front).
def big_numbers():
    for i in range(10_000_000):
        yield i

total = 0
for n in big_numbers():
    total += n
    if n == 5:
        break                          # we only computed 6 values, not 10 million
print("Partial total:", total)

# Generator expression: like a list comprehension but with () -> lazy
squares = (x * x for x in range(5))
print(list(squares))                   # [0, 1, 4, 9, 16]

# Generators can also be methods, making a class iterable without __next__
class Team:
    def __init__(self, members):
        self.members = members

    def __iter__(self):                # generator method -> new fresh iterator each loop
        for m in self.members:
            yield m

team = Team(["Robi", "Neha", "Divya"])
print(list(team))
print(list(team))                      # works again, unlike CountUpTo above


# ---- 11d. CONTEXT MANAGERS: __enter__ and __exit__ (the 'with' statement) ----
# 'with' guarantees setup and cleanup, even if an error happens inside the block.
#     __enter__()  -> runs at the start of 'with'; its return value goes after 'as'
#     __exit__()   -> ALWAYS runs at the end (normal finish OR exception)
class FileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print("Opening file...")
        self.file = open(self.filename, self.mode)
        return self.file               # this becomes 'f' in "with ... as f"

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing file...")
        self.file.close()
        # exc_type / exc_value / traceback describe an exception raised inside the
        # block (all None if there was none).
        # Return True  -> suppress the exception
        # Return False/None -> let it propagate (default)

# Create the file first so the example never fails with FileNotFoundError
with FileOpener("sample.txt", "w") as f:
    f.write("Hello from a custom context manager\n")

with FileOpener("sample.txt", "r") as f:
    print(f.read())

# Cleanup still happens when an error occurs inside the block
try:
    with FileOpener("sample.txt", "r") as f:
        print(1 / 0)                   # error -> __exit__ still runs and closes the file
except ZeroDivisionError:
    print("Error caught, file was still closed:", f.closed)

# A context manager that SUPPRESSES errors by returning True from __exit__
class IgnoreErrors:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print("Suppressed:", exc_type.__name__, "-", exc_value)
        return True                    # True = swallow the exception

with IgnoreErrors():
    print(1 / 0)
print("Program continues after the with block")

# Shortcut: build a context manager from a generator using contextlib
from contextlib import contextmanager

@contextmanager
def opened(filename, mode):
    print("Opening file...")
    file = open(filename, mode)
    try:
        yield file                     # code before yield = __enter__, after = __exit__
    finally:
        print("Closing file...")
        file.close()                   # 'finally' guarantees cleanup

with opened("sample.txt", "r") as f:
    print(f.read())

import os
os.remove("sample.txt")                # tidy up the demo file

print("\nDone - all OOP topics covered.")