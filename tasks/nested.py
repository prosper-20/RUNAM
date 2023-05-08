# def outer_function(text):
#     def inner_function():
#         return f"You typed {text}"
#     return inner_function()


# print(outer_function("Prosper"))


# def outer_function(text):
#     def inner_function():
#         return f"You typed {text}"
#     inner_function()


# print(outer_function("Prosper"))



# class Employee:

#     raise_amount = 1.04

#     def __init__(self, first, last, pay):
#         self.first = first
#         self.last = last
#         self.pay = pay
#         self.email = f"{self.first}.{self.last}@gmail.com"

#     def profile(self):
#         return f"Hi {self.first}, your email is {self.email}"
    

#     def apply_raise(self):
#         self.pay = int(self.pay * self.raise_amount)

#     @classmethod
#     def set_raise_amount(cls, amount):
#         cls.raise_amount = amount

#     @classmethod
#     def from_string(cls, text):
#         first, last, pay = text.split("-")
#         return cls(first, last, pay)


# emp_1 = Employee("prosper", "edward", 90000)

# print(emp_1.profile())
# print(emp_1.pay)
# emp_1.apply_raise()
# print(emp_1.pay)
# Employee.set_raise_amount(1.5)
# emp_1.apply_raise()
# print(emp_1.pay)

# my_string = "prosper-edward-500000"

# emp_3 = Employee.from_string(my_string)
# print(emp_3.email)




money = 	u'\u20a6'

print(money)


        

