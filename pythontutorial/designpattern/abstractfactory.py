# _*_ coding=utf-8 _*_
import random

__author__ = 'patrick'


class PetShop:
    def __init__(self, animal_factory=None):
        self.pet_factory = animal_factory

    def show_pet(self):
        pet = self.pet_factory.get_pet()
        print("We have a lovely {}".format(pet))
        print ("IT says {}".format(pet.speak()))
        print ("We also have {}".format(self.pet_factory.get_food()))


class Dog:

    def __init__(self):
        pass

    def speak(self):
        print "woooo...."

    def __str__(self):
        return "I am a dog"


class Cat:

    def __init__(self):
        pass

    def speak(self):
        print "miao....."

    def __str__(self):
        return "I am a Cat"


class DogFactory:
    def __init__(self):
        pass

    def get_pet(self):
        return Dog()

    def get_food(self):
        return "dog food"


class CatFactory:
    def __init__(self):
        pass

    def get_pet(self):
        return Cat()

    def get_food(self):
        return "Cat Food"


def get_factory():
    return random.choice([DogFactory, CatFactory])()


if __name__ == '__main__':
    for i in range(3):
        factory = get_factory()
        pet_shop = PetShop(factory)
        pet_shop.show_pet()
        print "=" * 20