""""""


from celestine.typed import (
    OBJ,
    SELF,
    B,
    N,
    Z,
)


class Point:
    """"""

    point_x: Z
    point_y: Z

    def __init__(self, point_x: Z, point_y: Z):
        self.point_x = point_x
        self.index_y = point_y

    def __repr__(self):
        return f"Point({self.point_x}, {self.point_y})"

    def __str__(self):
        return f"({self.point_x}, {self.point_y})"


class Axis:
    """"""

    point: Z
    size: Z

    @classmethod
    def clone(cls, self: SELF) -> SELF:
        """"""
        return cls(self.point, self.size)

    def copy(self) -> SELF:
        """"""
        return self.clone(self)

    @classmethod
    def copy(cls, axis: SELF) -> SELF:
        """"""
        return cls(axis.point, axis.size)

    def index(self) -> Z:
        """"""
        return self.point

    def move(self, point: Z) -> N:
        """"""
        self.point += point

    def valid(self) -> B:
        """"""
        return 0 <= self.point < self.size

    def __eq__(self, other: OBJ) -> B:
        """"""
        if not isinstance(other, Axis):
            return False

        point = self.point == other.point
        size = self.size == other.size
        return point and size

    def __init__(self, point: Z, size: Z) -> N:
        """"""
        self.point = point
        self.size = size


class Grid:
    """"""

    axis_x: Axis
    axis_y: Axis
    size: Z

    @classmethod
    def clone(cls, self: SELF) -> SELF:
        """"""
        return cls(self.axis_x.clone(), self.axis_y.clone())

    def copy(self) -> SELF:
        """"""
        return self.clone(self)

    def index(self) -> Z:
        """"""
        return self.axis_y.point * self.axis_x.size + self.axis_x.point

    def valid(self) -> B:
        """"""
        return self.axis_x.valid() and self.axis_y.valid()

    def __eq__(self, other: OBJ) -> B:
        """"""
        if not isinstance(other, Grid):
            return False

        axis_x = self.axis_x == other.axis_x
        axis_y = self.axis_y == other.axis_y
        return axis_x and axis_y

    def __init__(self, axis_x: Axis, axis_y: Axis) -> N:
        """"""
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.size = axis_x.size * axis_y.size
