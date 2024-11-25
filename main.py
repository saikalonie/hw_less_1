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



class Hero:

    def __init__(self, name, health=100):
        self.name = name
        self.health = health

    def introduce(self):
        return f'Я {self.name} мое здоровье {self.health}'

    def rest(self):
        self.health += 10
        return f'{self.name} отдыхает и восстанавливает здоровье. Новое здоровье {self.health}'

    def action(self):
        return f'{self.name} Выполняет базовое действие'


class Mage(Hero):

    def __init__(self, name, health=100, mana=100):
        super().__init__(name, health)
        self.mana = mana

    def cast_spell(self):
        if self.mana >=10:
            self.mana -=10
            return f'{self.name} использует заклинание \n Огненный шар {self.mana}'
        else:
            return f'{self.name} недостаточно маны для заклинания'

    def action(self):
        base_action = super().action()
        spell_result = self.cast_spell()

        return f'{base_action}\n{spell_result}'


class Warrior(Hero):

    def __init__(self, name, health=150, strength=150, stamina=100):
        super().__init__(name, health)
        self.strength = strength
        self.stamina = stamina

    def charge_attack(self):
        if self.stamina >= 20:
            self.stamina -= 20
            damage =self.strength * 2
            return f'{self.name} наносит мощный удар, нанося {damage} урона \nОсталось выносливости {self.stamina}'

    def action(self):
        base_action = f"{self.name} за победу!"
        attack_result = self.charge_attack()
        return f'{base_action}\n{attack_result}'

def hero_action(hero):
    print(hero.introduce())
    print(hero.rest())
    print(hero.action())

mage = Mage('Сесилион')
warrior = Warrior('Циклоп')

hero_action(mage)
print()
hero_action(warrior)
