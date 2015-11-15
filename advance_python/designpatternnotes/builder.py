# _*_ coding=utf-8 _*_
__author__ = 'patrick'

""" Product class"""


class Building(object):
    def __init__(self, floor=None, size=None):
        self.floor = floor
        self.size = size

    def __repr__(self):
        return "floor {0}, size {1}".format(self.floor, self.size)


"""
    abstract builder
"""


class Builder(object):
    def __init__(self):
        self.building = None

    def new_building(self):
        self.building = Building()


"""
 Concrete Builder
"""


class HouseBuilder(Builder):
    def __init__(self):
        pass

    def build_floor(self):
        self.building.floor = "One"

    def build_size(self):
        self.building.size = "BIG"


class FlatBuilder(Builder):
    def __init__(self):
        pass

    def build_floor(self):
        self.building.floor = "Two"

    def build_size(self):
        self.building.size = "SMALL"


"""
Director, Architecture
"""


class Architecture(object):
    def __init__(self):
        self.builder = None

    def construct_building(self):
        self.builder.new_building()
        self.builder.build_floor()
        self.builder.build_size()

    def get_building(self):
        return self.builder.building


"""
client
"""


def client():
    arch = Architecture()
    arch.builder = HouseBuilder()
    arch.construct_building()
    print(arch.get_building())

    arch.builder = FlatBuilder()
    arch.construct_building()
    print(arch.get_building())


if __name__ == '__main__':
    client()