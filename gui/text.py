# from mem_dixy.tag.alphabet import convert
# from mem_dixy.tag.alphabet import tag
# from mem_dixy.tag.alphabet import hashy
# from mem_dixy.tag.alphabet import space
from mem_dixy.tag.alphabet import *
from mem_dixy.Unicode.U0000 import LOW_LINE


from enum import Enum


class State(Enum):
    NONE = 1
    TAG = 2
    HASH = 3
    SPACE = 3
    SYMBOL = 4


# string = input("you ugly")
string = "-🌋 Volcano🏕️ Camping🏜️ Desert 1girl __vodo__on__!!||?#$&& pie"


falcon = []

for character in string:
    falcon.append(convert.get(character, str()))

bird = str().join(falcon)

tigger = []
mouse = []

state_now = State.NONE
state_past = State.NONE


class Atoken:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


print(VERTICAL_LINE)
print(EXCLAMATION_MARK)
print(AMPERSAND)


print(AMPERSAND in sql_and)
print(EXCLAMATION_MARK)
print(AMPERSAND)


class AND(Atoken):
    def __init__(self, value):
        super().__init__(AMPERSAND)


class IS(Atoken):
    def __init__(self, value):
        super().__init__(PLUS_SIGN)


class NOT(Atoken):
    def __init__(self, value):
        super().__init__(HYPHEN_MINUS)


class OR(Atoken):
    def __init__(self, value):
        super().__init__(VERTICAL_LINE)


class Atag(Atoken):
    def __init__(self, value):
        super().__init__(value)


class Asymbol(Atoken):
    def __init__(self, value):
        super().__init__("&")


def add_token():
    global tigger
    global mouse
    value = str().join(tigger)
    hold = []
    start = False
    end = False
    for character in value:
        start = character is not LOW_LINE
        end |= start
        if end:
            hold.append(character)

    value = str().join(hold)
    cat = Atag(value)

    mouse.append(cat)
    tigger = []


now = False
last = False
for character in bird:
    now = character in two_token
    if last and not now:
        add_token()

    if character in all_token:
        tigger.append(character)

    if character in one_token:
        add_token()

    last = now

add_token()

print(string)
print(bird)
print(tigger)
print(mouse)
