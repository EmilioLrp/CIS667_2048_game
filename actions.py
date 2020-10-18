from enum import Enum


class Action(Enum):
    up = "u",
    down = "d",
    left = "l",
    right = "r",
    upLeft = "ul",
    upRight = "ur",
    downLeft = "dl",
    downRight = "dr"

    def get_value(self):
        return self.value[0]
