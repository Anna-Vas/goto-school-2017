import random

def make_choice(x, y, field):

    # Define size of the field
    x_size = len(field)
    y_size = len(field[0])

    # Add all other bots situated in a direct line from current position to the list
    bots = []

    # Adding bots to the left from current position
    flag = True
    i = 0
    while i < x and flag:
        if field[i][y] != 0:
            bots.append(['left', field[i][y]['life']])
            flag = False
        i += 1

    # Adding bots to the right from current position
    flag = True
    i = x + 1
    while i < x_size and flag:
        if field[i][y] != 0:
            bots.append(['right', field[i][y]['life']])
            flag = False
        i += 1

    # Adding bots above current position
    flag = True
    i = 0
    while i < y and flag:
        if field[x][i] != 0:
            bots.append(['up', field[x][i]['life']])
            flag = False
        i += 1

    # Adding bots below current position
    flag = True
    i = y + 1
    while i < y_size and flag:
        if field[x][i] != 0:
            bots.append(['down', field[x][i]['life']])
                        flag = False
        i += 1

    # If there are four bots in a direct line, bot starts shooting to the one with the least health
    if len(bots) == 4:
        min_health = sorted(bots, key=lambda x: x[1])
        return 'fire_' + min_health[0][0]

    # If there are three bots in a direct line, bot tries to escape
    if len(bots) == 3:
        directions = set(['left', 'right', 'up', 'down'])
        bots_directions = set(bots[0][0], bots[1][0], bots[2][0])
        direction_fire = str(directions - bots_directions)
        return 'go_' + direction_fire[2:len(direction_fire)-2]
    
    # If there are two bots in a direct line, bot moves randomly to a safe direction
    if len(bots) == 2:
        two_bots_string = bots[0][0] + bots[1][0]
        if two_bots_string == 'leftright':
            return random.choice(['go_up', 'go_down'])
        if two_bots_string == 'updown':
            return random.choice(['go_left', 'go_right'])
        # It other bots occupy both vertical and horizontal direction, bot moves to the one with less health
        min_health = sorted(bots, key=lambda x: x[1])
        return 'go_' + min_health[0][0]

    # Two strategies in case there is one bot in a direct line
    if len(bots) == 1:
        # If other bot has less health, bot starts shooting
        if bots[0][1] < field[x][y]["life"]:
            return 'fire_' + bots[0][0]
        # If other bot has more health, bot starts moving in order to escape
        else:
            if bots[0][0] == 'left' or bots[0][0] == 'right':
                return random.choice(['go_up', 'go_down'])
            else:
                return random.choice(['go_left', 'go_right'])

    # If there are no bots in a direct line, bot starts randomly moving around the field
    if len(bots) == 0:
        return random.choice(['go_up', 'go_down', 'go_left', 'go_right'])
