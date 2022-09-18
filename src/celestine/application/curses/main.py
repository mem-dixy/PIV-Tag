"""Package celestine."""
import curses
from celestine.application.window import Window as Window_
from celestine.application.window import Frame as Frame_


HEIGHT = 24
WIDTH = 80


class Frame(Frame_):
    def clear(self):
        self.frame.clear()

    def noutrefresh(self):
        self.frame.noutrefresh()


class Cursor():
    def __init__(self, session, stdscr):
        self.session = session
        self.stdscr = stdscr
        self.cord_x = 0
        self.cord_y = 0
        self.width = WIDTH
        self.height = HEIGHT

    def move(self):
        self.stdscr.move(self.cord_y, self.cord_x)

    def input(self, key):
        (cord_x, cord_y) = self.session.python.curses_cursor_input_match(
            key,
            curses,
            self.cord_x,
            self.cord_y
        )
        self.cord_x = cord_x % self.width
        self.cord_y = cord_y % self.height


class Widget():
    def __init__(self, column, row, width, height):
        self.cord_x = column
        self.cord_y = row
        self.width = width
        self.height = height
        self.type = "wiget"

    def select(self, cord_x, cord_y):
        temp_a = cord_x >= self.cord_x
        temp_b = cord_x < self.cord_x + self.width
        temp_c = cord_y >= self.cord_y
        temp_d = cord_y < self.cord_y + self.height
        return temp_a and temp_b and temp_c and temp_d

    def unselect(self, cord_x, cord_y):
        return not self.select(cord_x, cord_y)


class String(Widget):
    def __init__(self, x, y, text):
        super().__init__(x, y, len(text), 1)
        self.text = text
        self.type = "string"

    def draw(self, window):
        window.addstr(self.cord_y, self.cord_x, self.text)


class Widget():
    def __init__(self, frame, item, kind):
        self.frame = frame
        self.item = item
        self.type = kind
        self.cord_x = 0
        self.cord_y = 0
        self.width = 0
        self.height = 0

    def select(self, cord_x, cord_y):
        temp_a = cord_x >= self.cord_x
        temp_b = cord_x < self.cord_x + self.width
        temp_c = cord_y >= self.cord_y
        temp_d = cord_y < self.cord_y + self.height
        return temp_a and temp_b and temp_c and temp_d

    def unselect(self, cord_x, cord_y):
        return not self.select(cord_x, cord_y)

    def grid(self, cord_x, cord_y):
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.width = len(self.item)
        self.height = 1
        self.frame.addstr(cord_y, cord_x * 20, self.item)


class Button(Widget):
    def __init__(self, frame, text):
        super().__init__(
            frame,
            F"button:{text}",
            "button",
        )


class Label(Widget):
    def __init__(self, frame, text):
        super().__init__(
            frame,
            F"label:{text}",
            "label",
        )


class Curses():
    @staticmethod
    def window(column, row, width, height):
        nlines = height
        ncols = width
        begin_y = row
        begin_x = column
        return curses.newwin(nlines, ncols, begin_y, begin_x)

    @staticmethod
    def subwindow(window, column, row, width, height):
        nlines = height
        ncols = width
        begin_y = row
        begin_x = column
        return window.subwin(nlines, ncols, begin_y, begin_x)

    @staticmethod
    def doupdate():
        curses.doupdate()


class Window(Window_):

    def __init__(self, session):
        super().__init__(session)
        ignore = None

    def show_frame(self, index):
        return self.frame_get(index)

    def image_load(self, file):
        return file

    def curses_string(self, frame, tag, string, cord_x, cord_y):
        window = self.frame_get(frame)
        thing = String(cord_x, cord_y, string)
        thing.draw(window)
        self.item_set(frame, tag, thing)

    def button(self, frame, tag, label, _):
        item = Button(
            self.frame_get(frame),
            label,
        )
        self.item_set(frame, tag, item)
        return item

    def file_dialog(self, frame, tag, _):
        item = Label(
            self.frame_get(frame),
            "File dialog thing.",
        )
        self.item_set(frame, tag, item)
        return item

    def image(self, frame, tag, _image):
        item = Label(
            self.frame_get(frame),
            _image,
        )
        self.item_set(frame, tag, item)
        return item

    def label(self, frame, tag, label):
        item = Label(
            self.frame_get(frame),
            label,
        )
        self.item_set(frame, tag, item)
        return item

    def main_it(self, stdscr):
        key = ord(' ')

        cursor = Cursor(self.session, stdscr)

        background = Curses.window(0, 0, WIDTH, HEIGHT)
        background.box()

        header1 = Curses.subwindow(background, 0, 0, WIDTH, 1)
        header1.addstr(self.session.language.APPLICATION_TITLE)

        header2 = Curses.subwindow(background, 0, HEIGHT - 1, WIDTH, 1)
        header2.addstr(self.session.language.CURSES_EXIT)

        for index in range(len(self.session.window)):
            frame = Curses.window(
                1,
                1,
                WIDTH - 1,
                HEIGHT - 2,
            )
            self.frame_set(index, frame)

        display_it_now = 0

        frame = self.show_frame(display_it_now)
        self.session.window[0].main(self.session, 0, self)

        #  refresh
        stdscr.noutrefresh()
        background.noutrefresh()
        frame.noutrefresh()
        Curses.doupdate()

        while key != ord('q'):

            if key == ord(' '):

                for key, thing in self.item[display_it_now].item.items():
                    if thing.select(cursor.cord_x - 1, cursor.cord_y - 1):
                        if thing.type == "button":
                            new = thing.item.split(":")[1]
                            indexer = int(new.split(" ")[1])

                            frame.clear()
                            frame = self.frame_get(indexer)

                            self.session.window[indexer].main(
                                self.session, indexer, self)

                            display_it_now = indexer

                            #  refresh
                            stdscr.noutrefresh()
                            background.noutrefresh()
                            frame.noutrefresh()
                            Curses.doupdate()

            cursor.input(key)
            cursor.move()

            key = stdscr.getch()

    def main(self):
        curses.wrapper(self.main_it)
