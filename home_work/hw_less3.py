from abc import ABC, abstractmethod


class Room(ABC):
    def __init__(self, features, price):
        self._features = features
        self.__price = price

    @abstractmethod
    def get_features(self):
        """Метод для получения списка удобств"""
        pass

    @abstractmethod
    def get_price(self):
        """Метод для получения стоимости номера"""
        pass


class WiFiService:
    def wifi_description(self):
        return "Услуга Wi-Fi предоставляется бесплатно."


class BreakfastService:
    def breakfast_description(self):
        return "Завтрак включен в стоимость номера."


class StandardRoom(Room):
    def get_features(self):
        return self._features

    def get_price(self):
        return self._Room__price


class FamilyRoom(Room, WiFiService):
    def get_features(self):
        features = self._features.copy()
        features.append(self.wifi_description())
        return features

    def get_price(self):
        return self._Room__price


class LuxuryRoom(Room, WiFiService, BreakfastService):
    def get_features(self):
        features = self._features.copy()
        features.append(self.wifi_description())
        features.append(self.breakfast_description())
        return features

    def get_price(self):
        return self._Room__price


standard = StandardRoom(["Телевизор", "Душ"], 3000)

family = FamilyRoom(["Телевизор", "Ванна"], 5000)

luxury = LuxuryRoom(["Двуспальная кровать", "PlayStation"], 8000)


print("Standard Room: ")
print(f'Цена: {standard.get_price()} сомов')
print(f"Удобство 1: {standard.get_features()[0]}")
print(f"Удобство 2: {standard.get_features()[1]}")
print("-"*20)

print("Family Room: ")
print(f'Цена: {family.get_price()} сомов')
print(f"Удобство 1: {family.get_features()[0]}")
print(f"Удобство 2: {family.get_features()[1]}")
print(f"Удобство 3: {family.get_features()[2]}")
print("-"*20)

print("Luxury Room: ")
print(f'Цена: {luxury.get_price()} сомов')
print(f"Удобство 1: {luxury.get_features()[0]}")
print(f"Удобство 2: {luxury.get_features()[1]}")
print(f"Удобство 3: {luxury.get_features()[2]}")
print(f"Удобство 4: {luxury.get_features()[3]}")
print("-"*20)
