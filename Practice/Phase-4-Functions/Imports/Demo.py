# a simple variable
p = 100


class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def sub(self):
        return self.a - self.b

    def mul(self):
        return self.a * self.b

    def div(self):
        return self.a / self.b


# function used in import
def calc():
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    c = Calculator(a, b)

    print("Addition:", c.add())
    print("Subtraction:", c.sub())
    print("Multiplication:", c.mul())
    print("Division:", c.div())

    return "Calculation Done"