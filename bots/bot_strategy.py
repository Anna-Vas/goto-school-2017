import random

def make_choice(x,y,field):
    x_size = len(field)
    y_size = len(field[0])
    bots = []
    flag = True
    i = 0
    while i < x and flag:
        if field[i][y]!=0:
            bots.append(['left', field[i][y]['life']])
            flag = False
        i += 1
    flag = True
    i = x+1
    while i < x_size and flag:
        if field[i][y]!=0:
            bots.append(['right', field[i][y]['life']])
            flag = False
        i += 1
    flag = True
    i = 0
    while i < y and flag:
        if field[x][i] != 0:
            bots.append(['up', field[x][i]['life']])
            flag = False
        i += 1
    flag = True
    i = y+1
    while i < y_size and flag:
        if field[x][i] != 0:
            bots.append(['down', field[x][i]['life']])
                        flag = False
        i += 1

    if len(bots) == 4:
        min_health = sorted(bots, key=lambda x: x[1])
        return 'fire_' + min_health[0][0]
    if len(bots) == 3:
        directions = set(['left', 'right', 'up', 'down'])
        bots_directions = set(bots[0][0], bots[1][0], bots[2][0])
        direction_fire = str(directions - bots_directions)
        return 'go_' + direction_fire[2:len(direction_fire)-2]
    if len(bots) == 2:
        two_bots_string = bots[0][0] + bots[1][0]
        if two_bots_string == 'leftright':
            return random.choice(['go_up', 'go_down'])
        if two_bots_string == 'updown':
            return random.choice(['go_left', 'go_right'])
        min_health = sorted(bots, key=lambda x: x[1])
        return 'go_' + min_health[0][0]
    if len(bots) == 1:
        if bots[0][1] < field[x][y]["life"]:
            return 'fire_' + bots[0][0]
        else:
            if bots[0][0] == 'left' or bots[0][0] == 'right':
                return random.choice(['go_up', 'go_down'])
            else:
                return random.choice(['go_left', 'go_right'])
    if len(bots) == 0:
        return random.choice(['go_up', 'go_down', 'go_left', 'go_right'])
