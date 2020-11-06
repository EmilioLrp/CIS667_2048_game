from enum import Enum


class Action(Enum):
    """
    7,8,9
    4, ,6
    1,2,3
    """
    up = "8",
    down = "2",
    left = "4",
    right = "6",
    upLeft = "7",
    upRight = "9",
    downLeft = "1",
    downRight = "3",

    def get_value(self) -> str:
        return self.value[0]

    @classmethod
    def left_direction(cls, action: str) -> bool:
        if action in [cls.up.get_value(), cls.left.get_value(), cls.upLeft.get_value(),
                      cls.upRight.get_value()]:
            return True
        return False
