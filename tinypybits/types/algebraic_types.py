from copy import copy, deepcopy
from dataclasses import dataclass
from functools import partial
import inspect


def build_algebraic_type(class_name, variants):
    def make_classmethod_constructor(self, v):
        return v()

    def make_classmethod_constructor_with_args(cls, t, *args):
        print(t)
        return t(*args)

    attributes = {}
    for variant in variants:
        name = variant.__name__
        constructor_signature = inspect.signature(variant.__init__)
        parameter_count = len(constructor_signature.parameters)
        if parameter_count == 1:
            attributes[name] = staticmethod(variant)
        else:
            variant = deepcopy(variant)
            attributes[name] = staticmethod(lambda *args, **kwargs: variant(*args, **kwargs))

    return type(class_name, (), attributes)


@dataclass
class Quit:
    pass


@dataclass
class Move:
    x: float
    y: float


@dataclass
class Write:
    symbol: str


@dataclass
class Color:
    red: int
    green: int
    blue: int


MessageAuto = build_algebraic_type("MessageAuto", [Quit, Move, Write, Color])


class Message:
    @staticmethod
    def quit():
        return Quit()

    @staticmethod
    def move(x, y):
        return Move(x, y)

    @staticmethod
    def write(symbol):
        return Write(symbol)

    @staticmethod
    def color(r, g, b):
        return Color(r, g, b)


def execute(command):
    print(command)
    match command:
        case Quit():
            print("im quitting")
        case Move(x, y):
            print(f"Will move to ({x=}, {y=})")
        case Write(symbol):
            print(f"Will write symbol '{symbol}'")
        case Color(red, green, blue):
            print(f"Will color to RGB ({red},{green},{blue})")
        case _:
            print("No idea what yoy ask for")


execute(Message.quit())
execute(Message.move(1, 1))
execute(Message.write("$"))
execute(Message.color(255, 255, 255))

execute(MessageAuto.Quit())
execute(MessageAuto.Move(1, 1))