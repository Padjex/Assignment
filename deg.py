import math


def degr(x):
    p_radians = math.acos(x)

    # Pretvori radijane u stupnjeve
    p_degrees = math.degrees(p_radians)

    # Ispis rezultata
    print("Kut p u radijanima:", p_radians)
    print("Kut p u stupnjevima:", p_degrees)


def angle_between_vectors(a, b):

    numerator = scalar_product_of_vectors(a, b)
    denominator = vector_magnitude(a) * vector_magnitude(b)

    print(numerator)
    print(denominator)

    cos_value = numerator / denominator
    return cos_value


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
