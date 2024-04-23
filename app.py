import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
import math

# Dictionary to store points and their 2D coordinates
points_2d = {}

# Dictionary to store vectors between loaded 2D points
vectors_2d = {}

# Dictionary to store points and their 3D coordinates
points_3d = {}

# Dictionary to store vectors between loaded 3D points
vectors_3d = {}


# Function to open file dialog
def choose_file(dimension):
    path = filedialog.askopenfilename(initialfile="/", title="Choose file", filetypes=(("Text files", "*.txt"),))
    if path:
        try:
            with open(path, "r") as file:
                content = file.read()
                set_coordinates(content, dimension)
                if dimension == 2:
                    check_results_2d()
                elif dimension == 3:
                    check_result_3d()
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            # show_message("An error occurred", dimension)
            print("An error occurred:", e)


def set_coordinates(content, dimension):
    try:
        # Use regex to extract coordinates
        coordinates = re.findall(r"[-+]?\d*\.\d+|\d+", content)
        if dimension == 2:
            if len(coordinates) >= 8:
                global points_2d

                points_2d = {
                    'A': (float(coordinates[0]), float(coordinates[1])),
                    'B': (float(coordinates[2]), float(coordinates[3])),
                    'C': (float(coordinates[4]), float(coordinates[5])),
                    'X': (float(coordinates[6]), float(coordinates[7]))
                }

                label_A_value.config(text=f"({points_2d['A'][0]}, {points_2d['A'][1]})")
                label_B_value.config(text=f"({points_2d['B'][0]}, {points_2d['B'][1]})")
                label_C_value.config(text=f"({points_2d['C'][0]}, {points_2d['C'][1]})")
                label_X_value.config(text=f"({points_2d['X'][0]}, {points_2d['X'][1]})")
            else:
                message = "File does not contain enough coordinates (expected at least 8)"
                print(message)
                show_message(message, 2)
        elif dimension == 3:
            if len(coordinates) >= 15:
                global points_3d

                points_3d = {
                    'A': (float(coordinates[0]), float(coordinates[1]), float(coordinates[2])),
                    'B': (float(coordinates[3]), float(coordinates[4]), float(coordinates[5])),
                    'C': (float(coordinates[6]), float(coordinates[7]), float(coordinates[8])),
                    'D': (float(coordinates[9]), float(coordinates[10]), float(coordinates[11])),
                    'X': (float(coordinates[12]), float(coordinates[13]), float(coordinates[14]))
                }

                label_A_3D_value.config(text=f"({points_3d['A'][0]}, {points_3d['A'][1]}, {points_3d['A'][2]})")
                label_B_3D_value.config(text=f"({points_3d['B'][0]}, {points_3d['B'][1]}, {points_3d['B'][2]})")
                label_C_3D_value.config(text=f"({points_3d['C'][0]}, {points_3d['C'][1]}, {points_3d['C'][2]})")
                label_D_3D_value.config(text=f"({points_3d['D'][0]}, {points_3d['D'][1]}, {points_3d['D'][2]})")
                label_X_3D_value.config(text=f"({points_3d['X'][0]}, {points_3d['X'][1]}, {points_3d['X'][2]})")

            else:
                message = "File does not contain enough coordinates (expected at least 15)"
                print(message)
                show_message(message, 3)
    except Exception as e:
        print("An error occurred:", e)


def check_results_2d():
    # Creating vectors from point A
    vectors_2d['AB'] = (points_2d['B'][0] - points_2d['A'][0], points_2d['B'][1] - points_2d['A'][1])
    vectors_2d['AC'] = (points_2d['C'][0] - points_2d['A'][0], points_2d['C'][1] - points_2d['A'][1])

    # Creating vectors from point B
    vectors_2d['BA'] = (points_2d['A'][0] - points_2d['B'][0], points_2d['A'][1] - points_2d['B'][1])
    vectors_2d['BC'] = (points_2d['C'][0] - points_2d['B'][0], points_2d['C'][1] - points_2d['B'][1])

    # Creating vectors from point C
    vectors_2d['CA'] = (points_2d['A'][0] - points_2d['C'][0], points_2d['A'][1] - points_2d['C'][1])
    vectors_2d['CB'] = (points_2d['B'][0] - points_2d['C'][0], points_2d['B'][1] - points_2d['C'][1])

    can_be_rectangle = False

    # Checking scalar products of obtained vectors
    # If any of them equals 0, then we know points can be vertices of a rectangle or square
    if scalar_product_of_vectors(vectors_2d['AB'], vectors_2d['AC']) == 0:
        can_be_rectangle = 'A'
    elif scalar_product_of_vectors(vectors_2d['BA'], vectors_2d['BC']) == 0:
        can_be_rectangle = 'B'
    elif scalar_product_of_vectors(vectors_2d['CB'], vectors_2d['CB']) == 0:
        can_be_rectangle = 'C'

    # Here we check if points satisfy the first condition
    if can_be_rectangle:
        message1 = "Points A, B, and C can be vertices of a rectangle or a square."
        label_result_1.config(text=message1)
        print(message1)

        # Here we call the function to calculate the length of the diagonal
        diagonal_length = calculate_diagonal(can_be_rectangle, 2)
        message3 = f"The diagonal of the obtained shape is: {diagonal_length}"
        label_result_3.config(text=message3)
        print(message3)

        # Here we call the function to determine the shape
        shape = determine_shape(can_be_rectangle, 2)
        message4 = "The resulting shape of three points is " + shape
        label_result_4.config(text=message4)
        print(message4)

    else:
        message = "Points A, B, and C cannot be vertices of a rectangle."
        print(message)
        show_message(message, 2)


def check_result_3d():
    # Creating vectors from point A
    vectors_3d['AB'] = (
        points_3d['B'][0] - points_3d['A'][0], points_3d['B'][1] - points_3d['A'][1],
        points_3d['B'][2] - points_3d['A'][2])
    vectors_3d['AC'] = (
        points_3d['C'][0] - points_3d['A'][0], points_3d['C'][1] - points_3d['A'][1],
        points_3d['C'][2] - points_3d['A'][2])
    vectors_3d['AD'] = (
        points_3d['D'][0] - points_3d['A'][0], points_3d['D'][1] - points_3d['A'][1],
        points_3d['D'][2] - points_3d['A'][2])

    # Creating vectors from point B
    vectors_3d['BA'] = (
        points_3d['A'][0] - points_3d['B'][0], points_3d['A'][1] - points_3d['B'][1],
        points_3d['A'][2] - points_3d['B'][2])
    vectors_3d['BC'] = (
        points_3d['C'][0] - points_3d['B'][0], points_3d['C'][1] - points_3d['B'][1],
        points_3d['C'][2] - points_3d['B'][2])
    vectors_3d['BD'] = (
        points_3d['D'][0] - points_3d['B'][0], points_3d['D'][1] - points_3d['B'][1],
        points_3d['D'][2] - points_3d['B'][2])

    # Creating vectors from point C
    vectors_3d['CA'] = (
        points_3d['A'][0] - points_3d['C'][0], points_3d['A'][1] - points_3d['C'][1],
        points_3d['A'][2] - points_3d['C'][2])
    vectors_3d['CB'] = (
        points_3d['B'][0] - points_3d['C'][0], points_3d['B'][1] - points_3d['C'][1],
        points_3d['B'][2] - points_3d['C'][2])
    vectors_3d['CD'] = (
        points_3d['D'][0] - points_3d['C'][0], points_3d['D'][1] - points_3d['C'][1],
        points_3d['D'][2] - points_3d['C'][2])

    # Creating vectors from point D
    vectors_3d['DA'] = (
        points_3d['A'][0] - points_3d['D'][0], points_3d['A'][1] - points_3d['D'][1],
        points_3d['A'][2] - points_3d['D'][2])
    vectors_3d['DB'] = (
        points_3d['B'][0] - points_3d['D'][0], points_3d['B'][1] - points_3d['D'][1],
        points_3d['B'][2] - points_3d['D'][2])
    vectors_3d['DC'] = (
        points_3d['C'][0] - points_3d['D'][0], points_3d['C'][1] - points_3d['D'][1],
        points_3d['C'][2] - points_3d['D'][2])

    can_be_rectangular_prism = False

    # Calculating the scalar product of all vectors from point A
    product_vector_ab_ac = scalar_product_of_vectors(vectors_3d['AB'], vectors_3d['AC'])
    product_vector_ab_ad = scalar_product_of_vectors(vectors_3d['AB'], vectors_3d['AD'])
    product_vector_ac_ad = scalar_product_of_vectors(vectors_3d['AC'], vectors_3d['AD'])

    # Calculating the scalar product of all vectors from point B
    product_vector_ba_bc = scalar_product_of_vectors(vectors_3d['BA'], vectors_3d['BC'])
    product_vector_ba_bd = scalar_product_of_vectors(vectors_3d['BA'], vectors_3d['BD'])
    product_vector_bc_bd = scalar_product_of_vectors(vectors_3d['BC'], vectors_3d['BD'])

    # Calculating the scalar product of all vectors from point C
    product_vector_ca_cb = scalar_product_of_vectors(vectors_3d['CA'], vectors_3d['CB'])
    product_vector_ca_cd = scalar_product_of_vectors(vectors_3d['CA'], vectors_3d['CD'])
    product_vector_cb_cd = scalar_product_of_vectors(vectors_3d['CB'], vectors_3d['CD'])

    # Calculating the scalar product of all vectors from point D
    product_vector_da_db = scalar_product_of_vectors(vectors_3d['DA'], vectors_3d['DB'])
    product_vector_da_dc = scalar_product_of_vectors(vectors_3d['DA'], vectors_3d['DC'])
    product_vector_db_dc = scalar_product_of_vectors(vectors_3d['DB'], vectors_3d['DC'])

    # Checking the conditions here, and if any of them is true,
    # we store the name of the point from which the vectors are mutually orthogonal
    if product_vector_ab_ac == 0 and product_vector_ab_ad == 0 and product_vector_ac_ad == 0:
        can_be_rectangular_prism = 'A'
    elif product_vector_ba_bc == 0 and product_vector_ba_bd == 0 and product_vector_bc_bd == 0:
        can_be_rectangular_prism = 'B'
    elif product_vector_ca_cb == 0 and product_vector_ca_cd == 0 and product_vector_cb_cd == 0:
        can_be_rectangular_prism = 'C'
    elif product_vector_da_db == 0 and product_vector_da_dc == 0 and product_vector_db_dc == 0:
        can_be_rectangular_prism = 'D'

    # Here we check if the points satisfy the first condition
    if can_be_rectangular_prism:
        message5 = "Points A, B, C, and D can be vertices of a rectangular prism or a cube."
        label_result_5.config(text=message5)
        print(message5)
        print(can_be_rectangular_prism)

        # Here we call the function to calculate the length of the diagonal
        diagonal_length = calculate_diagonal(can_be_rectangular_prism, 3)
        message6 = f"The diagonal of the obtained shape is: {diagonal_length}"
        label_result_6.config(text=message6)
        print(message6)

        # Here we call the function to determine the shape
        shape = determine_shape(can_be_rectangular_prism, 3)
        message7 = "The resulting shape of four points is " + shape
        label_result_7.config(text=message7)
        print(message7)

    else:
        message = "Points A, B, C and D cannot be vertices of a rectangular prism."
        print(message)
        show_message(message, 3)


def point_x_in_rectangle():
    pass


def calculate_diagonal(start_point, dimension):
    if dimension == 2:
        # The diagonal can be obtained by the magnitude of vectors obtained from points other than start_point
        diagonal_vector = vectors_2d[[key for key in vectors_2d.keys() if start_point not in key][0]]
        return vector_magnitude(diagonal_vector)
    elif dimension == 3:
        # We need to calculate all side lengths, and then apply the formula for calculating the diagonal of a cube
        vectors_from_start_point = [vectors_3d[key] for key in vectors_3d.keys() if key.startswith(start_point)]

        v1_magnitude = vector_magnitude(vectors_from_start_point[0])
        v2_magnitude = vector_magnitude(vectors_from_start_point[1])
        v3_magnitude = vector_magnitude(vectors_from_start_point[2])

        diagonal_length = math.sqrt(v1_magnitude ** 2 + v2_magnitude ** 2 + v3_magnitude ** 2)
        return diagonal_length


def determine_shape(start_point, dimenstion):
    if dimenstion == 2:
        # Collecting vectors starting from the start_point
        vectors_from_start_point = [vectors_2d[key] for key in vectors_2d.keys() if key.startswith(start_point)]
        shape = 'rectangle'

        # Here we get the magnitudes of those vectors and if they are equal, it's a square.
        magnitude_1 = vector_magnitude(vectors_from_start_point[0])
        magnitude_2 = vector_magnitude(vectors_from_start_point[1])

        if magnitude_1 == magnitude_2:
            shape = 'square'

        return shape
    elif dimenstion == 3:
        # We need to calculate all side lengths,
        vectors_from_start_point = [vectors_3d[key] for key in vectors_3d.keys() if key.startswith(start_point)]

        v1_magnitude = vector_magnitude(vectors_from_start_point[0])
        v2_magnitude = vector_magnitude(vectors_from_start_point[1])
        v3_magnitude = vector_magnitude(vectors_from_start_point[2])

        shape = "rectangular prism"

        if v1_magnitude == v2_magnitude and v1_magnitude == v3_magnitude:
            shape = 'cube'

        return shape


def scalar_product_of_vectors(a, b):
    # Setting a_z to a[2] if it exists, otherwise to 0
    a_z = a[2] if len(a) > 2 else 0

    # Setting b_z to b[2] if it exists, otherwise to 0
    b_z = b[2] if len(b) > 2 else 0

    scalar_product = a[0] * b[0] + a[1] * b[1] + a_z * b_z
    return scalar_product


def vector_magnitude(vector):
    # Setting vector_z to vector[2] if it exists, otherwise to 0
    vector_z = vector[2] if len(vector) > 2 else 0

    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector_z ** 2)
    return magnitude


def show_message(message, dimension):
    popup = tk.Toplevel()
    popup.title("Notification")
    popup.overrideredirect(True)
    popup.geometry("400x100")

    label = tk.Label(popup, text=message, padx=10, pady=10)
    label.pack()

    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    cleaning_data(dimension)

    button = tk.Button(popup, text="OK", command=popup.destroy, width=20)
    button.pack(pady=10)


def cleaning_data(dimension):
    if dimension == 2:
        label_result_1.config(text="")
        label_result_2.config(text="")
        label_result_3.config(text="")
        label_result_4.config(text="")

        global points_2d
        global vectors_2d

        points_2d
        vectors_2d = {}

    elif dimension == 3:
        label_result_5.config(text="")
        label_result_6.config(text="")
        label_result_7.config(text="")
        label_result_8.config(text="")

        global points_3d
        global vectors_3d

        points_3d = {}
        vectors_3d = {}


# Creating the main window
root = tk.Tk()
root.geometry("800x650")
root.title("Assignment")

label_2D = tk.Label(root, text="Choose a file with 2D coordinates", font=("Arial", 10))
label_2D.pack(pady=10)

# Creating a button to choose a file with 2D coordinates
button_2D = tk.Button(root, text="Choose file", command=lambda: choose_file(2), height=1, width=10, bg="#74bdfc",
                      pady=5,
                      fg="#ffffff",
                      font=("Arial", 10, "bold"))
button_2D.pack()

# Creating a frame to organize labels for 2D points
div_frame = tk.Frame(root, pady=10)
div_frame.pack()

# Creating labels with names of 2D points
label_A = tk.Label(div_frame, text="A", font=("Arial", 8, 'bold'))
label_A.grid(row=0, column=0, padx=50)
label_B = tk.Label(div_frame, text="B", font=("Arial", 8, 'bold'))
label_B.grid(row=0, column=1, padx=50)
label_C = tk.Label(div_frame, text="C", font=("Arial", 8, 'bold'))
label_C.grid(row=0, column=2, padx=50)
label_X = tk.Label(div_frame, text="X", font=("Arial", 8, 'bold'))
label_X.grid(row=0, column=3, padx=50)

# Creating labels for loaded 2D coordinates of points
label_A_value = tk.Label(div_frame, text="( , )", font=("Arial", 8, 'bold'))
label_A_value.grid(row=1, column=0, pady=10)
label_B_value = tk.Label(div_frame, text="( , )", font=("Arial", 8, 'bold'))
label_B_value.grid(row=1, column=1, pady=10)
label_C_value = tk.Label(div_frame, text="( , )", font=("Arial", 8, 'bold'))
label_C_value.grid(row=1, column=2, pady=10)
label_X_value = tk.Label(div_frame, text="( , )", font=("Arial", 8, 'bold'))
label_X_value.grid(row=1, column=3, pady=10)

div_frame_for_result = tk.Frame(root, pady=10)
div_frame_for_result.pack()

# Creating labels for 2D results
label_result_1 = tk.Label(div_frame_for_result, text="", font=("Arial", 10, 'bold'))
label_result_1.pack(pady=4)

label_result_2 = tk.Label(div_frame_for_result, text="", font=("Arial", 10, 'bold'))
label_result_2.pack(pady=4)

label_result_3 = tk.Label(div_frame_for_result, text="", font=("Arial", 10, 'bold'))
label_result_3.pack(pady=4)

label_result_4 = tk.Label(div_frame_for_result, text="", font=("Arial", 10, 'bold'))
label_result_4.pack(pady=4)

label_2D = tk.Label(root, text="Choose a file with 3D coordinates", font=("Arial", 10))
label_2D.pack(pady=10)

# Creating a button to choose a file with 3D coordinates
button_3D = tk.Button(root, text="Choose file", command=lambda: choose_file(3), height=1, width=10, bg="#74bdfc",
                      pady=5,
                      fg="#ffffff",
                      font=("Arial", 10, "bold"))
button_3D.pack()

# Creating a frame to organize labels for 3D points
div_frame_3 = tk.Frame(root, pady=10)
div_frame_3.pack()

# Creating labels with names of 3D points
label_A_3d = tk.Label(div_frame_3, text="A", font=("Arial", 8, 'bold'))
label_A_3d.grid(row=0, column=0, padx=50)
label_B_3d = tk.Label(div_frame_3, text="B", font=("Arial", 8, 'bold'))
label_B_3d.grid(row=0, column=1, padx=50)
label_C_3d = tk.Label(div_frame_3, text="C", font=("Arial", 8, 'bold'))
label_C_3d.grid(row=0, column=2, padx=50)
label_D_3d = tk.Label(div_frame_3, text="D", font=("Arial", 8, 'bold'))
label_D_3d.grid(row=0, column=3, padx=50)
label_X_3d = tk.Label(div_frame_3, text="X", font=("Arial", 8, 'bold'))
label_X_3d.grid(row=0, column=4, padx=50)

# Creating labels for loaded 3D coordinates of points
label_A_3D_value = tk.Label(div_frame_3, text="( , , )", font=("Arial", 8, 'bold'))
label_A_3D_value.grid(row=1, column=0, pady=10)
label_B_3D_value = tk.Label(div_frame_3, text="( , , )", font=("Arial", 8, 'bold'))
label_B_3D_value.grid(row=1, column=1, pady=10)
label_C_3D_value = tk.Label(div_frame_3, text="( , , )", font=("Arial", 8, 'bold'))
label_C_3D_value.grid(row=1, column=2, pady=10)
label_D_3D_value = tk.Label(div_frame_3, text="( , , )", font=("Arial", 8, 'bold'))
label_D_3D_value.grid(row=1, column=3, pady=10)
label_X_3D_value = tk.Label(div_frame_3, text="( , , )", font=("Arial", 8, 'bold'))
label_X_3D_value.grid(row=1, column=4, pady=10)

div_frame_for_result_3d = tk.Frame(root, pady=10)
div_frame_for_result_3d.pack()

# Creating labels for 3D results
label_result_5 = tk.Label(div_frame_for_result_3d, text="", font=("Arial", 10, 'bold'))
label_result_5.pack(pady=4)

label_result_6 = tk.Label(div_frame_for_result_3d, text="", font=("Arial", 10, 'bold'))
label_result_6.pack(pady=4)

label_result_7 = tk.Label(div_frame_for_result_3d, text="", font=("Arial", 10, 'bold'))
label_result_7.pack(pady=4)

label_result_8 = tk.Label(div_frame_for_result_3d, text="", font=("Arial", 10, 'bold'))
label_result_8.pack(pady=4)

root.mainloop()
