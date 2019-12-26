import random


class ReturnDirections():
    NORTH = '\"North\"'
    SOUTH = '\"South\"'
    EAST = '\"East\"'
    WEST = '\"West\"'
    STOP = '\"Stop\"'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST: NORTH,
            WEST: SOUTH,
            STOP: STOP}

    RIGHT = dict([(y, x) for x, y in LEFT.items()])

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}

    @classmethod
    def random(cls):
        return random.choice(
            [ReturnDirections.SOUTH, ReturnDirections.NORTH, ReturnDirections.EAST, ReturnDirections.WEST,
             ReturnDirections.STOP])
