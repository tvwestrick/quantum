def ket_display(dictionary):

    display = ""

    for key in list(dictionary.keys()):
        ket_key = "|" + key + "＞"

        if dictionary[key].real == 0 and dictionary[key].imag == 0:
            display = display
        elif display == "":
            display = display + f' {dictionary[key]}{ket_key}'
        else:
            display = display + f' + {dictionary[key]}{ket_key} '

    return display


def emoji_display(dictionary):

    display = ""

    for key in list(dictionary.keys()):
        emoji_key = ""
        i = 0
        while i < len(key):
            if key[i] == "0":
                emoji_key = emoji_key + "⬆️"
            elif key[i] == "1":
                emoji_key = emoji_key + "➡️️"
            i += 1

        if dictionary[key].real == 0 and dictionary[key].imag == 0:
            display = display
        elif display == "":
            display = display + f' {dictionary[key]}{emoji_key}'
        else:
            display = display + f' + {dictionary[key]}{emoji_key} '

    return display