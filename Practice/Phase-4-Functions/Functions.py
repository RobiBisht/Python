# User-defined functions with function calling (Procedural style)

def india():
    print("Hello India")


def vinay():
    india()
    print("Hello Universe")


def robi():
    vinay()
    print("Hello World")

print("Start")   # Program starts here

robi()




# Simple Calculation Using Function

def calc():
    a=10
    b=20
    add=a+b
    sub=a-b 
    mul=a*b 
    div=b/a 
    return add,sub,mul,div

ss=calc()
print(ss)




# Functions With Five Senarios

#No Arguments & No Return Value

def add1():
    a=10
    b=20
    c=a+b
    print(c)

add1()    



#Arguments & No Return Value

def add2(a,b):
    c=a+b
    print(c)

add2(10,20)    



#No Arguments & Return Value

def add3():
    a=10
    b=20
    c=a+b
    return c

z=add3()    
print(z)


#Arguments & Return Value

def add4(a,b):
    c=a+b
    return c
x=10
y=20
print(add4(x,y))



#*args & *kwargs
#*args - Allow You To Pass Multiple Number Of Arguments

def add_all(*args):
    print("args received as tuple :", args)
    total = 0
    for num in args:
        total += num
    return total

print(add_all(1, 2, 3))
print(add_all(10, 20, 30, 40))



#**kwargs - Allow You To Pass Multiple Keyword Arguments

def show_details(**kwargs):
    print("kwargs received as dict :", kwargs)
    for key, value in kwargs.items():
        print(key, ":", value)

show_details(name="Robi", age=21, course="BCA")



#Combining Normal Args, *args and **kwargs Together

def full_demo(a, b, *args, **kwargs):
    print("a =", a)
    print("b =", b)
    print("extra positional :", args)
    print("extra keyword :", kwargs)

full_demo(1, 2, 3, 4, 5, city="Solapur", pin=413001)



#Lambda Function - Basic

square = lambda x: x * x
print(square(5))

add = lambda a, b: a + b
print(add(10, 20))



#Lambda With map() - applies function to every item in a list

numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))
print("Squares :", squares)



#Lambda With filter() - keeps items where function returns True

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Evens :", evens)



#Lambda With reduce() - reduces list to single value

from functools import reduce

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, numbers)
print("Total using reduce :", total)



# Alias Method
def Hello():

    print("Hello World")

z=Hello  #alias (Copy Of Functions Address)

print(z)

z()



# Calling Function Inside Function
def outer():

    print("outer")

    def inner():

        print("inner")

    inner()

outer()



#global keyword - modify a global variable inside a function

counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print("Counter :", counter)



#nonlocal keyword - modify enclosing function's variable from nested function

def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        print("Inside inner, count =", count)

    inner()
    inner()
    print("Inside outer, count =", count)

outer()



# Returning Function From Function

def outer():

    print("outer")

    print("Inner Start")

    def inner():

        print("inner")

    print("Inner End")

    return inner

z=outer()

z()




# Passing Function As An Argument To Another Function

def outer(a):
    
    a()

    print("outer")
    
def inner():

    print("inner")
    
outer(inner)




#  Decorators
#1st Example Of Decorator

def simple_decorator(func):

    def wrapper(name):

        print("bye")

    func("a")   

    return wrapper

@simple_decorator

def say_hello(name):

    print("Function being excuted")

say_hello('Rohit')

#2nd Example Of Decorator

def abc(f):
    def inner():
        print("###")
        f(10,20)
        print("@@@")
    return inner

@abc
def sum(a,b):
    print(a+b)
    
sum()



#File Handling - Writing To A File

with open("sample.txt", "w") as f:
    f.write("Hello ICRI\n")
    f.write("Learning File Handling\n")



#File Handling - Reading From A File

with open("sample.txt", "r") as f:
    content = f.read()
    print(content)



#File Handling - Reading Line By Line

with open("sample.txt", "r") as f:
    for line in f:
        print("Line :", line.strip())



#File Handling - Appending To A File

with open("sample.txt", "a") as f:
    f.write("Appended Line\n")



#File Handling - Working With JSON Files

import json

data = {"name": "Robi", "age": 21, "course": "BCA"}

# write dict to json file
with open("data.json", "w") as f:
    json.dump(data, f)

# read json file back into dict
with open("data.json", "r") as f:
    loaded_data = json.load(f)
    print(loaded_data)
    print(loaded_data["name"])


