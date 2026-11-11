# Print Statement

a=10
b=20

print(f"value of a={a} and value of b={b}")
print(f'value of {a} and value of {b}')



# Area Of Triangle

r=5

area=3.14*r**2

print(f"Area Of Triangle = {area}")



#Swap Using Third Variable

a=10
b=20

print(f"Print Before Swap a={a} and b={b}")
 
c=a
a=b
b=c

print(f"Print After Swap a={a} and b={b}")



#Swaping Without Using Third Variable (Most Used)

x = 10
y = 5

x, y = y, x

print(f"x = {x}")
print(f"y = {y}")
    


#Swaping Using Arithmetic Operators(This works for integers and other numeric values in many cases, but it has limitations)

x = 10
y = 5

x = x + y
y = x - y
x = x - y

print(f"x = {x}")
print(f"y = {y}")



#Attributes Of Different Data Types

# Integer Attributes

a = 30  

print(type(a))
    
print(dir(a))


#String Attributes & Methods

name="icri welcome"  

print(type(name))
print(dir(name))
print(name.capitalize())



#Float Attributes

pi=3.14  

print(pi)
print(type(pi))
print(dir(pi))



#Complex Number Attributes

z=2+4j 
print(z)
print(type(z))
print(dir(z))



#Boolean Attributes

status=True
print(type(status))
print(dir(status))



#Simple [ If-Else ] Statement

age=int(input("Enter Your Age :"))

if age >= 18 :
    print("You Can Vote.")

else :
    print("You Cannot Vote.")    



#[ If ] Statement With [ Or ] Logical Operator


marks = 60

status = 'enable'

dept = 'mm'

bonus = 10

if status=='disable' or dept=='cs':
    bonus = 10

total_marks = marks+bonus

print(f'total_marks = {total_marks}')



#[ Elif ] Ladder


day=int(input("Enter Day : "))

if day==1:
    print("Today Is Monday")

elif day==2:    
    print("Today Is Tuesday")

elif day==3:    
    print("Today Is Wednesday")

elif day==4:    
    print("Today Is Thursday")

elif day==5:    
    print("Today Is Friday")

elif day==6:
    print("Today Is Saturday")

elif day==7:    
    print("Today Is Sunday")

else :
    print("Invalid Day")



#[ If-Elif-Else ] Statement


salary = int(input("Enter Salary :"))

if salary >= 10000 and salary <= 20000 :
    bonus=salary*10/100

elif salary >= 20000 and salary <= 30000 :
    bonus=salary*20/100

elif salary >=30000 and salary<=40000:
    bonus=salary*30/100

else:
    bonus=0

total_salary= salary + bonus

print(f'"Total Salary Of Employee: {total_salary}')    
                 
 
 
#Match-Case


day=int(input("Enter Day : "))

match day:

    case 1:
        print("Monday")

    case 2:
        print("Tuesday")

    case 3:
        print("Wednesday")

    case 4:
        print("Thursday")

    case 5:
        print("Friday")

    case 6:
        print("Saturday")

    case 7:
        print("Sunday")

    case _:
        print("Invalid Data, Please try again")



#Nesting


a=int(input("Enter Number : "))

b=int(input("Enter Number : "))

c=int(input("Enter Number : "))

if a>b:
    if a>c:
        print(a," Is Largest")
        
    else:
        print(c," Is Largest")
        
else:
    if b>c:
        print(b, " Is Largest")
        
    else:
        print(c, " Is Largest")
        
print("DONE")



#Exception Handling - try/except/else/finally

try:
    a = int(input("Enter a number : "))
    b = int(input("Enter another number : "))
    result = a / b

except ZeroDivisionError:
    print("Error : Cannot divide by zero")

except ValueError:
    print("Error : Please enter valid numbers")

else:
    print(f"Result = {result}")   # runs only if no exception occurred

finally:
    print("This always runs, error or not")



#Exception Handling - raise (manually throwing an error)

def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    print(f"Age set to {age}")

try:
    set_age(-5)
except ValueError as e:
    print("Caught Error :", e)



#Custom Exception (User-defined Exception Class)

class InsufficientBalanceError(Exception):
    def __init__(self, message="Balance is too low for this withdrawal"):
        super().__init__(message)

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError()
    return balance - amount

try:
    withdraw(1000, 5000)
except InsufficientBalanceError as e:
    print("Custom Exception Caught :", e)

