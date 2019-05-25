import random

def make_choice(x,y,field):
    x_size = len(field)
    y_size = len(field[0])
    bots = []
    crash_bots = []
    flag = True
    i = x - 1
    while i >= 0 and flag:
        if field[i][y]!=0:
            bots.append(['left', field[i][y]['life']])
            if field[i][y]['history'] != []:
                steps = len(field[i][y]['history'])
                if field[i][y]['history'][steps-1] == 'crash':
                    crash_bots.append('left')
            flag = False
        i -= 1
    flag = True
    i = x+1
    while i < x_size and flag:
        if field[i][y]!=0:
            bots.append(['right', field[i][y]['life']])
            if field[i][y]['history'] != []:
                steps = len(field[i][y]['history'])
                if field[i][y]['history'][steps-1] == 'crash':
                    crash_bots.append('right')
            flag = False
        i += 1
    flag = True
    i = y - 1
    while i >= 0 and flag:
        if field[x][i] != 0:
            bots.append(['up', field[x][i]['life']])
            if field[x][i]['history'] != []:
                steps = len(field[x][i]['history'])
                if field[x][i]['history'][steps-1] == 'crash':
                    crash_bots.append('up')
            flag = False
        i -= 1
    flag = True
    i = y+1
    while i < y_size and flag:
        if field[x][i] != 0:
            bots.append(['down', field[x][i]['life']])
            if field[x][i]['history'] != []:
                steps = len(field[x][i]['history'])
                if field[x][i]['history'][steps-1] == 'crash':
                    crash_bots.append('down')
            flag = False
        i += 1

    if len(bots) == 4:
        min_health = sorted(bots, key=lambda x: x[1])
        return 'fire_' + min_health[0][0]
    if len(bots) == 3:
        directions = set(['left', 'right', 'up', 'down'])
        bots_directions = set(bots[0][0], bots[1][0], bots[2][0])
        direction_go = str(directions - bots_directions)
        if x == 0:
            direction_go = 'right'
        elif y == 0:
            direction_go = 'down'
        elif x == x_size-1:
            direction_go = 'left'
        elif y == y_size-1:
            direction_go = 'up'
        else:
            direction_go = direction_go[2:len(direction_fire)-2]
        return 'go_' + direction_go
    if len(bots) == 2:
        two_bots_string = bots[0][0] + bots[1][0]
        if two_bots_string == 'leftright':
            if y == 0:
                return 'go_down'
            elif y == y_size-1:
                return 'go_up'
            else:
                return random.choice(['go_up', 'go_down'])
        if two_bots_string == 'updown':
            if x == 0:
                return 'go_right'
            elif x == x_size-1:
                return 'go_left'
            else:
                return random.choice(['go_left', 'go_right'])
            
        min_health = sorted(bots, key=lambda x: x[1])
        if min_health[0][0] == 'left':
            if x == 0:
                return 'go_left'
            else:
                return 'go_right'
        if min_health[0][0] == 'right':
            if x == x_size-1:
                return 'go_right'
            else:
                return 'go_left'
        if min_health[0][0] == 'up':
            if y == y_size-1:
                return 'go_up'
            else:
                return 'go_down'
        if min_health[0][0] == 'down':
            if y == 0:
                return 'go_down'
            else:
                return 'go_up'
    if len(bots) == 1:
        if field[x][y]["life"] >= 40:
            return 'fire_' + bots[0][0]
        if field[x][y]["life"] >= 20 and field[x][y]["life"] > bots[0][1]:
            return 'fire_' + bots[0][0]
        if crash_bots != []:
            return 'fire_' + crash_bots[0]
        if field[x][y]["life"] >= 20 and (bots[0][1] - field[x][y]["life"]) <= 10:
            return 'fire_' + bots[0][0]
        else:
            if bots[0][0] == 'left' or bots[0][0] == 'right':
                if y == 0:
                    return 'go_down'
                elif y == y_size-1:
                    return 'go_up'
                else:
                    return random.choice(['go_up', 'go_down'])
            else:
                if x == 0:
                    return 'go_right'
                elif x == x_size-1:
                    return 'go_left'
                else:
                    return random.choice(['go_left', 'go_right'])
    if bots == []:
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
