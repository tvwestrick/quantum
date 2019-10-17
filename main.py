import q

q.display_code = 0

zero = q.Qubit(1, 0)
uno = q.Qubit(1, 0)
dos = q.Qubit(1, 0)
tres = q.Qubit(1, 0)
cuatro = q.Qubit(1, 0)

both = q.MultiQSyst([zero, uno])

user_input = ""

while user_input != "quit":

    user_input = input("> ")

    if user_input == "help":
        print("'H_' is the hadamard gate on qubit _")
        print("'X_' is the the Pauli X gate on the qubit in the _ index")
        print("'Y_' is the the Pauli Y gate on the qubit in the _ index")
        print("'Z_' is the the Pauli Z gate on the qubit in the _ index")
        print("'CNOT_,_' is the CNOT where the first _ is the control qubit and the second _ is the target qubit")
        print("'emoji' changes the display settings to emoji mode")
        print("'m_' measures the qubit at the _ index")

        print("'ket' changes the display settings to ket mode")

    if user_input == "":
        pass

    # single qubit gates
    elif user_input[0] == "H" and user_input[1:].isdigit():
        both.hadamard(int(user_input[1:]))

    elif user_input[0] == "X" and user_input[1:].isdigit():
        both.x(int(user_input[1:]))

    elif user_input[0] == "Y" and user_input[1:].isdigit():
        both.y(int(user_input[1:]))

    elif user_input[0] == "Z" and user_input[1:].isdigit():
        both.z(int(user_input[1:]))

    # multi qubit gates

    elif user_input[0:4] == "CNOT" and user_input.count(",") == 1 and user_input[4:].replace(",", "").isdigit():
        both.cnot(int(user_input[4: user_input.index(",")]), int(user_input[user_input.index(",") + 1:]))

    # measurement tools

    elif user_input == "m":
        both.measure_comp()

    elif user_input[0] == "T" and user_input[1:].isdigit():
        both.t(int(user_input[1:]))

    elif user_input[0] == "m" and user_input[1:] != "" and user_input[1:].isdigit():
        both.partial_m(int(user_input[1:]))

    # display settings

    elif user_input == "emoji":
        q.display_code = 1
        print("Emoji display activated")

    elif user_input == "ket":
        q.display_code = 0
        print("Ket display activated")

    else:
        pass
