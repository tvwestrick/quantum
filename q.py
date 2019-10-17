import random
import displays
import org_func
import cmath


display_code = int()
root_half = cmath.sqrt(0.5)

def display_choice(dictionary):
    # display choice is in the variable display_code
    if display_code == 0:
        return displays.ket_display(dictionary)
    elif display_code == 1:
        return displays.emoji_display(dictionary)


def binary_rep(number, bit_count):
    i = bit_count - 1
    # adjusts bit_count to the indexing of a string, as i
    representation = ""
    while i >= 0:
        if number >= 2**i:
            representation = representation + "1"
            number = number - 2**i
        else:
            representation = representation + "0"
        i -= 1
    return representation


def complex_conj(compl):
    return compl.real + -1*compl.imag*1j


class Qubit:
    def __init__(self, zero_basis, one_basis):
        self.q = org_func.norm_list([zero_basis, one_basis])
        # q is a list with the coefficients of the zero basis and the one basis
        # note that the zero_basis coefficient is at the zero index (same with the one_basis coefficient and one index)

class MultiQSyst:
    def __init__(self, qubit_list):
        self.qubit_list = qubit_list

        # displays the individual states of the qubits in the computational basis, using the display choice

        if display_code == 1:
            i = 0
            while i < len(qubit_list):
                print(f"Qubit {str(i)} -- {qubit_list[i].q[0]}⬆️ + {qubit_list[i].q[1]}➡️️")
                i += 1
        elif display_code == 0:
            i = 0
            while i < len(qubit_list):
                print(f"Qubit {str(i)} -- {qubit_list[i].q[0]}|0＞️ + {qubit_list[i].q[1]}|1＞️️")
                i += 1

        # creates all_basis, a list of all the basis states
        start = 0
        self.all_basis = []
        while start < 2**len(qubit_list):
            self.all_basis.append(binary_rep(start, len(qubit_list)))
            start += 1

        # creates the dictionary self.qsyst; keys are basis states as strings, values are the coefficients
        self.qsyst = dict()
        for basis in self.all_basis:
            i = 0
            coefficient = 1
            while i < len(basis):
                if int(basis[i]) == 1:
                    coefficient = coefficient * qubit_list[i].q[1]
                else:
                    coefficient = coefficient * qubit_list[i].q[0]
                i += 1
            self.qsyst[basis] = coefficient

        print("Syst --> " + display_choice(self.qsyst))

    def cnot(self, control, target):
        # control and target are the index of the qubits in the list
        if control == target:
            print("Target qubit cannot be same as control qubit.")
        elif control >= len(self.qubit_list) or target >= len(self.qubit_list):
            print("At least one of those qubits does not exist.")
        else:
            self.cnot_qsyst = dict()

            for basis in self.all_basis:
                switched_basis = basis[0: target] + str((int(basis[target]) + int(basis[control])) % 2) + basis[target+1:]
                # switched_basis is the basis that will take the coefficient from basis
                self.cnot_qsyst[switched_basis] = self.qsyst[basis]

            self.qsyst.clear()

            for basis in sorted(self.cnot_qsyst):
                self.qsyst.update({basis: self.cnot_qsyst[basis]})

            print("--> CNOT --> " + display_choice(self.qsyst))

            org_func.norm_dict(self.qsyst)

    def single_gate(self, index, matrix, name):
        if index >= len(self.qubit_list):
            print("Qubit DNE")
        else:
            double_list = []
            # double_list makes a list of list of each basis and a basis with a indexed qubit reversed
            # called double_list because every pair is double counted
            for basis in self.qsyst.keys():
                double_list.append([basis, basis[0: index] + str((int(basis[index]) + 1) % 2) + basis[index+1:]])

            for pair in double_list:
                pair.sort()

            # creates basis_pairs, which is double_list with repeats removed
            basis_pairs = []
            for pair in double_list:
                if pair not in basis_pairs:
                    basis_pairs.append(pair)

            # creates basis_pairs_coef, which is the the pairs of coefficients of the basis pairs
            basis_pairs_coef = []
            for pair in basis_pairs:
                pair_coef = []
                for component in pair:
                    pair_coef.append(self.qsyst[component])
                basis_pairs_coef.append(pair_coef)

            # gated_pair_coef, is the new coefficient pairs after the gate is applied
            gated_pair_coef = []
            for pair in basis_pairs_coef:
                new_pair = [matrix[0][0] * pair[0] + matrix[0][1] * pair[1], matrix[1][0] * pair[0] + matrix[1][1] * pair[1]]
                gated_pair_coef.append(new_pair)

            #recreates the dictionary with the gate applied
            self.qsyst.clear()
            i = 0
            while i < len(basis_pairs):
                update = {basis_pairs[i][0] : gated_pair_coef[i][0], basis_pairs[i][1] : gated_pair_coef[i][1]}
                self.qsyst.update(update)
                i += 1

            self.qsyst = org_func.dictionary_sort(self.qsyst)

            print(name + " --> " + display_choice(self.qsyst))

    # Pauli Gates

    def x(self, index):
        x = [[0, 1],
             [1, 0]]

        self.single_gate(index, x, "[X]" + str(index))

    def y(self, index):
        y = [[0, -1j],
             [1j, 0]]

        self.single_gate(index, y, "[Y]" + str(index))

    def z(self, index):
        z = [[1, 0],
             [0, -1]]

        self.single_gate(index, z, "[Z]" + str(index))

    # Other single qubit gates

    def hadamard(self, index):
        h = [[root_half, root_half],
             [root_half, -1 * root_half]]

        self.single_gate(index, h, "[H]" + str(index))

    def t(self, index):
        t = [[1, 0],
             [0, cmath.exp(1j*0.25*cmath.pi)]]
        self.single_gate(index, t, "[T]" + str(index))


    def measure_comp(self):
        # measures the entire system in the computational basis
        rand = random.random()
        lower_bound = 0
        upper_bound = 0
        done = 0

        i = 0
        while done == 0:
            basis = self.all_basis[i]
            upper_bound = upper_bound + (self.qsyst[basis] * complex_conj(self.qsyst[basis])).real
            if lower_bound <= rand < upper_bound:
                for thing in self.all_basis:
                    if thing != basis:
                        self.qsyst.update({thing: 0})
                        done = 1
            else:
                lower_bound = upper_bound

            i += 1

        org_func.norm_dict(self.qsyst)

        print("--> m --> " + display_choice(self.qsyst))

    def partial_m(self, index):
        # a partial measurement on a single qubit in the computational basis
        if index >= len(self.qubit_list):
            print("Qubit DNE")
        else:
            basis_zeroes = []
            basis_ones = []

            # separates the basis states into basis states with zero at the index (basis_zeroes)
            # and basis states with one at the index

            for basis in self.qsyst.keys():
                if basis[index] == "0":
                    basis_zeroes.append(basis)
                else:
                    basis_ones.append(basis)

            probability = 0
            for basis in basis_zeroes:
                probability = (self.qsyst[basis] * complex_conj(self.qsyst[basis])).real + probability

            rand = random.random()

            if rand <= probability:
                for basis in basis_ones:
                    self.qsyst.update({basis: 0})
            else:
                for basis in basis_zeroes:
                    self.qsyst.update({basis: 0})

            org_func.norm_dict(self.qsyst)

            print("--> m" + str(index) + " --> " + display_choice(self.qsyst))




