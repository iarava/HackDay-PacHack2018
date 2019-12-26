from app.dto.HelperDTOs import Directions


class PublicPlayer:
    def __init__(self, isPacman=True, direction=Directions.NORTH, position=[0, 0], jsonString=None, activeCapsule=False):
        self.isPacman = isPacman
        self.direction = direction
        self.position = position
        self.activeCapsule = activeCapsule
        if (jsonString != None):
            self.__dict__ = jsonString

    def __str__(self):
        returnVal = 'G'
        if self.direction == Directions.NORTH:
            returnVal = 'N'
        if self.direction == Directions.SOUTH:
            returnVal = 'S'
        if self.direction == Directions.WEST:
            returnVal = 'W'
        if self.direction == Directions.EAST:
            returnVal = 'E'
        if self.isPacman:
            return returnVal.lower()
        return returnVal.upper()