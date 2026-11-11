#Lists

# Basic List Operations

# Creating a list

numbers = [10, 20, 30, 40]

print(numbers)
print(type(numbers))

# Accessing elements

print(numbers[0])      # First element
print(numbers[-1])     # Last element

# Modifying elements

numbers[1] = 25
print(numbers)



# List Methods (Intermediate)

fruits = ["apple", "banana", "mango"]

fruits.append("orange")     # Add at end
fruits.insert(1, "grapes")  # Add at index
fruits.remove("banana")     # Remove by value
fruits.pop()                # Remove last item

print(fruits)

# Other useful methods

fruits.sort()
fruits.reverse()
print(len(fruits))




# Advanced List Concepts

#List Comprehension

# Squares of numbers

squares = [x*x for x in range(1, 6)]
print(squares)

#Nested List

matrix = [
    [1, 2, 3],
    [4, 5, 6]
]

print(matrix[1][2])  # Output: 6

# Slicing

nums = [1, 2, 3, 4, 5]
print(nums[1:4])
print(nums[::-1])

# extend()

a = [1, 2]
b = [3, 4]
a.extend(b)
print(a)

# copy vs assignment

x = [1, 2, 3]
y = x          # Same reference
z = x.copy()   # New copy

x.append(4)
print(y)  # Changed
print(z)  # Not changed

# del keyword

del nums[2]
print(nums)

# all(), any(), sum(), min(), max().

print(all([1, 2, 3]))
print(any([0, 0, 1]))

# enumerate()

for index, value in enumerate(nums):
    print(index, value)



#Mutable Default Argument Pitfall (Common Bug)

# WRONG WAY - default list is shared across calls

def add_item_wrong(item, mylist=[]):
    mylist.append(item)
    return mylist

print(add_item_wrong("apple"))     # ['apple']
print(add_item_wrong("banana"))    # ['apple', 'banana']  <-- unexpected!


# CORRECT WAY - use None as default, create new list inside

def add_item_correct(item, mylist=None):
    if mylist is None:
        mylist = []
    mylist.append(item)
    return mylist

print(add_item_correct("apple"))   # ['apple']
print(add_item_correct("banana"))  # ['banana']   <-- correct



# Tuples

#Basic Tuple

t = (10, 20, 30)

print(t)
print(type(t))

# Accessing tuple elements

print(t[0])
print(t[-1])

# Tuple Features

# Tuple unpacking

a, b, c = t
print(a, b, c)

# Tuple with single element

single = (10,)
print(type(single))

# Advanced Tuple Usage

# Tuple inside list

data = [(1, "A"), (2, "B"), (3, "C")]

for item in data:
    print(item)

# Slicing

t = (10, 20, 30, 40)
print(t[1:3])

# count() and index()

print(t.count(20))
print(t.index(30))

# Tuple concatenation & repetition

t1 = (1, 2)
t2 = (3, 4)
print(t1 + t2)
print(t1 * 3)

# Immutable nature (important)

t = (1, 2, 3)
# t[0] = 100   ❌ Error



# Sets

#Basic Set

s = {10, 20, 30, 10}

print(s)   # Duplicate removed
print(type(s))

# Set Methods

s.add(40)
s.remove(20)
s.discard(100)   # No error if element not present

print(s)

# Set Operations (Advanced)

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a.union(b))        # All elements
print(a.intersection(b)) # Common elements
print(a.difference(b))   # a - b


# pop() & clear()

s = {1, 2, 3}
s.pop()
s.clear()

# issubset(), issuperset()

a = {1, 2}
b = {1, 2, 3}
print(a.issubset(b))
print(b.issuperset(a))

# symmetric_difference()

print(a.symmetric_difference(b))

# Frozen set (Immutable set)

fs = frozenset([1, 2, 3])

# Set comprehension

squares = {x*x for x in range(5)}
print(squares)



# Dictionaries


#Basic Dictionary

student = {
    "name": "Robi",
    "age": 19,
    "course": "BCA"
}

print(student)
print(type(student))

# Access & Modify Dictionary

print(student["name"])
print(student.get("age"))

student["age"] = 20
student["city"] = "Solapur"

print(student)

# Dictionary Methods (Intermediate)

print(student.keys())
print(student.values())
print(student.items())

# Looping dictionary

for key, value in student.items():
    print(key, ":", value)

# Advanced Dictionary Concepts

#Dictionary Comprehension

# Square values

squares = {x: x*x for x in range(1, 6)}
print(squares)

#Nested Dictionary

students = {
    1: {"name": "Aman", "age": 18},
    2: {"name": "Ravi", "age": 19}
}

print(students[2]["name"])

# pop() & popitem()


student.pop("age")
student.popitem()

# update()

student.update({"course": "BSc", "year": 2})

# setdefault()

student.setdefault("city", "Solapur")

# fromkeys()

keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)

# Copy vs reference

a = {"x": 1}
b = a
c = a.copy()
a["y"] = 2

# Dictionary sorting

d = {3: "c", 1: "a", 2: "b"}
print(dict(sorted(d.items())))



#Shallow Copy vs Deep Copy

import copy

original = [1, 2, [3, 4]]

shallow = copy.copy(original)      # same as .copy(), nested list still shared
deep = copy.deepcopy(original)     # fully independent copy, nested included

original[2].append(100)

print("Original :", original)
print("Shallow  :", shallow)       # nested list changed too (shared reference)
print("Deep     :", deep)          # unaffected (fully independent)



#Deep Copy With Dictionaries (Nested)

student = {
    "name": "Amit",
    "marks": {"math": 80, "science": 75}
}

shallow_dict = student.copy()
deep_dict = copy.deepcopy(student)

student["marks"]["math"] = 100

print("Shallow Dict :", shallow_dict)   # marks changed too
print("Deep Dict    :", deep_dict)      # unaffected



#List Attributes & Methods

mylist=[10,20,30,40,50]  

print(mylist[0],mylist[-1])

print(type(mylist))

print(dir(mylist))

mylist.append(80)

print(mylist) 



#Tuple Attributes

mytuple=(10,20,30,40,50)  
print(mytuple)
print(type(mytuple))
print(dir(mytuple))



#Set Attributes

myset={10,20,30,40,50}  
print(myset)
print(type(myset))
print(dir(myset))



#Dictionary Attributes

mydict={"name":"icri","location":"bangalore"}  
print(mydict)
print(type(mydict))
print(dir(mydict))



#String Methods In Depth

text = "  Hello ICRI Students  "

print(text.strip())                    # remove leading/trailing spaces
print(text.lower())
print(text.upper())
print(text.replace("ICRI", "Python"))
print(text.strip().split(" "))         # split into list of words
print("-".join(["a", "b", "c"]))       # join list into string
print(text.strip().startswith("Hello"))
print(text.strip().endswith("Students"))
print(text.count("t"))
print(text.find("ICRI"))               # index position, -1 if not found
print("abc123".isalnum())
print("abc".isalpha())
print("123".isdigit())

name = "Robi"
age = 21
print("Name is {} and age is {}".format(name, age))    # .format() style
print("Name is %s and age is %d" % (name, age))        # % style (older)
