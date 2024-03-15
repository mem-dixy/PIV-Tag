""""""

import math

from celestine.typed import (
    LS,
    A,
    B,
    D,
    H,
    K,
    N,
    I,
    R,
    S,
    override,
)
from celestine.window import container
from celestine.window.collection import (
    Abstract,
    Area,
    Point,
    Line,
    Plane,
    Tree,
)
from celestine.window.container import Image as Mode


class Element(Abstract):
    """"""


class View(Abstract, Tree):
    """"""

    item: D[S, Abstract]

    def find(self, name: S) -> N | Abstract:
        """"""
        for key, value in self:
            if key == name:
                return value
            if not getattr(value, "find", False):
                continue
            item = value.find(name)
            if item:
                return item
        return None

    def click(self, point: Point, **star: R) -> B:
        if not super().click(point, **star):
            return False

        for _, item in self:
            item.click(point)

        return True

    @override
    def draw(self, **star: R) -> N:
        """"""
        if self.hidden:
            return

        for _, item in self:
            item.draw(**star)

    @override
    def make(self, canvas: A) -> N:
        """"""
        for _, item in self:
            item.make(canvas)

    @override
    def spot(self, area: Area) -> N:
        """"""
        def under_spot(
            this, index_x: I, index_y: I, partition_x: I, partition_y: I
        ) -> Plane:
            """"""
            size_x = this.one.length
            size_y = this.two.length

            fragment_x = size_x // partition_x
            fragment_y = size_y // partition_y

            left = this.one.minimum
            upper = this.two.minimum

            ymin = upper + fragment_y * (index_y + 0)
            ymax = upper + fragment_y * (index_y + 1)
            xmin = left + fragment_x * (index_x + 0)
            xmax = left + fragment_x * (index_x + 1)

            one = Line(xmin, xmax)
            two = Line(ymin, ymax)

            return Plane(one, two)

        super().spot(area)
        length = max(1, len(self))

        match self.mode:
            case container.Zone.DROP:
                partition_x = 1
                partition_y = length
            case container.Zone.SPAN:
                partition_x = length
                partition_y = 1
            case container.Zone.GRID:
                partition_x = self.width
                partition_y = math.ceil(length / self.width)
            case container.Zone.NONE:
                partition_x = 1
                partition_y = 1

        index = 0
        for _, item in self:
            index_x = index % partition_x
            index_y = min(index // partition_x, partition_y - 1)
            index += 1

            world = under_spot(
                self.area.world,
                index_x,
                index_y,
                partition_x,
                partition_y,
            )
            local = under_spot(
                self.area.world,
                index_x,
                index_y,
                partition_x,
                partition_y,
            )
            local -= area.world.origin

            rectangle = Area(local, world)
            item.spot(rectangle)

    def zone(
        self,
        name: S,
        *,
        mode=container.Zone.NONE,
        **star: R,
    ) -> K:
        """"""
        return self.set(
            self._view(
                self.hold,
                name,
                self.element_item,
                mode=mode,
                parent=self,
                **star,
            )
        )

    def drop(self, name: S, **star: R) -> K:
        """"""
        return self.zone(name, mode=container.Zone.DROP, **star)

    def span(self, name: S, **star: R) -> K:
        """"""
        return self.zone(name, mode=container.Zone.SPAN, **star)

    def __enter__(self) -> K:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> B:
        if exc_type or exc_value or traceback:
            print("ERROR")
        return False

    def __init__(
        self,
        hold,
        name,
        element_item,
        *,
        mode=container.Zone.NONE,
        row=0,
        col=0,
        **star: R,
    ) -> N:
        #
        self.element_item = element_item
        self._element = element_item["element"]
        self._view = element_item["view"]
        self._window = element_item["window"]

        super().__init__(hold, name, **star)

        self.width = col
        self.height = row
        self.mode = mode

        for range_y in range(row):
            for range_x in range(col):
                name = f"{self.name}_{range_x}-{range_y}"
                self.set(
                    Abstract(
                        hold,
                        name,
                        self,
                    )
                )

    def element(self, name: S, **star: R) -> N:
        """"""
        self.set(
            self._element(
                self.hold,
                name,
                self,
                **star,
            )
        )

    # syntax sugar

    def button(self, name: S, task: S, /, text: S, **star: R) -> N:
        self.element(name, action=task, text=text, **star)

    def link(self, name: S, task: S, /, text: S, **star: R) -> N:
        self.element(name, goto=task, text=text, **star)

    def icon(self, name: S, /, **star: R) -> N:
        self.element(name, fit=Mode.FILL, **star)

    def image(self, name: S, /, **star: R) -> N:
        self.element(name, fit=Mode.FULL, **star)

    def label(self, name: S, /, text: S, **star: R) -> N:
        self.element(name, text=text, **star)


class Window(Tree):
    """"""

    hold: H
    page: View
    code: D[S, A]  # function
    view: D[S, View]

    canvas: A

    def extension(self) -> LS:
        """"""
        return [
            ".bmp",
            ".sgi",
            ".rgb",
            ".bw",
            ".png",
            ".jpg",
            ".jpeg",
            ".jp2",
            ".j2c",
            ".tga",
            ".cin",
            ".dpx",
            ".exr",
            ".hdr",
            ".tif",
            ".tiff",
            ".webp",
            ".pbm",
            ".pgm",
            ".ppm",
            ".pnm",
            ".gif",
            ".png",
        ]

    def drop(
        self,
        name: S,
        **star: R,
    ) -> K:
        """"""
        return self.set(
            self.element_item["view"](
                self.hold,
                name,
                self.element_item,
                mode=container.Zone.DROP,
                parent=self,
                **star,
            )
        )

    ###############
    # star might not be needed for all functions
    # but it will stay for now for ease of itegration later

    def click(self, point: Point, **star: R) -> N:
        """"""
        # check
        for _, item in self:
            item.click(point, **star)

    def draw(self, **star: R) -> N:
        """"""
        # check
        for _, item in self:
            item.draw(**star)

    def make(self) -> N:
        """"""
        for _, item in self:
            item.make(self.canvas)

    def spot(self, area: Area, **star: R) -> N:
        """"""
        # check
        self.area = area
        for _, item in self:
            item.spot(area, **star)

    ###############
    # No star functions

    def find(self, name: S) -> N | Abstract:
        """"""
        for key, value in self:
            if key == name:
                return value
            item = value.find(name)
            if item:
                return item
        raise KeyError(name)

    ###############

    def turn(self, page: S, **star: R) -> N:
        """"""
        view = self.view.get(page)
        if not view:
            return

        self.page.hide()
        self.page = view
        self.page.show()
        self.draw()

    def work(self, code: S, **star: R) -> N:
        """"""
        caller = self.code.get(code)
        if not caller:
            return

        caller(self.hold, **star)
        self.draw(**star)

    def __enter__(self) -> K:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            raise exc_type
        if exc_value:
            raise exc_value
        if traceback:
            raise traceback

        self.spot(self.area)
        self.make()

        for _, item in self:
            item.hide()

        self.turn(self.hold.main)

        return False

    def __init__(self, hold: H, element_item, **star: R) -> N:
        super().__init__(**star)
        self.area = Area.make(0, 0)
        self.hold = hold
        self.code = {}
        self.view = {}
        self.element_item = element_item
        self.page = View(hold, "", element_item, parent=None)
