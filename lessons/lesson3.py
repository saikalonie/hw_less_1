#Инкапсуляция

#Уровни

class BankAccount:

    def __init__(self, name, age, balance):
        self.name = name
        self._age = age
        self.__balance = balance
        self._validate_age(age)

    def _validate_age(self, age):
        if age < 18:
            raise ValueError("Возраст должен быть 18+")

    def get_age(self):
        return self._age

    def set_age(self, new_age):
        self._validate_age(new_age)
        self._age = new_age
        print(f'Возраст изменен на {self._age}')

    # def set_balance(self, amount):
    #     if amount <= 0:
    #         raise ValueError('Баланс должен быть положительным')
    #     self.__balance = amount
    #     print(f'Баланс изменен на {self.__balance}')

    # def get_balance(self):
    #     return self.__balance

    def __str__(self):
        return (f'name: {self.name}\n'
                f'age: {self._age}\n'
                f'balance: {self.__balance}\n')

# Создаем объекты
beka = BankAccount("Bekbolot", 19, 100000)
print(beka)

beka.set_age(29)
beka._BankAccount__balance = 12
# beka.set_balance(15000)

print(f'Текущий возраст: {beka.get_age()}')
# print(f'Текущий баланс: {beka.get_balance()}')

print(dir(beka))

saikal = BankAccount("Saikal", 19, 200)
print(saikal)
