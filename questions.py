component = dict()

# Surface mount
single_package_smt = ["SIL"]

small_outline_package = ["DFN", "DIL", "SOIC", "SOJ", "SON", "PSON", "WSON", "USON", "SOP", "CSOP", "DSOP", "HSOP",
                         "SSOP", "TSOP",  "HTSOP", "VSOP", "TVSOP" "MSOP", "PSOP", "QSOP", "SSOP", "HSSOP",  "TSSOP", "VSSOP", "HTSSOP", "TSOP"]

quad_flat_package = ["DFN", "QFN", "PQFN",
                     "UQFN", "VQFN", "HVQFN", "WQFN", "CFP", "QFP",  "BQFP", "CQFP", "LQFP", "MQFP", "PQFP", "TQFP", "ETQFP", "VQFP"]

# Questions for Library and Component data
def component_questions():

    # Default values
    lib_name = ''
    component['name'] = ''
    component['package'] = ''
    component['datasheet'] = ''
    component['pins'] = ''
    component['center_pad'] = ''
    component['quad_l_r_pins'] = ''
    component['quad_t_b_pins'] = ''

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
        package = ''
        print("")
        print("What is the package? (required)")
        component['package'] = input().strip().upper()
        if '-' in component['package']:
            try:
                package, pins = component['package'].split("-")
                component['pins'] = int(pins)
            except ValueError:
                print("Wrong Package Format")
                component['package'] = ''

        # Check package_type
        if component['package'] in single_package_smt or package in single_package_smt:
            component['package_type'] = "single_package"

        elif component['package'] in small_outline_package or package in small_outline_package:
            component['package_type'] = "dual_package"

        elif component['package'] in quad_flat_package or package in quad_flat_package:
            component['package_type'] = "quad_package"

        else:
            print("Package not available")
            component['package'] = ''
            component['pins'] = ''

    # Total number of pins
    while not component['pins']:
        try:
            print("")
            print("How many pins does it have? (required)")
            component['pins'] = int(input())
            if component['pins'] % 2 != 0 and component['package_type'] != "single_package":
                print("Not a pair number")
                component['pins'] = ''

        except ValueError:
            print("Not a number")

    # # Bottom/Center/Thermal pads
    while component['center_pad'] == '':
        print("")
        print("Does it have a Bottom/Center/Thermal pad? (required)")
        component['center_pad'] = input().strip().upper()
        if component['center_pad'] == "Y" or component['center_pad'] == "YES" or component['center_pad'] == "1":
            component['center_pad'] = 1

        elif component['center_pad'] == "N" or component['center_pad'] == "NO" or component['center_pad'] == "0":
            component['center_pad'] = 0

        else:
            component['center_pad'] = ''
            print("Not a valid answer")

    # single package bottom pins
    if component['package_type'] == "single_package":
        component['quad_t_b_pins'] = component['pins']

    # Dual package left pins
    elif component['package_type'] == "dual_package":
        component['quad_l_r_pins'] = component['pins']/2

    # Quad package Question
    elif component['package_type'] == "quad_package":
        while True:
            try:
                while not component['quad_l_r_pins']:
                    print("")
                    print("How many pins does it have on the left side? (required)")
                    component['quad_l_r_pins'] = int(input())
            except ValueError:
                print("Not a number")

            try:
                while not component['quad_t_b_pins']:
                    print("")
                    print("How many pins does it have on the top side? (required)")
                    component['quad_t_b_pins'] = int(input())

            except ValueError:
                print("")
                print("Not a number")

            if component['pins'] != ((component['quad_l_r_pins'] * 2) + (component['quad_t_b_pins'] * 2)):
                print("")
                print("Total pins do not match sides")
                component['quad_l_r_pins'] = ''
                component['quad_t_b_pins'] = ''

            else:
                break

# Questions for Component Sizing

    # Default values
    component['length'] = ''
    component['width'] = ''
    component['spacing'] = ''
    component['pads_length'] = ''
    component['pads_width'] = ''
    component['pads_distance_l_r'] = ''
    component['pads_distance_t_b'] = ''
    component['pads_distance_c_b'] = ''
    component['center_pad_length'] = ''
    component['center_pad_width'] = ''

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
    print("                 ")
    print("  -------------- ")
    print("  |        ____|_")
    print("  | W     |______")
    print("  |            | ")
    print("  -------------- ")
    print("        L        ")

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

    # Size of # Bottom/Center/Thermal pad

    if component['center_pad'] == 1:
        print("                 ")
        print("  -------------- ")
        print("  |            | ")
        print("  |           L| ")
        print("  |            | ")
        print("  | o          | ")
        print("  -------------- ")
        print("         W       ")

        # Ask pad length
        while not component['center_pad_length']:
            try:
                print("")
                print("How much is the length(L) of the pad? (mm) (required)")
                component['center_pad_length'] = float(input())

            except ValueError:
                print("Not a number")

        # Ask pad width
        while not component['center_pad_width']:
            try:
                print("")
                print("How much is the width(W) of the pad? (mm) (required)")
                component['center_pad_width'] = float(input())

            except ValueError:
                print("Not a number")

    if component['package_type'] == "single_package":
        print("                  ")
        print("    -----------   ")
        print("    |O        |   ")
        print("    |         |   ")
        print(" ^  |    x    |   ")
        print(" C  |         |   ")
        print(" |  |_________|   ")
        print(" v    |  |  |     ")

        # Ask distance between Pads
        while not component['pads_distance_c_b']:
            try:
                print("")
                print(
                    "How much is the distance(C) between the IC center and Bottom pads center? (mm) (required)")
                component['pads_distance_c_b'] = float(input())

            except ValueError:
                print("Not a number")

    if component['package_type'] == "dual_package" or component['package_type'] == "quad_package":
        print("                   ")
        print("   < - - P - - >   ")
        print("     ---------     ")
        print(" [-]-|O      |-[-] ")
        print("     |       |     ")
        print(" [-]-|       |-[-] ")
        print("     |       |     ")

        # Ask distance between Pads
        while not component['pads_distance_l_r']:
            try:
                print("")
                print(
                    "How much is the distance(P) between the Left and Right pads center? (mm) (required)")
                component['pads_distance_l_r'] = float(input())

            except ValueError:
                print("Not a number")

    if component['package_type'] == "quad_package":
        print("                  ")
        print(" ^    |  |  |     ")
        print(" |  -----------   ")
        print(" |  |O        |   ")
        print(" T  |         |   ")
        print(" |  |         |   ")
        print(" |  |_________|   ")
        print(" v    |  |  |     ")

        # Ask distance between Pads
        while not component['pads_distance_t_b']:
            try:
                print("")
                print(
                    "How much is the distance(T) between the Top and Bottom pads center? (mm) (required)")
                component['pads_distance_t_b'] = float(input())

            except ValueError:
                print("Not a number")

    return lib_name, component

# ----------------- Questions Part -----------------
# Questions for pin data


def pin_questions(pin_number, pin_list):
    # Default values
    pin_name = ''
    pin_direction = ''

    # Create direction list
    direction_list = ["nc", "in", "out", "io",
                      "oc", "hiz", "pas", "pwr", "sup"]

    # Ask Pin Name
    while not pin_name:
        print("")
        print(f"What is the name of pin{pin_number + 1} ? (required)")
        pin_name = input().strip().upper().replace(" ", "_")

        # Check if Pin name is unique
        if not any(p['name'] == pin_name for p in pin_list):
            continue
        else:
            print("")
            print("Pin name already used")
            pin_name = ''

    # Ask Pin Direction
    while not pin_direction:
        try:
            print("")
            print(f"Direction of pin{pin_number + 1} (required)")
            print("1: Not connected")
            print("2: Input")
            print("3: Output")
            print("4: In/output")
            print("5: Open collector or open drain")
            print("6: High impedance output")
            print("7: Passive ")
            print("8: Power input")
            print("9: General supply")
            print("")
            print("Insert option number ")
            answer = int(input().strip())

            if answer in range(1, 10):
                pin_direction = direction_list[answer-1]

            else:
                print("Not a valid option")

        except ValueError:
            print("Not a valid answer")

    return pin_name, pin_direction

# Questions for # Bottom/Center/Thermal pad
def center_pad_questions(pin_list):
    # Default values
    center_name = ''
    center_direction = ''

    # Pin direction list
    direction_list = ["nc", "in", "out", "io",
                      "oc", "pwr", "pas", "hiz", "sup"]

    # Ask Pin Name
    while not center_name:
        print("")
        print(f"What is the name of Bottom/Center/Thermal pad name ? (required)")
        center_name = input().strip().upper().replace(" ", "_")

        # Check if Pin name is unique
        if not any(p['name'] == center_name for p in pin_list):
            continue
        else:
            print("")
            print("Pin name already used")
            center_name = ''

    # Ask Pin Direction
    while not center_direction:
        try:
            print("")
            print("Direction of Central pad ? (required)")
            print("1: Not connected")
            print("2: Input")
            print("3: Output")
            print("4: In/output")
            print("5: Open collector or open drain")
            print("6: High impedance output")
            print("7: Passive ")
            print("8: Power input")
            print("9: General supply")
            print("")
            print("Insert option number ")
            answer = int(input().strip())

            if answer in range(1, 10):
                center_direction = direction_list[answer-1]
            else:
                print("Not a valid option")

        except ValueError:
            print("Not a valid answer")

    return center_name, center_direction

# Questions for Orientation simbol and Pin counting
def orientation_questions():
    orientation_symbol = ''
    orientation_position = ''
    pin_counter = ''

    # Orientation Symbol
    print("")
    print("Orientation symbol")
    print("1: line ")
    print("2: dot ")
    print("3: triangle")
    print("0: default")

    while orientation_symbol == '':
        try:
            print("")
            print("Insert option number ")
            answer = int(input().strip())

            if answer in range(4):
                orientation_symbol = answer

            else:
                print("")
                print("Wrong option")

        except ValueError:
            print("Not a valid answer")

    # Default options
    if orientation_symbol == 0:
        orientation_symbol = 2
        orientation_position = 2
        pin_counter = 0

    # Orientation position
    if orientation_symbol == '1' and orientation_position == '':
        print("")
        print("Symbol position")
        print("1: Under pad")
        print("2: Over pad ")
        while orientation_position == '':
            try:
                print("")
                print("Insert option number ")
                answer = int(input().strip())

                if answer in range(1, 3):
                    orientation_position = answer

                else:
                    print("")
                    print("Not a valid option")

            except ValueError:
                print("Not a valid answer")

    elif orientation_position == '':
        print("")
        print("Orientation symbol")
        print("1: Next to pad ")
        print("2: Over pad ")
        print("3: Corner ")

        while orientation_position == '':
            try:
                print("")
                print("Insert option number ")
                answer = int(input().strip())

                if answer in range(4):
                    orientation_position = answer
                else:
                    print("")
                    print("Not a valid option")

            except ValueError:
                print("Not a valid answer")

    # Pin Count
    if pin_counter == '':
        print("")
        print("Pin Count information")
        print("0: No pin count ")
        print("1: Marking on 5 and 10 pins ")
        print("2: Marking on 5 and 10 pins and total on 10 pins ")
        print("3: Marking on 5 and 10 pins and total on component edges ")

        while pin_counter == '':
            try:
                print("")
                print("Insert option number ")
                answer = int(input().strip())

                if answer in range(4):
                    pin_counter = answer
                else:
                    print("")
                    print("Not a valid option")

            except ValueError:
                print("Not a valid answer")

    return orientation_symbol, orientation_position, pin_counter
