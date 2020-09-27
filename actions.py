from getkey import keys


class Action:
    # up = keys.UP
    # down = keys.DOWN
    # left = keys.LEFT
    # right = keys.RIGHT
    def __int__(self):
        self._actions = {
            "up": keys.UP,
            "down": keys.DOWN,
            "left": keys.LEFT,
            "right": keys.RIGHT
        }

    def get_action(self):
        return self._actions


