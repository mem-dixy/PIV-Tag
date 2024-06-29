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
    LS,
    A,
    B,
    K,
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

    image: pygame.Surface
    text_item: A

    @override
    def draw(self, **star: R) -> B:
        """"""
        if not super().draw(**star):
            return False

        dest = self.area.world.origin.value

        def render(source: A) -> N:
            """"""
            if source:
                self.canvas.blit(source, dest)

        render(self.image)
        render(self.text_item)

        return True

    @override
    def make(self, canvas: A, **star: R) -> N:
        """"""
        super().make(canvas, **star)
        self.font = star.pop("font")

        size = self.area.local.size.value

        self.image = pygame.Surface(size)

        if self.text:
            self.update_text(self.text)

        if self.path:
            self.update_image(self.path)

    def update_image(self, path: P, **star: R) -> N:
        """"""
        self.path = path

        # reset image
        self.image.fill((0, 0, 0))

        if pillow:
            image_pillow = pillow.open(self.path)
            width = image_pillow.image.width
            height = image_pillow.image.height
        else:
            image_pygame = pygame.image.load(self.path)
            width = image_pygame.get_width()
            height = image_pygame.get_height()

        # TODO got to figure out Area coordinates
        # or cach this somehow
        target = self.area.local
        target = Plane.make(*self.area.world.size.value)
        curent = Plane.make(width, height)
        match self.fit:
            case Image.FILL:
                curent.scale_to_min(target)
            case Image.FULL:
                curent.scale_to_max(target)
        curent.center(target)

        if pillow:
            image_pillow.resize(curent.size)

            buffer = image_pillow.image.tobytes()
            size = image_pillow.image.size
            format_ = image_pillow.image.mode
            source = pygame.image.frombuffer(buffer, size, format_)
        else:
            surface = image_pygame
            size = curent.size.value
            source = pygame.transform.smoothscale(surface, size)

        dest = curent.origin.value
        self.image.blit(source, dest)

    def update_text(self, text: S) -> N:
        """"""
        self.text = text
        antialias = True
        color = self.color
        background = None
        self.text_item = self.font.render(
            text,
            antialias,
            color,
            background,
        )

    def __init__(self, name: S, parent: K, **star: R) -> N:
        super().__init__(name, parent, **star)
        self.path = star.pop("path", "")
        self.color = (255, 0, 255)
        self.font = None

        self.text_item = None


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
    def make(self, **star: R) -> N:
        """"""
        super().make(font=self.font, **star)

    @override
    def run(self) -> N:
        super().run()

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

    @override
    def __init__(self, **star: R) -> N:
        element = {
            "element": Element,
            "view": View,
            "window": self,
        }
        super().__init__(element, **star)
        self.area = Area.make(1920, 1080)

        value = self.area.world.size.value
        self.canvas = pygame.display.set_mode(value)

        caption = bank.language.APPLICATION_TITLE
        pygame.display.set_caption(caption)

        pygame.font.init()
        file_path = load.asset("cascadia_code_regular.otf")
        size = 40
        self.font = pygame.font.Font(file_path, size)
