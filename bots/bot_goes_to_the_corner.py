import random
 
def make_choice(x,y,field):
    
    # Define size of the field  
    x_size = len(field)
    y_size = len(field[0])
    
    # Bot starts moving towards the right bottom corner
    if x < x_size - 1:
        return "go_right"
    if y < y_size - 1:
        return "go_down"
    
    # Bot starts randomly shooting when he'd reached the corner
    return random.choice(["fire_up", "fire_left"])
