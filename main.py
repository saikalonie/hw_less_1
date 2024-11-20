#ООП - объектно ориентировочнное программирование

types_python = 1, 'str', 1.45, True, (), {}, []

print(type(types_python))
class Car:
    def drive(self):
        print('Машина едет ')

    def __init__(self, model, volume, age):
        self.model = model
        self.volume = volume
        self.age = age
        print(self.model, self.volume, self.age)

    def __str__(self):
        return f'Модель: {self.model}, Год: {self.age}'

audi = Car("audi", "2,8", "2000")
mazda = Car("A8", "2,5","2004")

audi.drive()

print(audi)
print(mazda)
