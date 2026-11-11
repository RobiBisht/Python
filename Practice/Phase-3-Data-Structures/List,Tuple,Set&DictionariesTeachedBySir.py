mylist=[10,20,30,40,50]

print(mylist[0],mylist[-1])

print(type(mylist))

print(dir(mylist))

mylist.append(80)

print(mylist)



l1=[]
print(len(l1))
n=int(input("enter total list element="))

for i in range(n):
    z=int(input("enter actual values="))
    l1.append(z)
print(l1)

even=[]

odd=[]

for i in range(n):
    if l1[i]%2 ==0:
        even.append(l1[i])
    else:
        odd.append(l1[i])
print(even)
print(odd)
print(sum(even))
print(sum(odd))


#Dictionaries

mobile={
        "Ajay":123456768,
    
        "Ajay":123456769,
    
        "Shivam":9876543
    
    }

print(len(mobile))

print(mobile["Ajay"])

print(mobile["Shivam"])

print(mobile.get("Ajay"))

print(dir(mobile))


print(type(mobile))

print(dir(mobile))

print(mobile.keys())

for key in mobile.keys():
    
    print(key)

for value in mobile.values():
    
    print(value)

print(len(mobile))

print(mobile.items())

for k,v in mobile.items():
    
    print(k,":",v)

  
company = {
    
    "name": "ABC Ltd",
    "employees": 
        
    [
     
        {"id": 1, "name": "Ravi", "role": "Dev"},
        {"id": 2, "name": "Ajay", "role": "Tester"}
    
    ]
    
}

print(company["employees"])

print(company["employees"][0])

print(company["employees"][0]["role"])

for i in company:
    
    print(i)
    
    if i is "employees":
        
        #print("yes")
        
        print(company[i][0]["name"])
   
    

student = {
    
    "name": "Amit",
    "subjects": 
        
    [
       
        {"name": "Math", "marks": 80},
        {"name": "Science", "marks": 75},
        {"name": "English", "marks": 70}
   
    ]
    
}

print(student["subjects"][1]["marks"])


student = {
    
    "name": "Amit",
    
    "subjects": 
        
    [
        
        {"name": "Math", "marks": 80},
        {"name": "Science", "marks": 75},
        {"name": "English", "marks": 70}
    
    ]
    
}


'''
student
 ├── name
 └── subjects (list)
      ├── 0 → {name, marks}
      ├── 1 → {name, marks}
      └── 2 → {name, marks}
'''


#2
student = {
   
    "name": "Amit",
    "subjects": 
   
    [
    
        {"name": "Math", "marks": 80},
        {"name": "Science", "marks": 75},
        {"name": "English", "marks": 70}
    
    ]
}


print(student["name"])

print(student["subjects"][0]["name"])

print(student["subjects"][1]["marks"])

for subject in student["subjects"]:

    print(subject["name"], "=", subject["marks"])

student["subjects"].append(

    {"name": "Computer", "marks": 90}
)

student["subjects"][0]["marks"] = 85

subjects = student.get("subjects", [])

print(subjects)

for sub in subjects:

    print(sub.get("name"), sub.get("marks"))

'''
student
 ├── name
 └── subjects (list)
      ├── 0 → {name, marks}
      ├── 1 → {name, marks}
      └── 2 → {name, marks}
'''


student = {

    "name": "Amit",
    "marks": {

        "math": 80,
        "science": 75

    }

}

student["address"] = {

    "city": "Delhi",
    "pin": 110001

}


print(student)

marks = student.get("marks", {})

print(marks.get("english"))

student["marks"]["english"] = 70

print(marks.get("english"))

#add

print(student)

orders = {

    "ORD1001": {

        "customer": {

            "id": 1,
            "name": "Ravi"

        },

        "items": [

            {"product": "Laptop", "price": 50000, "qty": 1},
            {"product": "Mouse", "price": 500, "qty": 2}

        ],

        "status": "PLACED"
    },

    "ORD1002": {

        "customer": {

            "id": 2,
            "name": "ajay"

        },

        "items": [

            {"product": "Phone", "price": 30000, "qty": 1}

        ],

        "status": "SHIPPED"

    }

}

print(orders["ORD1001"]["items"][1]["qty"])



#Customer name of an order

print(orders["ORD1001"]["customer"]["name"])

#First product name

print(orders["ORD1001"]["items"][0]["product"])

for item in orders["ORD1001"]["items"]:

    print(item["product"], item["qty"])

def calculate_total(order):

    total = 0

    for item in order["items"]:

        total += item["price"] * item["qty"]

    return total

total = calculate_total(orders["ORD1001"])

print("Total:", total)

#add

def add_item(order, product, price, qty):

    order["items"].append({
        
        "product": product,
        "price": price,
        "qty": qty

    })


add_item(orders["ORD1001"], "Keyboard", 1500, 1)

total = calculate_total(orders["ORD1001"])

print("Total:", total)

#Update order status (state change)

def update_status(orders, order_id, status):

    if order_id in orders:

        orders[order_id]["status"] = status

update_status(orders, "ORD1001", "DELIVERED")

#search
#Search across orders (professional pattern)
#Find all shipped orders


shipped_orders = []

for order_id, order in orders.items():

    if order["status"] == "SHIPPED":

        shipped_orders.append(order_id)

print(shipped_orders)

#Safe access (production habit)

order = orders.get("ORD9999")

if not order:

    print("Order not found") 