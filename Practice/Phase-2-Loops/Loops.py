#Simple While Loop

i=1

while i<=5:
    
    print("Hello World")
    
    i=i+1
    
print("done")   



#Simple For Loop

for i in range(1,11):
    print(i)



#Factorial Of Number Using While Loop

i=1

fact=1

n=5

while i<=5:
    fact = fact * i
    i=i+1
    print("Factorial of",n,"=",fact)



#Factorial Of Number Using For Loop

n = 5

fact = 1

for i in range(1, n + 1):
    fact *= i

print("Factorial of", n, "=", fact)



#Recursion - Concept + Simplest Example (Countdown)

def countdown(n):

    if n == 0:                 # base case (stops the recursion)
        print("Done")
        return

    print(n)

    countdown(n - 1)           # recursive case (function calls itself)

countdown(5)



#Recursion - Sum Of First N Numbers

def sum_recursive(n):

    if n == 0:                 # base case
        return 0

    return n + sum_recursive(n - 1)    # recursive case

print("Sum :", sum_recursive(5))



#Factorial Of Number Using Recursion

def factorial_recursive(n):

    if n == 0 or n == 1:       # base case
        return 1

    return n * factorial_recursive(n - 1)      # recursive case

print("Factorial :", factorial_recursive(5))



#fibonacci Series Using while Loop

a = 0
b = 1
count = 10

i = 0
while i < count:
    print(a)
    a, b = b, a + b
    i += 1



#fibonacci Series Using for Loop

a = 0
b = 1
count = 10

for i in range(count):
    next = a + b
    print(a)
    a = b
    b = next
    
print("hi") 



#Fibonacci Series Using Recursion

def fibonacci_recursive(n):

    if n <= 1:                 # base case
        return n

    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

for i in range(10):
    print(fibonacci_recursive(i), end=" ")
print()



#Sum Of Digits Of Number Using While Loop

n=int(input("Enter Any Number :"))

sum=0

while n>0:
    
    rem=n%10
    
    sum = sum + rem
    
    n=n//10
    
print(f'Sum Of Digits : {sum}')   



#Sum Of Digits Of Number Using For Loop


n=int(input("Enter Any Number :"))

sum=0

digits = len(str(n))

for _ in range(digits):
    rem = n % 10
    sum += rem
    n //= 10

print(f'Sum Of Digits : {sum}')







#Armstrong Number Using While Loop

n=int(input("Enter Any Number :"))

a=n

sum=0

while n>0:
    
    rem=n%10
    
    sum = sum + (rem*rem*rem)
    
    n=n//10
if sum==a:
        
        print(f'Number Is Armstrong ') 
        
else:
        
        print(f'Number Is Not Armstrong')   




#Armstrong Number Using For Loop

n = int(input("Enter Any Number: "))

a = n
sum = 0
digits = len(str(n))  

for _ in range(digits):
    rem = n % 10
    sum += rem ** digits
    n //= 10

if sum == a:
    print("Number Is Armstrong")
else:
    print("Number Is Not Armstrong")



#Pattern Using While Loop

i = 1

while i <= 5:
    
    j = 1
    
    while j <= i:
        
        print("*", end=" ")
        
        j = j + 1
    
    print()
    
    i = i + 1




#Reverse Pattern Using While Loop

i = 5

while i >= 1:
    
    j = 1
    
    while j <= i:
        
        print("*", end=" ")
        
        j = j + 1
    
    print()
    
    i = i - 1




#Pattern Using For Loop

for i in range(1,5):

    print(" * " * i)



#Reverse Pattern Using For Loop

for i in range(4,0,-1):

    print(" * " * i)



#Number Pattern Using While Loop

i = 1 

count = 1

while i <= 5 :
    
    j = 1

    while j <= i :

        print(count,end=" ")

        count = count + 1

        j = j + 1

    print()

    i = i + 1 



#Reverse Number Pattern Using While Loop

n = int(input("Enter Any Number : "))

print(f'Reverse Of A Number : {n}')

while n > 0 : 
    
    rem = n % 10
    
    print ( rem , end = '' )
    
    n = n // 10




#Number Pattern Using For Loop

count = 1
for i in range(1,6):
    
    for j in range(1,i+1):
        
        print(count,end=" ")
        
        count = count + 1
        
    print()



#Reverse Number Pattern Using For Loop

n = int(input("Enter Any Number : "))
print(f'Reverse Of A Number : {n}')
for i in range(n, 0, -1):
    rem = i % 10
    print(rem, end='')



#Prime Number Check Using While Loop


num = int(input("Enter a number: "))

if num < 2:
    print("Not a Prime Number")
else:
    is_prime = True
    i = 2

    while i < num:
        if num % i == 0:
            is_prime = False
            break

        i += 1

    if is_prime:
        print("Prime Number")
    else:
        print("Not a Prime Number")



#Prime Number Check Using While Loop.


num = int(input("Enter a number: "))

if num < 2:
    print("Not a Prime Number")
else:
    is_prime = True

    for i in range(2, num):
        if num % i == 0:
            is_prime = False
            break

    if is_prime:
        print("Prime Number")
    else:
        print("Not a Prime Number")



#Break Statement With While Loop

i=1

while i<=5:

    if i==3:

        break

    print(i)

    i=i+1

print("Done")



#Continue Statement With While Loop

i=1
while i<=5:

    if i==3:

        i=i+1

        continue

    print(i)

    i=i+1
print("Done")



#Break Statement With For Loop

for i in range(1,6):
    if i==3:

        break

    print(i)
print("Done")



#Continue Statement With For Loop

for i in range(1,6):

    if i==3:

        continue

    print(i)
print("Done")


#Logical Operators
a = 10
b = 20
c = 30



#Ternary Operator


a=100

b=20

c=a if a>b else b

print(c)



#Sum Of First 5 Natural Number Using While Loop

i=1

sum=0

while i<=5:

    sum = sum + i

    i=i+1

print("Total Sum Of :",sum)    



#Sum Of First 5 Natural Number Using For Loop

sum = 0

for i in range(1, 6):

    sum += i

print("Total Sum Of :", sum)



#Detect Even Or Odd Number Using While Loop

flag=0
n=9
i=2

while i<=n-1:
    if n%i==0:
        flag=1
        break
    i=i+1
    
if flag==0:
    print(f'Number Is Prime')

else:
    print(f'Number Is Not Prime')




#Detect Even Or Odd Number Using For Loop

flag=0
n=9
i=2

for i in range(2,n-1,1):
    if n%i==0:
        flag=1
        break
    i=i+1
    
if flag==0:
    print(f'Number Is Prime')

else:
    print(f'Number Is Not Prime')
