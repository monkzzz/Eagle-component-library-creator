import questions
import orientation
import symbol_pins_types
import symbol_wires_types

coordinates_list = list()
component = dict()
pin_list = list()
smd_pads = list()

def main():
    
    # Component and library questions function
    lib_name, component = questions.component_questions()

    # Create first text part of lbr file
    create_txt(lib_name, component)

    # Create and add Footprint data to lbr file
    smd_pads = footprint_create(lib_name, component)

    # Create and add Symbol data to lbr file
    pins = simbol_create(lib_name, component, pin_list)

    # Add device text on lbr file
    device_sets_txt(lib_name, component)

    # Connect Symbol pins to Footprint pads
    connects_txt(lib_name, smd_pads, pins)

    # Add text part to lbr file
    technologies_txt(lib_name, component)

    print("Library Created")

# ----------------- Footprint Creation Part -----------------
# Footprint creation main function
def footprint_create(lib_name, component):

    # List to store the pads
    pad = list()

    # - - - Pads - - -
    # Single
    if component['package_type'] == "single_package":
        # Bottom
        bottom_pads =  component['pins']
        orientation = -1

        # Pad X coordinates
        pads = pads_location(component, pad, bottom_pads, orientation)

        for i in range(component['pins']):
            # Create list of pads data
            smd_pads.append({'name': i+1, 'x': pads[i],
                        'y': -component['pads_distance_c_b'], 'dx': component['pads_length'], 'dy': component['pads_width'], 'layer': "1", 'rot': "R90"})

    # Dual
    elif component['package_type'] == "dual_package":

        # Left side
        left_pads =  component['quad_l_r_pins']
        orientation = 1

        # Pad Y coordinate
        pad = pads_location(component, pad, left_pads, orientation)

        # Right Side
        right_pads =  component['quad_l_r_pins']
        orientation = -1

        # Pad Y coordinate
        pad = pads_location(component, pad, right_pads, orientation)

        for i in range(component['pins']):
            # Left pad
            if i <component['quad_l_r_pins']:
                # X coordinate
                x_pos = -component['pads_distance_l_r']/2
                # Pad rotation
                rot = "R0"

            # Right pad
            else:
                # X coordinates
                x_pos = component['pads_distance_l_r']/2
                # Pad rotation
                rot = "R180"

            # Create list of pads data
            smd_pads.append({'name': i+1, 'x': x_pos,
                        'y': pad[i], 'dx': component['pads_length'], 'dy': component['pads_width'], 'layer': "1", 'rot': rot})

    # Quad package
    elif component['package_type'] == "quad_package":
        
        # Left Side
        left_pads =  component['quad_l_r_pins']
        orientation = 1

        # Pad Y coordinate
        pad = pads_location(component, pad, left_pads, orientation)

        # Bottom Side
        bottom_pads =  component['quad_t_b_pins']
        orientation = -1

        # Pad X coordinate
        pads = pads_location(component, pad, bottom_pads, orientation)

        # Right Side
        right_pads =  component['quad_l_r_pins']
        orientation = -1

        # Pad Y coordinate
        pad = pads_location(component, pad, right_pads, orientation)

        # Top Side
        top_pads =  component['quad_t_b_pins']
        orientation = 1

        # Pad X coordinate
        pad = pads_location(component, pad, top_pads, orientation)

        # Go through pads
        for i in range(component['pins']):

            # Left pad
            if i <(component['quad_l_r_pins']):
                # X coordinate
                x_pos = -component['pads_distance_l_r']/2
                # Y coordinate
                y_pos = pad[i]
                # Pad rotation
                rot = "R0"

            # Bottom pad
            elif component['quad_l_r_pins'] <= i < (component['quad_l_r_pins'] + component['quad_t_b_pins']): 
                # X coordinate
                x_pos = pad[i]
                # Y coordinate
                y_pos = -(component['pads_distance_t_b']) / 2
                # Pad rotation
                rot = "R90"

            # Check if right pin
            elif component['quad_l_r_pins']  + component['quad_t_b_pins'] <= i < ( (2 *component['quad_l_r_pins']) + component['quad_t_b_pins']): 
                # Put it on the right side
                x_pos = component['pads_distance_l_r'] / 2.
                y_pos = pad[i]
                
                # Pad rotation
                rot = "R180"

            # Check if top pin
            else:
                # Put it on the top side
                x_pos = pad[i]
                y_pos = component['pads_distance_t_b']/2
                # Pad rotation
                rot = "R270"

            # Create list of pads data
            smd_pads.append({'name': i+1, 'x': x_pos,
                        'y': y_pos, 'dx': component['pads_length'], 'dy': component['pads_width'], 'layer': "1", 'rot': rot})

    # Bottom/Center/Thermal pad
    if component['center_pad'] == 1:
        # Add data to list 
        smd_pads.append({'name': i+2, 'x': 0,
                        'y': 0, 'dx': component['center_pad_length'], 'dy': component['center_pad_width'], 'layer': "1", 'rot': "R0"})
    
    # - - - Wires - - -
    # Distance in X axis between pads edge for drawing wires
    # Single
    if component['package_type'] == "single_package":
        y_space = component['pads_distance_c_b'] - (component['pads_length']/2)
        x_space =''

    # Dual
    if component['package_type'] == "dual_package":
        x_space = component['pads_distance_l_r'] - (component['pads_length']/2)
        y_space =''

    # Quad 
    if component['package_type'] == "quad_package":
        x_space = component['pads_distance_l_r'] - (component['pads_length']/2)
        y_space = component['pads_distance_t_b'] - (component['pads_length']/2)

    # Draw the pads
    footprint_pads_txt(lib_name, component, smd_pads)

    # Draw the footprint wires
    footprint_wires_txt(lib_name, component, x_space, y_space)

    # Return the list
    return smd_pads

# Function to define x pad location
def pads_location(component, pad, side, signal):

    # If odd number of pins
    if side % 2 == 1:

        # calc the multiplier
        multi = int(side/2)

        # Go through the pins on the side
        for i in range(int(side)):

            #Calc the y position of the pin[i] 
            pad.append(signal*((multi * component['spacing']) - (i * component['spacing'])))

       # If even
    else:

        # half of the spacing
        half = component['spacing']/2

        # calc the multiplier
        multi = int(side) - 1

        # Go through the pins on the left side
        for i in range(int(side)):
            #Calc the y position of the pin[i]
            pad.append(signal*((multi * half) - (i * component['spacing'])))

    return pad  

# ----------------- Symbol Creation Part -----------------
# Symbol creation main function

def simbol_create(lib_name, component, pin_list):

    # Default value for symbol space between pins
    pin_space = 2.54

    j = 0.0
    k = 0.0

    # - - - Pins - - -
    for pin_number in range(component['pins']):

        # Ask pin info
        pin_name, pin_direction = questions.pin_questions(pin_number, pin_list)
       
        # Single
        if component['package_type'] == "single_package":
            pin_list, j = symbol_pins_types.single_package_pins(pin_name, pin_number, pin_direction, pin_space, j)
        
        # Dual
        elif component['package_type'] == "dual_package":
            pin_list, j = symbol_pins_types.dual_package_pins(component, pin_name, pin_number, pin_direction, pin_space, j)
        
        # Quad
        elif component['package_type'] == "quad_package":
            pin_list, j, k = symbol_pins_types.quad_package_pins(component, pin_name, pin_number, pin_direction, pin_space, j, k)
            

    # - - - Center Pad pin- - -
    if component['center_pad'] == 1:
        center_name, center_direction = questions.center_pad_questions(pin_list)
        
        pin_list= symbol_pins_types.central_pins(component, center_name, pin_number, center_direction, pin_space)


    # - - - Wires - - -
    # Single
    if component['package_type'] == "single_package":
        coordinates_list = symbol_wires_types.single_package_wires(component, pin_space)

    # Dual
    elif component['package_type'] == "dual_package":
        coordinates_list = symbol_wires_types.dual_package_wires(component, pin_space)

    # Quad
    elif component['package_type'] == "quad_package":
        coordinates_list = symbol_wires_types.quad_package_wires(component, pin_space)

    # Symbol wires text generation
    symbol_wires_txt(lib_name, component, coordinates_list)

    # Symbol pins text generation
    symbol_pins_txt(lib_name, pin_list)

    # Return Pin List
    return pin_list

# ----------------- Text Creation Part -----------------

# - - - Footprint - - -
# Footprint pads txt function

def footprint_pads_txt(lib_name, component, pads):
    # Orientation Type questions
    orientation_symbol, orientation_position, pin_counter = questions.orientation_questions()
    
    # Pads text list
    pads_text = list()

    for pad in pads:
        # Create the pad line of text
        pads_text.append(
            f"<smd name=\"{pad['name']}\" x=\"{pad['x']}\" y=\"{pad['y']}\" dx=\"{pad['dx']}\" dy=\"{pad['dy']}\" layer=\"{pad['layer']}\" rot=\"{pad['rot']}\"/>")

    # Calc the name text coordinates based on last pad
    # Single
    if component['package_type'] == "single_package":
        if component['center_pad'] == 1:
            text_pos_name = round(pads[-2]['y'] - 1.91, 2)
        else:
            text_pos_name = round(pads[-1]['y'] - 1.91, 2)

    # Dual and Quad
    else:
        if component['center_pad'] == 1:
            text_pos_name = -round(pads[-2]['y'] + 1.91, 2)
        else:
            text_pos_name = -round(pads[-1]['y'] + 1.91, 2)

    # Value text beneath Name
    text_pos_value = text_pos_name - 1.91

    # Create the name and value lines of text
    pads_text.append(
        f"<text x=\"0\" y=\"{text_pos_name}\" align=\"center\" size=\"1.27\" layer=\"25\" rot=\"R0\">&gt;{component['name']}</text>")
    pads_text.append(
        f"<text x=\"0\" y=\"{text_pos_value}\" align=\"center\" size=\"1.27\" layer=\"27\" rot=\"R0\">&gt;{component['value']}</text>")

    if orientation_symbol == 1:
        pads_text = orientation.line_indicator(component, pads, pads_text, orientation_position)
    elif orientation_symbol == 2:
        pads_text = orientation.dot_indicator(component, pads, pads_text, orientation_position)
    else:
        pads_text = orientation.triangle_indicator(component, pads, pads_text, orientation_position)

    if pin_counter == 1 or pin_counter == 2 or pin_counter == 3:
            pads_text = orientation.counting_indicator(component, pads, pads_text, pin_counter)
    

    # Add text to lbr file
    for line in pads_text:
        append_txt(lib_name, line)
    return True

# Footprint wire text lines
def footprint_wires_txt(lib_name, component, x_space, y_space):
    # Create list to store the text
    pkg_wire_text = list()

    # - - - Tdocument - - -

    # Position based on component size
    d_x_pos = component['width']/2
    d_y_pos = component['length']/2

    # Line width
    d_width = 0.05

    # Tdocument layer wires text
    pkg_wire_text.append(
        f"<wire x1=\"-{d_x_pos}\" y1=\"{d_y_pos}\" x2=\"{d_x_pos}\" y2=\"{d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"{d_x_pos}\" y1=\"{d_y_pos}\" x2=\"{d_x_pos}\" y2=\"{-d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"{d_x_pos}\" y1=\"-{d_y_pos}\" x2=\"-{d_x_pos}\" y2=\"{-d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"-{d_x_pos}\" y1=\"-{d_y_pos}\" x2=\"-{d_x_pos}\" y2=\"{d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")

    # Orientation

    # Single
    if component['package_type'] == "single_package":
            # Circle radius
            radius = round(d_x_pos / 15, 2)
            # Circle width
            c_width = round(d_x_pos / 15, 2)

            # Circle position
            c_x_pos = round(-d_x_pos + radius + (2 * c_width), 2)
            c_y_pos = round(-d_y_pos + radius + (2 * c_width), 2)

            # Tdocument layer circle
            pkg_wire_text.append(
                f"<circle x=\"{c_x_pos}\" y=\"{c_y_pos}\" radius=\"{radius}\" width=\"{c_width}\" layer=\"51\"/>")

    # Dual
    elif component['package_type'] == "dual_package":
        # Half-moon

        # Tdocument layer half-moon
        pkg_wire_text.append(
            f"<wire x1=\"-{d_x_pos/2}\" y1=\"{d_y_pos}\" x2=\"{d_x_pos/2}\" y2=\"{d_y_pos}\" width=\"{d_width}\" layer=\"51\" curve=\"180\"/>")
        
    # Quad
    elif component['package_type'] == "quad_package":
        # Circle radius
        radius = round(d_x_pos / 15, 2)
        # Circle Width
        c_width = round(d_x_pos / 15, 2)

        # Circle coordinates
        c_x_pos = round(-d_x_pos + radius + (2 * c_width), 2)
        c_y_pos = round(d_y_pos - radius - (2 * c_width), 2)

        # Tdocument layer circle
        pkg_wire_text.append(
            f"<circle x=\"{c_x_pos}\" y=\"{c_y_pos}\" radius=\"{radius}\" width=\"{c_width}\" layer=\"51\"/>")

    # - - - Tplace - - -

    # Tplace wires width
    p_width = 0.1
    # Based on pads sizing - a fixed ammount so it doesn't cover the pads
    # get x_pos by using between pads space and subtrating a fixed value

    if x_space and not y_space:
        p_x_pos = (x_space / 2) - (0.25 * (x_space / 2))

        # get y_pos by using the ratio of reduction of x
        p_y_pos = d_y_pos * (p_x_pos / d_x_pos)
    
    elif y_space and not x_space:
        p_y_pos = (y_space / 2) - (0.25 * (y_space / 2))

        # get x_pos by using the ratio of reduction of y
        p_x_pos = d_x_pos * (p_y_pos / d_y_pos)

    else:
        p_x_pos = (x_space / 2) - (0.25 * (x_space / 2))
        p_y_pos = (y_space / 2) - (0.25 * (y_space / 2))

    p_x_pos = round(p_x_pos, 2)
    p_y_pos = round(p_y_pos, 2)

    # Create tplace layer wires

    # If there is no thermal pad draw lines
    if component['center_pad'] == 0 :

        # Tplace layer wires text
        pkg_wire_text.append(
            f"<wire x1=\"-{p_x_pos}\" y1=\"{p_y_pos}\" x2=\"{p_x_pos}\" y2=\"{p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")
        pkg_wire_text.append(
            f"<wire x1=\"{p_x_pos}\" y1=\"{p_y_pos}\" x2=\"{p_x_pos}\" y2=\"{-p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")
        pkg_wire_text.append(
            f"<wire x1=\"{p_x_pos}\" y1=\"-{p_y_pos}\" x2=\"-{p_x_pos}\" y2=\"{-p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")
        pkg_wire_text.append(
            f"<wire x1=\"-{p_x_pos}\" y1=\"-{p_y_pos}\" x2=\"-{p_x_pos}\" y2=\"{p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")

        # Single
        if component['package_type'] == "single_package":
            # Orientation circle

            # Radius got from tplace
            radius = round(p_x_pos / 8, 2)
            # Width
            c_width = round(p_x_pos / 8, 2)

            # Circle position
            c_x_pos = round(-p_x_pos + radius + (2 * c_width), 2)
            c_y_pos = round(-p_y_pos + radius + (2 * c_width), 2)

            # Create tplace layer circle
            pkg_wire_text.append(
                f"<circle x=\"{c_x_pos}\" y=\"{c_y_pos}\" radius=\"{radius}\" width=\"{c_width}\" layer=\"21\"/>")

        # Dual
        elif component['package_type'] == "dual_package":
            # Orientation half-moon
            pkg_wire_text.append(
                f"<wire x1=\"-{p_x_pos/2}\" y1=\"{p_y_pos}\" x2=\"{p_x_pos/2}\" y2=\"{p_y_pos}\" width=\"{p_width}\" layer=\"21\" curve=\"180\"/>")
        
        # Quad
        else:
            # Orientation circle

            # Radius got from tplace
            radius = round(p_x_pos / 15, 2)
            # Width
            c_width = round(p_x_pos / 15, 2)

            # Circle position
            c_x_pos = round(-p_x_pos + radius + (2 * c_width), 2)
            c_y_pos = round(p_y_pos - radius - (2 * c_width), 2)

            # Create tplace layer circle
            pkg_wire_text.append(
                f"<circle x=\"{c_x_pos}\" y=\"{c_y_pos}\" radius=\"{radius}\" width=\"{c_width}\" layer=\"21\"/>")

    pkg_wire_text.append("</package>")
    pkg_wire_text.append("</packages>")

    # Add text to lbr file
    for line in pkg_wire_text:
        append_txt(lib_name, line)

    return True

# - - - Symbol - - -

# Symbol wire lines
def symbol_wires_txt(lib_name, component, cordinates):
    # Symbol text lines
    sy_wire_text = list()

    sy_wire_text.append("<symbols>")
    sy_wire_text.append(f"<symbol name=\"{component['name']}\">")

    # Symbol wires text
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[0]}\" y1=\"{cordinates[1]}\" x2=\"{cordinates[2]}\" y2=\"{cordinates[3]}\" width =\"0.254\" layer =\"94\"/>")
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[2]}\" y1=\"{cordinates[3]}\" x2=\"{cordinates[4]}\" y2=\"{cordinates[5]}\" width=\"0.254\" layer=\"94\"/>")
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[4]}\" y1=\"{cordinates[5]}\" x2=\"{cordinates[6]}\" y2=\"{cordinates[7]}\" width=\"0.254\" layer=\"94\"/>")
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[6]}\" y1=\"{cordinates[7]}\" x2=\"{cordinates[0]}\" y2=\"{cordinates[1]}\" width=\"0.254\" layer=\"94\"/>")

    # Symbol details text
    sy_wire_text.append(
        f"<text x=\"{cordinates[2] + 1.24}\" y=\"{cordinates[3] + 2.54}\" align=\"center-left\" size=\"1.778\" layer=\"95\">&gt;{component['name']}</text>")
    sy_wire_text.append(
        f"<text x=\"{cordinates[2] + 1.24}\" y=\"{cordinates[3] }\" align=\"center-left\" size=\"1.778\" layer=\"96\">&gt;{component['value']}</text>")

    # Add text to lbr file
    for line in sy_wire_text:
        append_txt(lib_name, line)

    return True

# Symbol pins text
def symbol_pins_txt(lib_name, pins):
    # Pins text lines
    pins_text = list()

    # Symbol pins text
    for pin in pins:
        pins_text.append(
            f"<pin name=\"{pin['name']}\" x=\"{pin['x']}\" y=\"{pin['y']}\" length=\"middle\" direction=\"{pin['direction']}\" rot=\"{pin['side']}\"/>")

    pins_text.append("</symbol>")
    pins_text.append("</symbols>")

    # Add text to lbr file
    for line in pins_text:
        append_txt(lib_name, line)

    return True

# --- Other txt ---

def device_sets_txt(lib_name, component):
    # Create the var to store the text
    device_text_lines = f"""
<devicesets>
<deviceset name="{component['name']}" prefix="IC">
<description>&lt;b&gt;{component['description']}&lt;/b&gt;&lt;p&gt;
Source: &lt;a href="{component['datasheet']}"&gt; Datasheet &lt;/a&gt;</description>
<gates>
<gate name="G$1" symbol="{component['name']}" x="0" y="0"/>
</gates>
<devices>
<device name="" package="{component['package']}">
"""
    # Add text to lbr file
    append_txt(lib_name, device_text_lines)

    return True


# Connect pin name to pad function
def connects_txt(lib_name, smd_pads, pins):
    # Connects text list
    connects_text = list()
    connects_text.append("<connects>")

    # Pin names list
    pin_names = list()
    
    for pin in pins:
        pin_names.append(pin['name'])

    i = 0
    # Connects text
    for pad in smd_pads:
        connects_text.append(
            f"<connect gate=\"G$1\" pin=\"{pin_names[i]}\" pad=\"{pad['name']}\"/>")
        i += 1

    connects_text.append("</connects>")

    # Add text to lbr file
    for line in connects_text:
        append_txt(lib_name, line)

    return True

# Technologies text function
def technologies_txt(lib_name, component):

    technologies_text_lines = f"""<technologies>"
<technology name="">
<attribute name="Manufacturer_Name" value="" constant="no"/>
<attribute name="Manufacturer_Part_Number" value="" constant="no"/>
<attribute name="Description" value="{component['description']}" constant="no"/>"
<attribute name="Height" value="" constant="no"/>"
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</drawing>
</eagle>
"""

    # Add text to lbr file
    append_txt(lib_name, technologies_text_lines)

    return True

# ----------------- Lbr Creation Part -----------------
# First part of the lbr file

def create_txt(new_file, component):

    template = f"""<?xml version="1.0" encoding="utf-8"?>
<!-- Test -->
<!DOCTYPE curve SYSTEM "eagle.dtd">
<eagle version="7.7.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="yes" active="yes"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="yes" active="yes"/>
<layer number="17" name="Pads" color="2" fill="1" visible="yes" active="yes"/>
<layer number="18" name="Vias" color="2" fill="1" visible="yes" active="yes"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="yes" active="yes"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="yes" active="yes"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="25" name="tNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="26" name="bNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="27" name="tValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="28" name="bValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="yes"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="yes"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="yes"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="yes"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="yes"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="yes"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="yes"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="yes"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="yes"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="yes"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="yes" active="yes"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="yes" active="yes"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="yes" active="yes"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="yes" active="yes"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="yes" active="yes"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="yes"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="yes"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="yes"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="yes"/>
<layer number="48" name="Document" color="7" fill="1" visible="yes" active="yes"/>
<layer number="49" name="Reference" color="7" fill="1" visible="yes" active="yes"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<library>
<description>&lt;{component['name']} {component['description']} &lt;/b&gt;&lt;p&gt;
&lt;author&gt;Automatic Creation&lt;/author&gt;</description>
<packages>
<package name="{component['package']}">
<description>&lt;b&gt;{component['package']}&lt;/b&gt;&lt;br&gt;
</description>
"""

    # Create the libr file we want to store the information
    with open(f"{new_file}.lbr", "w") as output:

        # Write the information from the template
        output.write(template + "\n")

        return True

# Add text to lbr file function
def append_txt(file_edit, text):
    with open(f"{file_edit}.lbr", "a") as output:
        output.write(text + "\n")
        return True

if __name__ == "__main__":
    main()
