import cmath


def complex_conj(compl):
    return compl.real + -1*compl.imag*1j


def dictionary_sort(dictionary):
    new_dict = dict()
    for key in sorted(dictionary.keys()):
        new_dict[key] = dictionary[key]
    return new_dict


def norm_dict(dictionary):
    coefficients = dictionary.values()

    norm_coef = norm_list(coefficients)

    i = 0
    for basis in dictionary.keys():
        dictionary.update({basis: norm_coef[i]})
        i += 1


def norm_list(list):
    length = 0

    for constant in list:
        length = length + constant * complex_conj(constant)

    # finds norm squared for list vector

    length = cmath.sqrt(length)

    normalized_list = []

    for constant in list:
        normalized_list.append(constant/length)

    return normalized_list
