import math

# -------------------------- #
# - - - Line indicator - - - #
# -------------------------- #

def line_indicator(component, pads, pads_text, version):
    # ----------------------------------------
    # version 1 is line under pad one
    # version 2 is line over pad one
    # ----------------------------------------

    # - - - Line under pad one - - - 
    if version == 1:
        # Single
        if component['package_type'] == "single_package":
            # Line coordinates
            x_1 = round(pads[0]['x'] + (component['spacing']/2), 2)
            y_1 = round(pads[0]['y'] + (pads[0]['dx']/2) + 0.05, 2)

            x_2 = x_1
            y_2 = round(pads[0]['y'] - (pads[0]['dx']/2) - 0.05, 2)

        # Dual and Quad
        else:
            # Line coordinates
            x_1 = round(pads[0]['x'] - (pads[0]['dx']/2) - 0.05, 2)
            y_1 = round(pads[0]['y'] - (component['spacing']/2), 2)

            x_2 = round(pads[0]['x'] + (pads[0]['dx']/2) + 0.05, 2)
            y_2 = y_1

    # - - - Line over pad one - - - 
    else:
        # Single
        if component['package_type'] == "single_package":
            # Line coordinates
            x_1 = round(pads[0]['x'] - (component['spacing']/2), 2)
            y_1 = round(pads[0]['y'] + (pads[0]['dx']/2) + 0.05, 2)

            x_2 = x_1
            y_2 = round(pads[0]['y'] - (pads[0]['dx']/2) - 0.05, 2)

        # Dual and Quad
        else:
            # Line coordinates
            x_1 = round(pads[0]['x'] - (pads[0]['dx']/2) - 0.05, 2)
            y_1 = round(pads[0]['y'] + (component['spacing']/2), 2)

            x_2 = round(pads[0]['x'] + (pads[0]['dx']/2) + 0.05, 2)
            y_2 = y_1

    # Create orientation line
    pads_text.append(
        f"<wire x1=\"{x_1}\" y1=\"{y_1}\" x2=\"{x_2}\" y2=\"{y_2}\" width=\"0.10\" layer=\"21\"/>")

    return pads_text

# ------------------------- #
# - - - Dot Indicator - - - #
# ------------------------- #

def dot_indicator(component, pads, pads_text, version):
    # ----------------------------------------
    # version 1 is dot next to pad one
    # version 2 is dot over pad one
    # version 3 is dot on top corner if quad package else is over pad one
    # ----------------------------------------

    # Size based on pin width
    radius = round(pads[0]['dy'], 2)
    width = round(pads[0]['dy'])

    # - - - Dot next to pad one - - - 
    if version == 1:
        # Single
        if component['package_type'] == "single_package":
            # Dot coordinates
            x_pos = round(pads[0]['x'], 2)
            y_pos = round(
                (pads[0]['y'] - (pads[0]['dx']/2) - radius - 0.05), 2)

        # Dual and Quad
        else:
            # Dot coordinates
            x_pos = round(
                (pads[0]['x'] - (pads[0]['dx']/2) - radius - 0.05), 2)
            y_pos = round(pads[0]['y'], 2)

    # - - - Dot over the pad one - - - 
    elif version == 2:
        # Single
        if component['package_type'] == "single_package":
            # Dot coordinates
            x_pos = round((pads[0]['x'] - pads[0]['dy'] - radius), 2)
            y_pos = round(pads[0]['y'], 2)

        # Dual and Quad
        else:
           # Dot coordinates
            x_pos = round(pads[0]['x'], 2)
            y_pos = round((pads[0]['y'] + pads[0]['dy'] + radius), 2)

    # - - - Dot on top corner if quad else is over pad one - - - 
    else:
        # Quad
        if component['package_type'] == "quad_package":
            # Dot coordinates
            x_pos = round((pads[0]['x']), 2)
            y_pos = round((pads[-1]['y']), 2)

        # Single
        elif component['package_type'] == "single_package":
            # Dot coordinates
            x_pos = round((pads[0]['x'] - pads[0]['dy'] - radius), 2)
            y_pos = round(pads[0]['y'], 2)

        # Dual
        else:
            # Dot coordinates
            x_pos = round(pads[0]['x'], 2)
            y_pos = round((pads[0]['y'] + pads[0]['dy'] + radius), 2)

    # Create orientation dot
    pads_text.append(
        f"<circle x=\"{x_pos}\" y=\"{y_pos}\" radius=\"{radius}\" width=\"{width}\" layer=\"21\"/>")

    return pads_text

# ------------------------------ #
# - - - Triangle indicator - - - #
# ------------------------------ #

def triangle_indicator(component, pads, pads_text, version):
    # ----------------------------------------
    # version 1 is triangle next to pad one
    # version 2 is triangle over pad one
    # version 3 is triangle on top corner if quad package else is over pad one
    # ----------------------------------------

    # - - - Triangle next to pad one - - - 
    if version == 1:

        # Single
        if component['package_type'] == "single_package":
            # Triangle coordinates
            x_1 = (pads[0]['x'] - (pads[0]['dy']))
            y_1 = - (pads[0]['dx']/2) - 0.254 + (pads[0]['y'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))

            x_2 = (pads[0]['x'])
            y_2 = - (pads[0]['dx']/2) - 0.254 + (pads[0]['y'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))

            x_3 = (pads[0]['x'] + (pads[0]['dy']))
            y_3 = - (pads[0]['dx']/2) - 0.254 + (pads[0]['y'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))

        # Dual and Quad
        else:
            # Triangle coordinates
            x_1 = - (pads[0]['dx']/2) - 0.254 + (pads[0]['x'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_1 = (pads[0]['y'] - (pads[0]['dy']))

            x_2 = - (pads[0]['dx']/2) - 0.254 + (pads[0]['x'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_2 = (pads[0]['y'])

            x_3 = - (pads[0]['dx']/2) - 0.254 + (pads[0]['x'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_3 = (pads[0]['y'] + (pads[0]['dy']))

    # - - - Triangle over pad one - - - 
    if version == 2:

        # Single
        if component['package_type'] == "single_package":
            # Triange coordinates
            x_1 = - pads[0]['dy'] - 0.254 + (pads[0]['x'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_1 = (pads[0]['y'] - (pads[0]['dy']))

            x_2 = - pads[0]['dy'] - 0.254 + (pads[0]['x'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_2 = (pads[0]['y'])

            x_3 = - pads[0]['dy'] - 0.254 + (pads[0]['x'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_3 = (pads[0]['y'] + (pads[0]['dy']))

        # Dual and Quad
        else:
            # Triangle coordinates
            x_1 = (pads[0]['x'] - (pads[0]['dy']))
            y_1 = pads[0]['dy'] + 0.254 + (pads[0]['y'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))

            x_2 = (pads[0]['x'])
            y_2 = pads[0]['dy'] + 0.254 + (pads[0]['y'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))

            x_3 = (pads[0]['x'] + (pads[0]['dy']))
            y_3 = pads[0]['dy'] + 0.254 + (pads[0]['y'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))

    # - - - Triangle on top corner if quad-package else is over pad one - - - 
    if version == 3:

        # Quad
        if component['package_type'] == "quad_package":
            # Change last pad based on having or not a Bottom/Center/Thermal pad
            if component['center_pad'] == '1':
                last_pad = pads[-2]['y']
            else:
                last_pad = pads[-1]['y']

            # Ccoordinates for normal orientation
            x_1 = (- ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_1 = (- (pads[0]['dy']))

            x_2 = (+ ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_2 = (0)

            x_3 = (- ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_3 = ((pads[0]['dy']))

            # Apply rotation formula
            x_1_r = (x_1 * math.cos(-45)) - (y_1 * math.sin(-45))
            y_1_r = (x_1 * math.sin(-45)) + (y_1 * math.cos(-45))

            x_2_r = (x_2 * math.cos(-45)) - (y_2 * math.sin(-45))
            y_2_r = (x_2 * math.sin(-45)) + (y_2 * math.cos(-45))

            x_3_r = (x_3 * math.cos(-45)) - (y_3 * math.sin(-45))
            y_3_r = (x_3 * math.sin(-45)) + (y_3 * math.cos(-45))

            # Triange over pad coordinates
            x_1 = x_1_r + pads[0]['x']
            y_1 = y_1_r + last_pad

            x_2 = x_2_r + pads[0]['x']
            y_2 = y_2_r + last_pad

            x_3 = x_3_r + pads[0]['x']
            y_3 = y_3_r + last_pad

        # Single
        elif component['package_type'] == "single_package":
            # Triange coordinates
            x_1 = - pads[0]['dy'] - 0.254 + (pads[0]['x'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_1 = (pads[0]['y'] - (pads[0]['dy']))

            x_2 = - pads[0]['dy'] - 0.254 + (pads[0]['x'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_2 = (pads[0]['y'])

            x_3 = - pads[0]['dy'] - 0.254 + (pads[0]['x'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))
            y_3 = (pads[0]['y'] + (pads[0]['dy']))

        # Dual
        else:
            # Triangle coordinates
            x_1 = (pads[0]['x'] - (pads[0]['dy']))
            y_1 = pads[0]['dy'] + 0.254 + (pads[0]['y'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))

            x_2 = (pads[0]['x'])
            y_2 = pads[0]['dy'] + 0.254 + (pads[0]['y'] - ((pads[0]['dy'] * 3**(1.0/2)) / 2))

            x_3 = (pads[0]['x'] + (pads[0]['dy']))
            y_3 = pads[0]['dy'] + 0.254 + (pads[0]['y'] + ((pads[0]['dy'] * 3**(1.0/2)) / 2))

    # Create orientation triangle
    pads_text.append(
        "<polygon width=\"0.0635\" layer=\"21\" spacing=\"0.254\">")
    pads_text.append(f"<vertex x=\"{x_1}\" y=\"{y_1}\"/>")
    pads_text.append(f"<vertex x=\"{x_2}\" y=\"{y_2}\"/>")
    pads_text.append(f"<vertex x=\"{x_3}\" y=\"{y_3}\"/>")
    pads_text.append("</polygon>")

    return pads_text

# ----------------------- #
# - - - Pin counter - - - #
# ----------------------- #

def counting_indicator(component, pads, pads_text, version):
    # ----------------------------------------
    # version 1 is dots and lines
    # version 2 is dots and lines and pin numbers
    # version 3 is dots and lines and edge numbers
    # ----------------------------------------

    # Dot and line sizes based on pin width
    radius = round(pads[0]['dy'], 2)
    c_width = round(pads[0]['dy'])

    # - - - Dots and lines - - - 
    for pad in pads:

        # Make sure its not a Bottom/Center/Thermal pad
        if component['center_pad'] == "0" or (component['center_pad'] == "1" and pad != pads[-1]):

            # Mark dot if pin mutiple of 5
            if pad["name"] % 5 == 0 and pad["name"] % 10 != 0:

                if pad["rot"] == "R0":
                    # Dot coordinates
                    c_x_pos = round((pad['x'] - (pad['dx']/2) - radius - 0.05), 2)
                    c_y_pos = round(pad['y'], 2)

                elif pad["rot"] == "R90":
                    # Dot coordinates
                    c_x_pos = round(pad['x'], 2)
                    c_y_pos = round((pad['y'] - (pad['dx']/2) - radius - 0.05), 2)

                elif pad["rot"] == "R180":
                    # Dot coordinates
                    c_x_pos = round((pad['x'] + (pad['dx']/2) + radius + 0.05), 2)
                    c_y_pos = round(pad['y'], 2)

                elif pad["rot"] == "R270":
                    # Dot coordinates
                    c_x_pos = round(pad['x'], 2)
                    c_y_pos = round((pad['y'] + (pad['dx']/2) + radius + 0.05), 2)

                # Create dot counter
                pads_text.append(
                    f"<circle x=\"{c_x_pos}\" y=\"{c_y_pos}\" radius=\"{radius/2}\" width=\"{c_width}\" layer=\"21\"/>")

            # Mark line if pin mutiple of 10
            if pad["name"] % 10 == 0:

                if pad["rot"] == "R0":
                    # Line coordinates
                    l_x_1 = round(pad['x'] - (pad['dx']/2) - (2*radius), 2)
                    l_y_1 = round(pad['y'], 2)

                    l_x_2 = round(pad['x'] - (pad['dx']/2) - 0.10, 2)
                    l_y_2 = l_y_1

                    # Text coordinates
                    y_text = l_y_1
                    x_text = l_x_1 - 0.254
                    rot = "SR270"

                elif pad["rot"] == "R90":
                    # Line coordinates
                    l_x_1 = pad['x']
                    l_y_1 = round(pad['y'] - (pad['dx']/2) - 0.10, 2)
                    l_x_2 = l_x_1
                    l_y_2 = round(pad['y'] - (pad['dx']/2) - (2*radius), 2)

                    # Text coordinates
                    x_text = l_x_1
                    y_text = l_y_2 - 0.254
                    rot = "R0"

                elif pad["rot"] == "R180":
                    # Line coordinates
                    l_x_1 = round(pad['x'] + (pad['dx']/2) + (2*radius), 2)
                    l_x_2 = round(pad['x'] + (pad['dx']/2) + 0.10, 2)
                    l_y_1 = round(pad['y'], 2)
                    l_y_2 = l_y_1

                    # Text coordinates
                    y_text = l_y_1
                    x_text = l_x_1 + 0.254
                    rot = "R90"

                elif pad["rot"] == "R270":
                    # Line coordinates
                    l_x_1 = pad['x']
                    l_x_2 = l_x_1
                    l_y_1 = round(pad['y'] + (pad['dx']/2) + 0.10, 2)
                    l_y_2 = round(pad['y'] + (pad['dx']/2) + (2*radius), 2)

                    # Text coordinates
                    x_text = l_x_1
                    y_text = l_y_2 + 0.254
                    rot = "SR180"

                # - - - Pin numbers - - - 

                # Only add pin number text in multiples of 10 if version 2
                if version == 2:
                    # Create number Text
                    pads_text.append(
                        f"<text x=\"{x_text}\" y=\"{y_text}\" align=\"center\" size=\"0.38\" layer=\"25\" rot=\"{rot}\">{pad['name']}</text>")

                # Create line counter
                pads_text.append(
                    f"<wire x1=\"{l_x_1}\" y1=\"{l_y_1}\" x2=\"{l_x_2}\" y2=\"{l_y_2}\" width=\"0.127\" layer=\"21\"/>")

            # - - - Text on edges - - - 
            if version == 3:

                # Distance if number has 3 digits
                if int(pad['name']) >= 99:
                    r = 0.55
                # Distance if number has less digits
                else:
                    r = 0.38

                # Single
                if component['package_type'] == "single_package":
                    # Corner pads
                    left_corners = [1]
                    right_corners = [component['pins']]

                # Dual
                elif component['package_type'] == "dual_package":
                    # Corner pads
                    left_corners = [1, component['quad_l_r_pins'] + 1]
                    right_corners = [
                        component['quad_l_r_pins'], component['pins']]

                # Quad
                elif component['package_type'] == "quad_package":
                    # Corner pads
                    left_corners = [1, component['quad_l_r_pins'] + 1, component['quad_l_r_pins'] +
                                    component['quad_t_b_pins']+1, (2 * component['quad_l_r_pins'])+component['quad_t_b_pins']+1]

                    right_corners = [component['quad_l_r_pins'],  component['quad_l_r_pins'] + component['quad_t_b_pins'],
                                     (2 * component['quad_l_r_pins'])+component['quad_t_b_pins'], (2 * component['quad_l_r_pins'])+(2*component['quad_t_b_pins'])]

                # Edge pins
                if pad['name'] in left_corners or pad['name'] in right_corners:

                    # Right edge
                    if pad['name'] in right_corners:
                        # Invert location
                        r = -r

                    if pad["rot"] == "R0":
                        # Text coordinates
                        x_text = round((pad['x'] - (pad['dx']/2) - radius - 0.05), 2)
                        y_text = round(pad['y'] + r, 2)

                        # Text rotation
                        rot = "SR270"

                    elif pad["rot"] == "R90":
                        # Text coordinates
                        x_text = round(pad['x'] - r, 2)
                        y_text = round((pad['y'] - (pad['dx']/2) - radius - 0.05), 2)

                        # Text rotation
                        rot = "R0"

                    elif pad["rot"] == "R180":
                        # Text coordinates
                        x_text = round((pad['x'] + (pad['dx']/2) + radius + 0.05), 2)
                        y_text = round(pad['y'] - r, 2)

                        # Text rotation
                        rot = "R90"

                    elif pad["rot"] == "R270":
                        # Text coordinates
                        x_text = round(pad['x'] + r, 2)
                        y_text = round((pad['y'] + (pad['dx']/2) + radius + 0.05), 2)

                        # Text rotation
                        rot = "SR180"

                    # Create number text
                    pads_text.append(
                        f"<text x=\"{x_text}\" y=\"{y_text}\" align=\"center\" size=\"0.38\" layer=\"25\" rot=\"{rot}\">{pad['name']}</text>")

    return pads_text
