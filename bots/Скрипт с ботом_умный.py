import random

def make_choice(x,y,field):

    x_size = len(field)
    y_size = len(field[0])

    for i in range(0, x-1):
        if field[i][y]!=0:
            return "fire_left"

    for i in range(x+1, x_size):
        if field[i][y]!=0:
            return "fire_right"

    for i in range(0, y - 1):
        if field[x][i] != 0:
            return "fire_up"

    for i in range(y + 1, y_size):
        if field[x][i] != 0:
            return "fire_down"

    return random.choice(["go_up", "go_down"])
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
import random
 
def make_choice(x,y,field):
 
    x_size = len(field)
    y_size = len(field[0])
 
    for i in range(0, x-1):
        if field[i][y]!=0:
            return "fire_left"
 
    for i in range(x+1, x_size):
        if field[i][y]!=0:
            return "fire_right"
 
    for i in range(0, y - 1):
        if field[x][i] != 0:
            return "fire_up"
 
    for i in range(y + 1, y_size):
        if field[x][i] != 0:
            return "fire_down"
 
    return random.choice(["go_up", "go_down"])
