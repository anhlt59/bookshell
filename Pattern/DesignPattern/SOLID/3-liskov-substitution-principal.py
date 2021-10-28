# LISKOV SUBSTITUTION PRINCIPAL
# https://en.wikipedia.org/wiki/Liskov_substitution_principle
# If S is a subtype of T, then objects of type T in a program may be replace
#   with objects of type S without altering any of the desirable properties of that program


# MISTAKE
# ----------------------------------------------------------------------------
# đảm bảo tất cả method/function liên quan tới 1 class,
# khi nó kế thừa từ base class phải không gây ra lỗi
class Rectangle:
    def __init__(self, width, height):
        self._height = height
        self._width = width

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        return f"Width: {self.width}, height: {self.height}"

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value


class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value


def use_it(rc):
    w = rc.width
    rc.height = 10  # unpleasant side effect
    expected = int(w * 10)
    print(f'with: {rc.width}\nheight: {rc.height}')
    print(f"Expected an area of {expected}, got {rc.area}")


# Square kế thừa từ Rectangle
# function use_it hoạt động đúng trên Rectangle
# nhưng không đúng trên Square, dẫn đến vi phạm LISKOV

rc = Rectangle(2, 3)
use_it(rc)
sq = Square(5)
use_it(sq)
