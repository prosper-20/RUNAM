# import time
import random
import math


# def profile(name, phone_number):
#     return f"Hi {name}, your number is {phone_number}"
#     # return "Hi"+ name + "your number is " + phone_number

# print(profile("prosper", "1234567898"))



# rate = int(input("Enter your rate per hour: "))
# hours = int(input("How many hours did you work today: "))

# def salary(rate, hours):
#     salary = rate * hours
#     return salary


# print(salary(rate, hours))


# def greet(*name):
#     return f"Welcome {name}"


# print(greet("prosper", "edward"))

# def get_salary(salary="200,000"):
#     return f"Your salary is {salary}"

# print(get_salary())

# print(get_salary("600,000"))


# PSEUDO CODE

a = [2, 4, 6]
c = []

# def squares(a):
#     for number in a:
#         new = pow(number, 2)
#         c.append(new)
#     return c

# print(squares(a))

# cubed_list = []
# def cube(a):
#     for number in a:
#         cubed_number = number ** 3
#         cubed_list.append(cubed_number)
#     return cubed_list


# print(cube(a))












# 1. For loop
# 2. Square the number
# 3. add to a new list









# def citizen(country="Nigeria"):
#     return f"You are from {country}"


# print(citizen())

# print(citizen("South Africa"))






# def adder(number1, number2):
#     return number1 + number2

# print(adder(5, 6))


# def greet(name, last_name):
#     return "Welcome " + name


# print(greet("prosper", "value"))

# def code():
#     return "I am using python"

# print(code())


# def greet():
#     return "This is 4 AM"

# print(greet())




# def greet():
#     print("Coding is fun!")


# greet()

# my_list = [5, 6, 7, 8, 9]
# random.shuffle(my_list)
# print(my_list)

# print(random.choice(my_list))

# print(random.sample(my_list, 3))

# print(random.randrange(2,5))

# print(random.uniform(2, 4))

# name = input("Enter your name: ")
# time.sleep(3)
# print("Welcome " + name)



# number = input("Pls enter a number: ")
# print(number)


# scores = [60, 70, 80, 90]

# print(sum(scores))

# a =[2, 4, 6, 8]

# output = enumerate(a)

# print(list(output))

# for number in range(-1,101):
#     print(number)

# c = zip(a, b)
# print(c)
# d = list(c)
# print(d)


# import random


# my_list = [2, 4, 5, 6]
# random.shuffle(my_list)
# print(my_list)


# print(random.choice(my_list))

# print(random.sample(my_list, 3))

# print(random.randrange(3, 9))

# print(random.uniform(4, 5))





class Employee:

    company_name = "Univelcity"
    raise_percentage = 1.8

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + 'gmail.com'

    def apply_raise(self):
        self.pay = int(self.pay *  Employee.raise_percentage)
        return self.pay
    

    @classmethod
    def set_raise_percentage(cls, percentage):
        cls.raise_percentage = percentage

    @classmethod
    def from_string(cls, given_string):
        first,last,pay = given_string.split("-")
        return Employee(first, last, pay)

    
    def profile(self):
        return f"Your fullname is {self.first} - {self.last}, you work for {self.company_name}"



emp_1 = Employee("prosper", "edward", 50000)
emp_2 = Employee("Dami", "Paul", 7000)
# emp_1.company_name = "Unilag"


# emp_3 = Employee.from_string("deborah-iluonaze-100000")
# print(emp_3.profile())


class Developer(Employee):
    def __init__(self, first, last, pay, programing_language):
        super().__init__(first, last, pay)
        self.programming_language = programing_language

    def profile(self):
        return "I am a boy"
        # return super().profile()


# print(help(Developer))
dev_1 = Developer("prosper", "edward", 500000, "Python")

print(dev_1.profile())
print(dev_1.pay)


class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        self.employees = employees

        if self.employees is None:
            self.employees = []
        else:
            self.employees = None

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emp(self):
        for emp in self.employees:
            print(emp)




my_manager = Manager("martins", "odio", 60000)
my_manager.add_emp(emp_1)
print(my_manager.print_emp())


# print(emp_1.pay)
# Employee.set_raise_percentage(2)
# emp_1.apply_raise()
# print(emp_1.pay)

# print(emp_2.pay)
# Employee.set_raise_percentage(2)
# print(emp_2.raise_percentage)
# print(emp_2.pay)

# # print(emp_1.__dict__)
# # print(emp_1.profile())




# # def counter(name):
# #     small = 0
# #     capital_letter = 0

# #     for letter in name:
# #         if letter.islower():
# #             small += 1
# #         else:
# #             capital_letter += 1

# #     return(small, capital_letter)


# # print(counter("Charles"))

# # num1 = int(input())
# # num2 = int(input())
# # def checker(num1, num2):
# #     new = []
# #     for num in range(num1, num2):
# #         if num % 2 == 0:
# #             new.append(num)
# #     while len(new) < 10:
# #         new.append("null")
# #     return new

# # print(checker(num1, num2))


# # my_list = [2, 4, 8, 9, 15]
# # number = input("Enter a number:")


# # def two_sum(my_list):
# #     for num in range(len(my_list)):    
# #         for num2 in  range(num+1, len(my_list)): 
# #             if my_list[num] + my_list[num2]== number:
# #                 return (my_list[num], my_list[num2])
            

# # print(two_sum([2, 4, 8, 9, 15]))
# # number = input("Enter a number:")

# # def checker(my_list):
# #     for i in range(len(my_list)):  
# #         for j in range(i+1, len(my_list)):  
# #             if my_list[i] + my_list[j] == number:  
# #                     new_list = i, j  
# #     return list(new_list)
            
# # print(checker([2, 4, 8, 9, 15]))



# # def intro(**data):
# #     print("\nData type of argument:",type(data))

# #     for key, value in data.items():
# #         # print("{} is {}".format(key,value))
# #         print(f"{key} is {value}")


# # intro(Firstname="Sita", Lastname="Sharma", Age=22, Phone=1234567890)
# # intro(Firstname="John", Lastname="Wood", Email="johnwood@nomail.com", Country="Wakanda", Age=25, Phone=9876543210)





# class Laptop:
#     model = "HP"
    

#     def __init__(self, brand, color, size):
#         self.brand = brand
#         self.color = color
#         self.size = size
#         self.keyboard = "360 Keyboard"

# lap_1 = Laptop("Dell", "blue", 12)
# print(lap_1.model)
# print(lap_1.keyboard)

# # print(emp_1.salary)
# # emp_1.raise_percentage= 1.40
# # print(emp_1.raise_salary())

# # print(emp_2.salary)
# # print(emp_2.raise_salary())

# # print(emp_1.salary)
# # emp_1.raise_salary()
# # print(emp_1.salary)

# # emp_1.company_name = "Unilag"
# # print(emp_1.company_name)
# # print(emp_2.company_name)


 
# # print(emp_1.profile())
# # print(emp_1.company_name)

# # print(emp_1.email)
# # print(emp_2.profile())

    



    












