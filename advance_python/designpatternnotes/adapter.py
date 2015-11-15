# _*_ coding=utf-8 _*_
__author__ = 'patrick'


class Dog(object):
    def __init__(self):
        self.name = "DOG"

    def bark(self):
        return "I am a Dog not god"


class Cat(object):
    def __init__(self):
        self.name = "CAT"

    def meow(self):
        return "meow!"


class Human(object):
    def __init__(self):
        self.name="HUMAN"

    def speak(self):
        return "I am Human Being"


class Car(object):
    def __init__(self):
        self.name = "CAR"

    def make_noise(self, octane_level):
        return "vroom{0}".format("!" * octane_level)


class Adapter(object):

    """
    Adapts an object by replacing methods.
    Usage:
    dog = Dog()
    dog = Adapter(dog, dict(make_noise = dog.bark)

    """

    def __init__(self,obj, adapter_methods):
        self.obj = obj
        self.__dict__.update(adapter_methods)

    def __getattr__(self, item):
        return getattr(self.obj, item)
"""
Adaptor class is the key which adapt the methods
it looks like method transformer
"""

def main():
    objects = []
    dog = Dog()
    objects.append(Adapter(dog, dict(make_noise=dog.bark)))
    cat = Cat()
    objects.append(Adapter(cat, dict(make_noise=cat.meow)))
    human = Human()
    objects.append(Adapter(human, dict(make_noise=human.speak)))
    car = Car()
    objects.append(Adapter(car, dict(make_noise=lambda: car.make_noise(3))))

    for obj in objects:
        print ("A {0} goes {1}".format(obj.name, obj.make_noise()))

if __name__ == '__main__':
    main()
