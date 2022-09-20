# Wires coordinates list
coordinates_list = list()

# ----------------- Symbol Wires -----------------

# - - - Single Package Wires - - -
def single_package_wires(component, pin_space):
        
    if component['center_pad'] == "1":
        r = 2

    else:
        r = 0

    # Max X
    x = component['pins'] * pin_space
    x = round(x, 2)

    # cord 1
    coordinates_list.append(-pin_space)
    coordinates_list.append(pin_space*(6+r))

    # cord 2
    coordinates_list.append(x)
    coordinates_list.append(pin_space*(6+r))

    # cord 3
    coordinates_list.append(x)
    coordinates_list.append(pin_space*2)

    # cord 4
    coordinates_list.append(- pin_space)
    coordinates_list.append(pin_space*2)

    return coordinates_list    


# - - - Dual Package Wires - - -

def dual_package_wires(component, pin_space):

    # Check if the total number of pins are even
    if (component['pins'] % 2) == 0:
        # Max y coordinate
        y = - component['quad_l_r_pins'] * pin_space

    # Or odd
    else:
        # Max y coordinate
        y = - (component['quad_l_r_pins'] + 1) * pin_space

    y = round(y, 2)

    # Add coordinates to list
    # cord 1
    coordinates_list.append(pin_space*2)
    coordinates_list.append(pin_space)
    
    # cord 2
    coordinates_list.append(pin_space*10)
    coordinates_list.append(pin_space)
    
    # cord 3
    coordinates_list.append(pin_space*10)
    coordinates_list.append(y)

    # cord 4
    coordinates_list.append(pin_space*2)
    coordinates_list.append(y)

    return coordinates_list    


# - - - Quad Package Wires - - -

def quad_package_wires(component, pin_space):
    if component['center_pad'] == '1':
        r = 1

    else:
        r = 0

    # Max x coordinate
    x = (component['quad_t_b_pins'] + 7 + (2* r) ) * pin_space
    x = round(x, 2)

    # Max y coordinate
    y = -(component['quad_l_r_pins'] + 2 + r) * pin_space
    y = round(y, 2)

    # Add coordinates to list
    # cord 1
    coordinates_list.append(pin_space*2)
    coordinates_list.append((3 + r) * pin_space)
    
    # cord 2
    coordinates_list.append(x)
    coordinates_list.append((3 + r) * pin_space)
    
    # cord 3
    coordinates_list.append(x)
    coordinates_list.append(y)

    # cord 4
    coordinates_list.append(pin_space*2)
    coordinates_list.append(y)

    return coordinates_list