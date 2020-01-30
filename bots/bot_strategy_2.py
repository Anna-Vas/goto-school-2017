import random

def make_choice(x,y,field):

    # Define size of field
    x_size = len(field)
    y_size = len(field[0])

    # Create a list for all the bots in a direct line from current position
    bots = []

    # If there's a bot to the left of current position, add it to the list
    flag = True
    i = x - 1
    while i >= 0 and flag:
        if field[i][y]!=0:
            bots.append(['left', field[i][y]['life']])
            flag = False
        i -= 1

    # If there's a bot to the right of current position, add it to the list
    flag = True
    i = x+1
    while i < x_size and flag:
        if field[i][y]!=0:
            bots.append(['right', field[i][y]['life']])
            flag = False
        i += 1

    # If there's a bot above current position, add it to the list
    flag = True
    i = y - 1
    while i >= 0 and flag:
        if field[x][i] != 0:
            bots.append(['up', field[x][i]['life']])
            flag = False
        i -= 1

    # If there's a bot below current position, add it to the list
    flag = True
    i = y+1
    while i < y_size and flag:
        if field[x][i] != 0:
            bots.append(['down', field[x][i]['life']])
            flag = False
        i += 1

    # If bot is surrounded by four other bots, it chooses the one with the least health and shoots to it
    if len(bots) == 4:
        min_health = sorted(bots, key=lambda x: x[1])
        return 'fire_' + min_health[0][0]
    # If there are three other bots in a direct line, bot tries to escape
    if len(bots) == 3:
        # Create set of all possible directions
        directions = set(['left', 'right', 'up', 'down'])
        # Collect all directions where are other bots
        bots_directions = set(bots[0][0], bots[1][0], bots[2][0])
        # Define direction where is no other bot
        direction_go = str(directions - bots_directions)
        # If bot is near a border, it moves to the opposite direction
        if x == 0:
            direction_go = 'right'
        elif y == 0:
            direction_go = 'down'
        elif x == x_size-1:
            direction_go = 'left'
        elif y == y_size-1:
            direction_go = 'up'
        # If bot isn't near a border, it moves to chosen direction
        else:
            direction_go = direction_go[2:len(direction_fire)-2]
        return 'go_' + direction_go

    # If there are two other bots in a direct line, bot tries to escape
    if len(bots) == 2:
        # Define where are other bots
        two_bots_string = bots[0][0] + bots[1][0]
        # If one bot is to the right and other is to the left, bot moves up or down
        if two_bots_string == 'leftright':
            # If bot is near top boder of the field, it moves down
            if y == 0:
                return 'go_down'
            # If bot is near bottom border of the field, it moves up
            elif y == y_size-1:
                return 'go_up'
            # If both directions are available, bot moves randomly up or down
            else:
                return random.choice(['go_up', 'go_down'])
        # If one bot is above and other is below, bot moves left or right
        if two_bots_string == 'updown':
            # If bot is near left border of the field, it moves right
            if x == 0:
                return 'go_right'
            # If bot is near right border of the field, it moves left
            elif x == x_size-1:
                return 'go_left'
            # If both directions are available, bot moves randomly left ot right
            else:
                return random.choice(['go_left', 'go_right'])
        # If other bots block both vertical and horizontal directions, bot escapes from the one with more health
        min_health = sorted(bots, key=lambda x: x[1])
        if min_health[0][0] == 'left':
            return 'go_right'
        if min_health[0][0] == 'right':
            return 'go_left'
        if min_health[0][0] == 'up':
            return 'go_down'
        if min_health[0][0] == 'down':
            return 'up'

    # If there is one bot in a direct line, bot tries to escape or to kill other bot depending on its health
    if len(bots) == 1:
        # If bot has more than 40 hp, it shoots to other bot anyway
        if field[x][y]["life"] >= 40:
            return 'fire_' + bots[0][0]
        # If bot has more hp than other bot, it starts shooting
        if field[x][y]["life"] > bots[0][1]:
            return 'fire_' + bots[0][0]
        # If bot has more than 20 hp and other bot hass less than 10 hp, bot starts shooting
        if field[x][y]["life"] >= 20 and (bots[0][1] - field[x][y]["life"]) <= 10:
                return 'fire_' + bots[0][0]
        # If bot has less than 10 hp or less hp than other bot, it tries to escape
        else:
            # If other bot is to the left or to the right, bot moves up or down
            if bots[0][0] == 'left' or bots[0][0] == 'right':
                if y == 0:
                    return 'go_down'
                elif y == y_size-1:
                    return 'go_up'
                else:
                    return random.choice(['go_up', 'go_down'])
            # If other bot is above or below, bot moves left or right
            else:
                if x == 0:
                    return 'go_right'
                elif x == x_size-1:
                    return 'go_left'
                else:
                    return random.choice(['go_left', 'go_right'])

    # If there are no bots in a direct line, bot starts randomly moving
    if len(bots) == 0:
        if x == 0:
            return 'go_right'
        elif y == 0:
            return 'go_down'
        elif x == x_size-1:
            return 'go_left'
        elif y == y_size-1:
            return 'go_up'
        else:
            return random.choice(['go_up', 'go_down', 'go_left', 'go_right'])
