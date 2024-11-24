
from main import Hero

class Archer(Hero):

    def __init__(self, name, health=100, energy=100, arrows=20):
        super().__init__(name, health)
        self.energy = energy
        self.arrows = arrows

    def shoot_arrows(self):
        if self.arrows > 0 and self.energy >= 10:
            self.arrows -= 1
            self.energy -=10
            return f'{self.name} стреляет из лука\n Осталось лука:{self.arrows}, \n Осталось энергии: {self.energy}'
        elif self.energy <10:
            return f'У {self.name} недостаточно энергии для наненсения урона'
        else:
            return f'У {self.name} закончились стрелы'

    def restore_energy(self):
        self.energy +=10
        return f'{self.name} восстанавливает энергию, когда отдыхает'


    def action(self):
        base_action = super().action()
        shooting_action = self.shoot_arrows()
        return f'{base_action}\n{shooting_action}'

archer = Archer('Ланселот')
print(archer.introduce())
print(archer.rest())
print(archer.action())
print(archer.action())
print(archer.action())
print(archer.restore_energy())
print(archer.action())


