"""Task No.1"""
class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

    def introduce (self):
        print(f'Привет меня зовут {self.name}, мне {self.age} лет и я живу в городе {self.city}')

    def is_adult (self):
        return self.age >= 18

first_person = Person("Saikal", 19, "Bishkek")
second_person = Person("Sezim", 18, "Ankara")
third_person = Person("Aidai", 25, "Dusseldorf")
forth_person = Person("Aijarkyn", 13, "Bishkek")


first_person.introduce()
print(f"Совершеннолетний: {first_person.is_adult()}")
second_person.introduce()
print(f"Совершеннолетний: {second_person.is_adult()}")
third_person.introduce()
print(f"Совершеннолетний: {third_person.is_adult()}")
forth_person.introduce()
print(f"Совершеннолетний: {forth_person.is_adult()}")
