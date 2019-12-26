import random
import bottle
import os
import numpy as np

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections
from app.dto.HelperDTOs import PublicFields

@bottle.post('/start')
def start():
    return "RandomTemplate"

def swapPosition(player):
    pos = player['position']
    swap = int(pos[0])
    pos[0] = int(player['position'][1])
    pos[1] = int(swap)

def getObjForLocation(gamefield, location):
    gamefield[location[0], location[1]]

def getObjectsAroundLocation(gamefield, location):
    northObj =  gamefield[location[0], location[1] + 1]
    southObj = gamefield[location[0], location[1] - 1]
    ostObj = gamefield[location[0] - 1, location[1]]
    westObj = gamefield[location[0] + 1, location[1]]


    return [northObj, southObj, ostObj, westObj]

def getLocationsAroundLocation(gamefield, location):

    north = [location[0], location[1] + 1]
    south = [location[0], location[1] - 1]
    ost = [location[0] - 1, location[1]]
    west = [location[0] + 1, location[1]]

    return [north, south, ost, west]

def heuristic(data, myplayer, x_current, y_current, value):
    if (data.publicPlayers[1 - myplayer]['isPacman']) == False:
        if data.publicPlayers[1 - myplayer]['weakened']:
            value = -1000
        else:
            value = value + 20

    if data.gameField[x_current][y_current] == PublicFields.WALL:
        value = -100
    if data.publicPlayers[myplayer]['isPacman']:
        if data.gameField[x_current][y_current] == PublicFields.FOOD:
            value = value + 5
        elif data.gameField[x_current][y_current] == PublicFields.CAPSULE:
            value = value + 10
        elif data.gameField[x_current][y_current] == PublicFields.EMPTY:
            value = value + 1

    if data.publicPlayers[myplayer]['isPacman'] == False:
        if data.gameField[x_current][y_current] == PublicFields.EMPTY:
            value = value + 1


    return value

def goThroughLocationsRecursive(data, gamefield, myPlayer, x_current, y_current, currentValue, current_depth):

    currentValue = heuristic(data, myPlayer, x_current, y_current, currentValue)

    if currentValue >= 0 | current_depth < 10:
        west = goThroughLocationsRecursive(data, gamefield, myPlayer, x_current - 1, y_current, currentValue, current_depth + 1)
        east = goThroughLocationsRecursive(data, gamefield, myPlayer, x_current + 1, y_current, currentValue, current_depth + 1)
        north = goThroughLocationsRecursive(data, gamefield, myPlayer, x_current, y_current - 1, currentValue, current_depth + 1)
        south = goThroughLocationsRecursive(data, gamefield, myPlayer, x_current, y_current + 1, currentValue, current_depth + 1)
        #print([west, east, north, south])
        return max([west, east, north, south])
    else:
        #print(currentValue)
        return currentValue



@bottle.post('/chooseAction')
def move():
    data = PublicGameState(ext_dict=bottle.request.json)
    id = data.agent_id

    gamefield = np.array(data.gameField)
    ratingfield = gamefield.copy()

    myPlayer = data.publicPlayers[id]

    if id == 1:
        enemyPlayer = data.publicPlayers[0]
    else:
        enemyPlayer = data.publicPlayers[1]

    swapPosition(myPlayer)
    swapPosition(enemyPlayer)

    enemyPosition = enemyPlayer['position']
    myPosition = myPlayer['position']




    north_start = 0
    south_start = 0
    east_start = 0
    west_start = 0

    if myPlayer['direction'] == "North":
        north_start += 10
    if myPlayer['direction'] == "South":
        south_start += 10
    if myPlayer['direction'] == "East":
        east_start += 10
    if myPlayer['direction'] == "West":
        west_start += 10

    if id == 0:
        east_start += 5
    else:
        west_start += 5

    north_val = goThroughLocationsRecursive(data, gamefield, id, x_current=myPosition[0] + 1, y_current=myPosition[1], currentValue=north_start, current_depth = 0)
    south_val = goThroughLocationsRecursive(data, gamefield, id, x_current=myPosition[0] - 1, y_current=myPosition[1], currentValue=south_start, current_depth=0)
    east_val = goThroughLocationsRecursive(data, gamefield, id, x_current=myPosition[0], y_current=myPosition[1] + 1, currentValue=east_start, current_depth=0)
    west_val = goThroughLocationsRecursive(data, gamefield, id, x_current=myPosition[0], y_current=myPosition[1] - 1, currentValue=west_start, current_depth=0)

    gamefield[myPosition[0], myPosition[1]] = 'X'
    gamefield[enemyPosition[0], enemyPosition[1]] = 'Y'

    for row in gamefield:
        for cell in row:
            if(cell == ' '):
                print(' ', end='')
            else:
                print(cell, end='')
        print("")

    print(myPlayer)
    print(enemyPlayer)

    print("Values received: north, south, east, west")
    print([north_val, south_val, east_val, west_val])


    direction = ReturnDirections.random()
    if north_val == max([north_val, south_val, east_val, west_val]):
        print("Return North")
        direction = ReturnDirections.NORTH
    elif south_val == max([north_val, south_val, east_val, west_val]):
        print("Return South")
        direction = ReturnDirections.SOUTH
    elif east_val == max([north_val, south_val, east_val, west_val]):
        print("Return East")
        direction = ReturnDirections.EAST
    elif west_val == max([north_val, south_val, east_val, west_val]):
        print("Return West")
        direction = ReturnDirections.WEST
    else:
        print("Return Random")


    return direction

application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '127.0.0.1'), port=os.getenv('PORT', '8080'))