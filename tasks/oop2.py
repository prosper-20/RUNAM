class Human:
    has_hair = True

    def __init__(self, name, age, language, country):
        self.name = name
        self.age = age
        self.language = language
        self.country = country


    
    def background(self):
        return f"Hello {self.name}, you are a citizen of {self.country}"
    

list



class Africans(Human):
    def __init__(self, name, age, language, country, color):
        super().__init__(name, age, language, country)
        self.color = color

    def background(self):
        return f"Hello {self.name}, you are a citizen of {self.country}"
    


class Black(Africans):
    def __init__(self, name, age, language, country, color):
        super().__init__(name, age, language, country, color)


    

man_1 = Africans("prosper", "78", "english", "Nigeria", "black")

print(isinstance(man_1, Human))

print(issubclass(Black, Human))






# print(man_1.background())




    
    

# class European(African):
#     def __init__(self, name, age, language, country):
#         super().__init__(name, age, language, country)
#         self.complexion = "white"
    


# human_1 = Human("Uju", 18, "Yoruba", "Nigeria")

# print(isinstance(human_1, European))
# print(issubclass(European, Human))

# var = African("Yusuf", 30, "Swahili", "Namibia")
# var2 = European("Jane", 45, "English", "U.S.A")
# print(var2.complexion)
# print(var.background())



    



    



    