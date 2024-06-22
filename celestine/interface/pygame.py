""""""

import enum

from celestine import (
    bank,
    load,
)
from celestine.interface import Abstract as Abstract_
from celestine.interface import Element as Element_
from celestine.interface import View as View_
from celestine.interface import Window as Window_
from celestine.package import (
    pillow,
    pygame,
)
from celestine.typed import (
    BF,
    LS,
    A,
    B,
    K,
    M,
    N,
    P,
    R,
    S,
    override,
)
from celestine.window.collection import (
    Area,
    Plane,
    Point,
)
from celestine.window.container import Image


class Mouse(enum.IntEnum):
    """Values returned by mouse click."""

    PRIMARY = 1
    MIDDLE = 2
    SECONDARY = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5
    TERTIARY = 6
    QUATERNARY = 7


class Abstract(Abstract_):
    """"""


class Element(Element_, Abstract):
    """"""

    image: M

    @override
    def draw(self, **star: R) -> B:
        """"""
        if not super().draw(**star):
            return False

        if self.image:
            bytes_ = self.image.image.tobytes()
            size = self.image.image.size
            format_ = self.image.image.mode
            flipped = False
            surface = pygame.image.fromstring(
                bytes_,
                size,
                format_,
                flipped,
            )
            self.render(surface)

        if self.text:
            font = star.pop("font")
            text = self.text
            antialias = True
            color = self.color
            background = None
            surface = font.render(text, antialias, color, background)
            self.render(surface)

        return True

    @override
    def make(self, canvas: A, **star: R) -> N:
        """"""
        size = self.area.world.size.value
        blender_mode = False
        if pillow and not blender_mode:
            self.image = pillow.new(size)
        else:
            self.image = None

        super().make(canvas, **star)

        if self.path:
            self.update(self.path)

    def render(self, source: A) -> N:
        """"""
        dest = self.area.world.origin.value
        area = None
        special_flags = 0
        self.canvas.blit(source, dest, area, special_flags)

    def update(self, path: P, **star: R) -> N:
        """"""
        self.path = path

        image = pillow.open(self.path)

        curent = Plane.make(image.image.width, image.image.height)
        target = Plane.make(*self.area.world.size.value)

        match self.fit:
            case Image.FILL:
                result = curent.scale_to_min(target)
            case Image.FULL:
                result = curent.scale_to_max(target)

        result.center(target)

        image.resize(result.size)
        self.image.paste(image, result)

    def __init__(self, name: S, parent: K, **star: R) -> N:
        super().__init__(name, parent, **star)
        self.path = star.pop("path", "")
        self.color = (255, 0, 255)


class View(View_, Abstract):
    """"""


class Window(Window_):
    """"""

    @override
    def draw(self, **star: R) -> N:
        """"""
        self.canvas.fill((0, 0, 0))

        super().draw(font=self.font, **star)

        pygame.display.flip()

    @override
    def extension(self) -> LS:
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

    @override
    def __enter__(self) -> K:
        super().__enter__()

        def set_caption() -> N:
            caption = bank.language.APPLICATION_TITLE
            pygame.display.set_caption(caption)

        def set_font() -> N:
            pygame.font.init()
            file_path = load.asset("cascadia_code_regular.otf")
            size = 40
            self.font = pygame.font.Font(file_path, size)

        set_caption()
        set_font()

        return self

    @override
    def __exit__(self, exc_type: A, exc_value: A, traceback: A) -> BF:
        super().__exit__(exc_type, exc_value, traceback)

        def set_icon() -> N:
            path = "icon.png"
            asset = load.asset(path)
            image = pygame.image.load(asset)
            icon = image.convert_alpha()
            pygame.display.set_icon(icon)

        set_icon()

        while True:
            bank.dequeue()
            event = pygame.event.wait()
            match event.type:
                case pygame.QUIT:
                    break
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == Mouse.PRIMARY:
                        self.click(Point(*pygame.mouse.get_pos()))
                case _:
                    pass

        pygame.quit()
        return False

    @override
    def __init__(self, **star: R) -> N:
        element = {
            "element": Element,
            "view": View,
            "window": self,
        }
        super().__init__(element, **star)
        self.area = Area.make(1280, 960)
        self.area = Area.make(1920, 1080)
        self.font = None

        value = self.area.world.size.value
        self.canvas = pygame.display.set_mode(value)
