component = dict()
pin_list = list()
smd_pads = list()

def main():

    # Ask all questions for storing component data
    lib_name, component = component_questions_set()

    # Create first text part of lbr file
    create_txt(lib_name, component)

    # Create and store package data text part on lbr file
    smd_pads = package_create(lib_name, component)
    pins = simbol_create(lib_name, component)

    # Create and store device text part on lbr file
    device_sets_txt(lib_name, component)

    # Create and store conects text part on lbr file
    connects_txt(lib_name, smd_pads, pins)

    # Create and store conects text part on lbr file
    technologies_txt(lib_name, component)

    print("Library Created")


# Questions for Library and Component data
def component_questions_set():

    # Default values
    lib_name = ''
    component['name'] = ''
    component['package'] = ''
    component['datasheet'] = ''
    component['pins'] = ''

    # Library name
    while not lib_name:
        print("")
        print("What is the name of the library? (required)")
        lib_name = input().strip().replace(" ", "_")

    # Name
    while not component['name']:
        print("")
        print("What is the name of the component? (required)")
        component['name'] = input().strip().replace(" ", "_").upper()

    # Value
    print("")
    print("What is the value of the component? (optional)")
    component['value'] = input().strip().replace(" ", "_").upper()
    if not component['value']:
        component['value'] = "default_value"

    # Description
    print("")
    print("What is the description? (optional)")
    component['description'] = input().strip()
    if not component['description']:
        component['description'] = "default_description"

    # Datasheet
    print("")
    print("What is the link to the datasheet? (optional)")
    component['datasheet'] = input().strip()

    # Package
    while not component['package']:
        print("")
        print("What is the package? (required)")
        component['package'] = input().strip().replace(" ", "_").upper()

    # Total number of pins
    while not component['pins']:
        try:
            print("")
            print("How many pins does it have? (required)")
            component['pins'] = int(input())
            if component['pins'] % 2 != 0:
                print("Not a pair number")
                component['pins'] = ''

        except ValueError:
            print("Not a number")

# Questions for Component Sizing

    # Default values
    component['length'] = ''
    component['width'] = ''
    component['spacing'] = ''
    component['pads_length'] = ''
    component['pads_width'] = ''
    component['pads_distance'] = ''

    print("              ")
    print("   ---------  ")
    print(" --|O      |--")
    print("   |       |  ")
    print(" --|      L|--")
    print("   |       |  ")
    print(" --|       |--")
    print("   ---------  ")
    print("       w      ")

    # Ask lenght
    while not component['length']:
        try:
            print("")
            print("What is the lenght(L)? (mm) (required) ")
            component['length'] = float(input())

        except ValueError:
            print("Not a number")

    # Ask width
    while not component['width']:
        try:
            print("")
            print("What is the width(W)? (mm) (required)")
            component['width'] = float(input())

        except ValueError:
            print("Not a number")

    print("                 ")
    print("   ---------     ")
    print(" --|O      |--   ")
    print("   |       | ^   ")
    print("   |       | | S ")
    print("   |       | v   ")
    print(" --|       |--   ")

    # Ask spacing value
    while not component['spacing']:
        try:
            print("")
            print("How much is the spacing(S) between pins? (mm) (required)")
            component['spacing'] = float(input())

        except ValueError:
            print("Not a number")

    # Size of pads
    print("         L       ")
    print("  -------------- ")
    print("  |        ____|_")
    print("  | W     |______")
    print("  |            | ")
    print("  -------------- ")

    # Ask pad length
    while not component['pads_length']:
        try:
            print("")
            print("How much is the length of the pad? (mm) (required)")
            component['pads_length'] = float(input())

        except ValueError:
            print("Not a number")

    # Ask pad width
    while not component['pads_width']:
        try:
            print("")
            print("How much is the width of the pad? (mm) (required)")
            component['pads_width'] = float(input())

        except ValueError:
            print("Not a number")

    print("                   ")
    print("   < - - P - - >   ")
    print("     ---------     ")
    print(" [-]-|O      |-[-] ")
    print("     |       |     ")
    print(" [-]-|       |-[-] ")
    print("     |       |     ")

    # Ask distance between Pads
    while not component['pads_distance']:
        try:
            print("")
            print("How much is the distance(P) between the pads center? (mm) (required)")
            component['pads_distance'] = float(input())

        except ValueError:
            print("Not a number")

    return lib_name, component

# ----------------- Questions Part -----------------
# Questions for pin data


def pin_questions_set(pin_number, pin_list):
    # Default values
    pin_name = ''
    pin_direction = ''

    # Create direction list
    direction_list = ["nc", "in", "out", "io",
                      "oc", "pwr", "pas", "hiz", "sup"]

    # Ask Pin Name
    while not pin_name:
        print("")
        print(f"What is the name of pin{pin_number + 1} ? (required)")
        pin_name = input().strip().replace(" ", "_")

        # Check if Pin name is unique
        if not any(p['name'] == pin_name for p in pin_list):
            continue
        else:
            print("")
            print("Pin name already used")
            pin_name = ''

    # Ask Pin Direction
    while (pin_direction not in direction_list):

        print("")
        print(f"What is the direction of pin{pin_number + 1} ? (required)")
        print("Directions: nc, in, out, io, oc, pwr, pas, hiz, sup")
        pin_direction = input().lower().strip()

    return pin_name, pin_direction


# ----------------- Package Creation Part -----------------
# Package creation main function


def package_create(lib_name, component):
    # if total pins divided by 2 gives a decimal (odd number)
    # center the midle pin of the package
    # if not
    # divide spacing

    # Distance between inside x pads edge
    x_space = component['pads_distance'] - (component['pads_length']/2)

    # Run function of distribution based on package
    y_distribution_list = pads_y_location(component)

    # Create smd pads data
    for i in range(component['pins']):
        # Check if pin is on the first half
        if i <(int(component['pins'])/2):
            # Put it on the left side of package
            x_pos = -component['pads_distance']/2

        else:
            # Put it on the right side of package
            x_pos = component['pads_distance']/2

        # Create list of pads data
        smd_pads.append({'name': i+1, 'x': x_pos,
                        'y': y_distribution_list[i], 'dx': component['pads_length'], 'dy': component['pads_width'], 'layer': "1", 'rot': "R0"})

    # Draw the pads
    package_pads_txt(lib_name, component, smd_pads)

    # Draw the package wires
    package_wires_txt(lib_name, component, x_space)

    # Return the list
    return smd_pads


# Function to define y pad location
def pads_y_location(component):

    # Get how many pins are in side
    side = component['pins']/2

    # Create a Pad list to store pads positions
    pad = list()

    # Fill the pad list with empty data
    for i in range(component['pins']):
        pad.append("")

    # If odd number of pins
    if side % 2 == 1:

        # calc the multiplier
        multi = int(side/2)

        # Go through the pins on the left side
        for i in range(int(side)):

            #Calc the y position of the left pin[i]
            pad[i] = (multi * component['spacing']) - \
                (i * component['spacing'])

        # Go through the pins on the right side
        for i in range(int(side)):

            # Calc the y position of the right pin[i]
            pad[i+int(side)] = -(multi * component['spacing']) + \
                (i * component['spacing'])

    # If even
    else:

        # Get half of the spacing
        half = component['spacing']/2

        # calc the multiplier
        multi = int(side) - 1

        # Go through the pins on the left side
        for i in range(int(side)):

            # Calc the y position of the left pin[i]
            pad[i] = (multi * half) - (i * component['spacing'])

        # Go through the pins on the right side
        for i in range(int(side)):

            # Calc the y position of the right pin[i]
            pad[i+int(side)] = -(multi * half) + (i * component['spacing'])

    return pad

# ----------------- Symbol Creation Part -----------------
# Symbol creation main function


def simbol_create(lib_name, component):

    #pins = component['pins']

    # Create list to store the coordinates of the wires
    coordinates_list = list()

    # Default value for space between pins
    pin_space = 2.54

    j = 0.0

    # Itirate through pins
    for pin_number in range(component['pins']):

        # Ask name of pins
        pin_name, pin_direction = pin_questions_set(pin_number, pin_list)

        # Divide pin number by 2
        # Then arrange half on the left and half on the right of the square

        # Check if pin is on the left side
        if pin_number < (component['pins'] / 2):

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
                            'direction': pin_direction, 'x': pin_space * 11, 'y': j, 'side': "R180"})

    # Check if the total number of pins are even
    if (component['pins'] % 2) == 0:
        # Calc the max y coordinate
        y = - ((component['pins'])/2) * pin_space

    # Or odd
    else:
        # Calc the max y coordinate
        y = - ((component['pins'] + 1)/2) * pin_space

    # Round value
    y = round(y, 2)

    # Add coordinates to list
    coordinates_list.append(pin_space*2)
    coordinates_list.append(pin_space)
    coordinates_list.append(pin_space*9)
    coordinates_list.append(pin_space)
    coordinates_list.append(pin_space*9)
    coordinates_list.append(y)
    coordinates_list.append(pin_space*2)
    coordinates_list.append(y)

    # Symbol wires text generation
    symbol_wires_txt(lib_name, component, coordinates_list)

    # Symbol pins text generation
    symbol_pins_txt(lib_name, pin_list)

    # Return Pin List
    return pin_list

# ----------------- Text Creation Part -----------------

# --- Package ---
# Package pads txt function


def package_pads_txt(lib_name, component, pads):
    # Create list to store the text
    pads_text = list()

    # Go through all the pads
    for pad in pads:
        # Create the pad line of text
        pads_text.append(
            f"<smd name=\"{pad['name']}\" x=\"{pad['x']}\" y=\"{pad['y']}\" dx=\"{pad['dx']}\" dy=\"{pad['dy']}\" layer=\"{pad['layer']}\" rot=\"{pad['rot']}\"/>")

        # Get position of last pad to use in text position
        text_pos = -round(pad['y'] + 1.50, 2)

        # Create the name and value lines of text
    pads_text.append(
        f"<text x=\"0\" y=\"{text_pos}\" align=\"center\" size=\"1.27\" layer=\"25\" rot=\"R0\">&gt;{component['name']}</text>")
    pads_text.append(
        f"<text x=\"0\" y=\"{text_pos - 1.50}\" align=\"center\" size=\"1.27\" layer=\"27\" rot=\"R0\">&gt;{component['value']}</text>")

    # Append lines of text to lbr file
    for line in pads_text:
        append_txt(lib_name, line)
    return True

# Package wire lines

def package_wires_txt(lib_name, component, x_space):
    # Create list to store the text
    pkg_wire_text = list()

    # tdocument

    # Get first position based component size
    d_x_pos = component['width']/2
    d_y_pos = component['length']/2

    # Width of the line 0.05
    d_width = 0.05

    # Create tdocument layer wires text
    pkg_wire_text.append(
        f"<wire x1=\"-{d_x_pos}\" y1=\"{d_y_pos}\" x2=\"{d_x_pos}\" y2=\"{d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"{d_x_pos}\" y1=\"{d_y_pos}\" x2=\"{d_x_pos}\" y2=\"{-d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"{d_x_pos}\" y1=\"-{d_y_pos}\" x2=\"-{d_x_pos}\" y2=\"{-d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"-{d_x_pos}\" y1=\"-{d_y_pos}\" x2=\"-{d_x_pos}\" y2=\"{d_y_pos}\" width=\"{d_width}\" layer=\"51\"/>")

    # tplace

    # Width of the line 0.1
    p_width = 0.1
    # Based on pads sizing - a fixed ammount so it doesn't cover the pads
    # get x_pos by using between pads space and subtrating a fixed value

    p_x_pos = (x_space / 2) - (0.25 * (x_space / 2))

    # get y_pos by using the ratio of reduction of x
    p_y_pos = d_y_pos * (p_x_pos / d_x_pos)

    p_x_pos = round(p_x_pos, 2)
    p_y_pos = round(p_y_pos, 2)

    # Create tplace layer wires
    pkg_wire_text.append(
        f"<wire x1=\"-{p_x_pos}\" y1=\"{p_y_pos}\" x2=\"{p_x_pos}\" y2=\"{p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"{p_x_pos}\" y1=\"{p_y_pos}\" x2=\"{p_x_pos}\" y2=\"{-p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"{p_x_pos}\" y1=\"-{p_y_pos}\" x2=\"-{p_x_pos}\" y2=\"{-p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")
    pkg_wire_text.append(
        f"<wire x1=\"-{p_x_pos}\" y1=\"-{p_y_pos}\" x2=\"-{p_x_pos}\" y2=\"{p_y_pos}\" width=\"{p_width}\" layer=\"21\"/>")

    # create orientation circle or line

    # Radius got from tplace
    radius = round(p_x_pos / 4, 2)
    # Width
    c_width = 0.127

    # Circle position
    c_x_pos = round(-p_x_pos + radius + (2 * c_width), 2)
    c_y_pos = round(p_y_pos - radius - (2 * c_width), 2)

    # Create tplace layer circle
    pkg_wire_text.append(
        f"<circle x=\"{c_x_pos}\" y=\"{c_y_pos}\" radius=\"{radius}\" width=\"{c_width}\" layer=\"21\"/>")

    pkg_wire_text.append("</package>")
    pkg_wire_text.append("</packages>")

    # Append lines of text to lbr file
    for line in pkg_wire_text:
        append_txt(lib_name, line)

    return True

# --- Symbol ---

# Symbol wire lines


def symbol_wires_txt(lib_name, component, cordinates):
    # Create list to store the text
    sy_wire_text = list()

    sy_wire_text.append("<symbols>")
    sy_wire_text.append(f"<symbol name=\"{component['name']}\">")

    # Create symbol wires text
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[0]}\" y1=\"{cordinates[1]}\" x2=\"{cordinates[2]}\" y2=\"{cordinates[3]}\" width =\"0.254\" layer =\"94\"/>")
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[2]}\" y1=\"{cordinates[3]}\" x2=\"{cordinates[4]}\" y2=\"{cordinates[5]}\" width=\"0.254\" layer=\"94\"/>")
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[4]}\" y1=\"{cordinates[5]}\" x2=\"{cordinates[6]}\" y2=\"{cordinates[7]}\" width=\"0.254\" layer=\"94\"/>")
    sy_wire_text.append(
        f"<wire x1=\"{cordinates[6]}\" y1=\"{cordinates[7]}\" x2=\"{cordinates[0]}\" y2=\"{cordinates[1]}\" width=\"0.254\" layer=\"94\"/>")

    # Create symbol details text
    sy_wire_text.append(
        f"<text x=\"21.59\" y=\"7.62\" align=\"center-left\" size=\"1.778\" layer=\"95\">&gt;{component['name']}</text>")
    sy_wire_text.append(
        f"<text x=\"21.59\" y=\"5.08\" align=\"center-left\" size=\"1.778\" layer=\"96\">&gt;{component['value']}</text>")

    # Append lines of text to lbr file
    for line in sy_wire_text:
        append_txt(lib_name, line)

    return True

# Symbol pins lines


def symbol_pins_txt(lib_name, pins):
    # Create list to store the text
    pins_text = list()

    # Create symbol pins text
    for pin in pins:
        pins_text.append(
            f"<pin name=\"{pin['name']}\" x=\"{pin['x']}\" y=\"{pin['y']}\" length=\"middle\" direction=\"{pin['direction']}\" rot=\"{pin['side']}\"/>")

    pins_text.append("</symbol>")
    pins_text.append("</symbols>")

    # Append lines of text to lbr file
    for line in pins_text:
        append_txt(lib_name, line)

    return True

# --- Other txt ---

def device_sets_txt(lib_name, component):
    # Create the var to store the text
    device_text_part = f"""
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
    # Append lines of text to lbr file
    append_txt(lib_name, device_text_part)

    return True


# Connects pin name to pad
def connects_txt(lib_name, smd_pads, pins):
    # Create list to store the text
    connects_text = list()

    pin_names = list()
    connects_text.append("<connects>")

    for pin in pins:
        pin_names.append(pin['name'])

    i = 0
    # Create connects text
    for pad in smd_pads:
        connects_text.append(
            f"<connect gate=\"G$1\" pin=\"{pin_names[i]}\" pad=\"{pad['name']}\"/>")
        i += 1

    connects_text.append("</connects>")

    # Append lines of text to lbr file
    for line in connects_text:
        append_txt(lib_name, line)

    return True

# Technologies text function
def technologies_txt(lib_name, component):
    # Create a string to store the text

    technologies_part = f"""<technologies>"
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

    # Append lines of text to lbr file
    append_txt(lib_name, technologies_part)

    return True

# ----------------- Lbr Creation Part -----------------
# Create first part of the lbr file

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

# Append text function
def append_txt(file_edit, text):
    with open(f"{file_edit}.lbr", "a") as output:
        output.write(text + "\n")
        return True


if __name__ == "__main__":
    main()
