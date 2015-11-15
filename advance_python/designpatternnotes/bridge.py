# _*_ coding=utf-8 _*_
__author__ = 'patrick'

"""http://en.wikibooks.org/wiki/Computer_Science_Design_Patterns/Bridge_Pattern#Python"""


class DrawingAPI:
    def __init__(self):
        pass

    def draw_circle(self, x, y, radius):
        print('API1.circle at {}:{} radius {}'.format(x, y, radius))


class Drawing2API:
    def __init__(self):
        pass

    def draw_circle(self, x, y, radius):
        print('API2.circle at {}:{} radius {}'.format(x, y, radius))


class CircleShape:
    def __init__(self, x, y, radius, draw_api):
        self.x = x
        self.y = y
        self.radius = radius
        self.draw_api = draw_api

    def draw(self):
        self.draw_api.draw_circle(self.x, self.y, self.radius)

    def scale(self, pct):
        self.radius *= pct

"""
bridge: initialize the class with different target class, it looks like different strategy
"""


def main():
    shapes = (
        CircleShape(1, 2, 3, DrawingAPI()),
        CircleShape(5, 7, 11, Drawing2API())
    )

    for shape in shapes:
        shape.scale(2.5)
        shape.draw()


if __name__ == '__main__':
    main()