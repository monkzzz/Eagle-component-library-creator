# Pins list
pin_list = list()

# ----------------- Symbol Pins -----------------

# - - - Single Package Pins - - -

def single_package_pins(pin_name, pin_number, pin_direction, pin_space, j):

    j = round(j, 2)

    # Add pins to list
    pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                            'direction': pin_direction, 'x': j, 'y': "0", 'side': "R90"})
    j += pin_space

    return pin_list, j


# - - - Dual Package pins - - -

def dual_package_pins(component, pin_name, pin_number, pin_direction, pin_space, j):
    # Check if pin is on the left side
    if pin_number < (component['quad_l_r_pins']):

        j = round(j, 2)

        # Add pins to list
        pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                            'direction': pin_direction, 'x': "0", 'y': j, 'side': "R0"})

        j -= pin_space

    # On the right side
    else:
        j += pin_space
        j = round(j, 2)

        # Add pins to list
        pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                            'direction': pin_direction, 'x': pin_space * 12, 'y': j, 'side': "R180"})

    return pin_list, j


# - - - Quad Package pins - - -

def quad_package_pins(component, pin_name, pin_number, pin_direction, pin_space, j, k):
    if component['center_pad'] == 1:
        r = pin_space

    else:
        r = 0

    # Left side pin
    if pin_number < component['quad_l_r_pins']:

        j = round(j, 2)

        # Add pins to list
        pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                            'direction': pin_direction, 'x': k, 'y': j, 'side': "R0"})

        j -= pin_space

    # Bottom side pin
    elif component['quad_l_r_pins'] <= pin_number < (component['quad_l_r_pins'] + component['quad_t_b_pins']):

        k += pin_space
        k = round(k, 2)

        # Add pins to list
        pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                            'direction': pin_direction, 'x': k + (4*pin_space) + r, 'y': j - (4*pin_space) - r, 'side': "R90"})

    # Right side pin
    elif (component['quad_l_r_pins'] + component['quad_t_b_pins']) <= pin_number < ((2 * component['quad_l_r_pins']) + component['quad_t_b_pins']):
        
        j += pin_space
        j = round(j, 2)

        # Add pins to list
        pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                            'direction': pin_direction, 'x': k + (9 * pin_space) + (2 * r), 'y': j, 'side': "R180"})
        
    # Top side pin
    else:
        k = round(k, 2)

        # Add pins to list
        pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                            'direction': pin_direction, 'x': k + (4 * pin_space) + r, 'y': j + (5 * pin_space) + r , 'side': "R270"})
        k -= pin_space

    return pin_list, j, k


# - - - Center Pad pin- - -

def central_pins(component, pin_name, pin_number, pin_direction, pin_space):
    if component['package_type'] == "single_package":
        x_pos = (component['quad_t_b_pins'] + 2) * pin_space
        y_pos = pin_space * 7
        rot = "R180"

    elif component['package_type'] == "dual_package":
        x_pos = pin_space * 6
        y_pos = - (component['quad_l_r_pins'] + 2) * pin_space
        rot = "R90"

    elif component['package_type'] == "quad_package":
        x_pos = (component['quad_t_b_pins'] + 8) * pin_space
        y_pos = -(component['quad_l_r_pins'] + 5) * pin_space
        rot = "R90"

    # Add pin to list
    pin_list.append({'number': pin_number+1, 'name': pin_name.upper(),
                        'direction': pin_direction, 'x': x_pos, 'y': y_pos, 'side': rot})

    return pin_list