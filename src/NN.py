import numpy as np
import random
# This code just work for the example, so lets define the architecture
nn_layers = [6, 6, 3, 2]
chromosome_len = 4

# Activation functions


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(0, z)


def tanh(z: np.ndarray) -> np.ndarray:
    return np.tanh(z)


def leaky_relu(z: np.ndarray) -> np.ndarray:
    return np.where(z > 0, z, z * 0.01)


class Gen():
    """ A gen is a representation of a conection in the Neuronal Network
    Each gen is a sequense of 4 numbers, the start layer, departure neuron, arrival neuron and the 
    weight
    """
    global nn_layers

    def __init__(self, code=[0, 0, 0, 0]) -> None:
        self.code = [0, 0, 0, 0]
        self.set_code(code)
        self.binary = ""
        for value in self.code:
            self.binary += format(value, '08b')

    def __str__(self) -> str:
        return str(self.get_code())

    def __repr__(self) -> str:
        return str(self.get_code())

    def get_code(self) -> list:
        return self.code.copy()

    def set_code(self, code: list) -> None:
        if (code[0] > 0) and (code[0] < (len(nn_layers)-1)):
            self.code[0] = int(code[0])
        if (code[1] > 0) and (code[1] < nn_layers[self.code[0]]):
            self.code[1] = int(code[1])
        if (code[2] > 0) and (code[2] < nn_layers[self.code[0] + 1]):
            self.code[2] = int(code[2])
        self.code[3] = code[3]

    def mute(self) -> None:
        for _ in range(random.randint(0, 5)):
            new_code = self.get_code()
            index = random.randint(0, 3)
            new_code[index] += (random.random() - 0.5)*4
            self.set_code(new_code)


class Chromosome():
    """Each Chromosome have 24 gens (the meaning of the life in reverse)
    also the Chromosome can combinate with other Chromosomes and just mutate itself.
    """

    def __init__(self, sequence=[]) -> None:
        if len(sequence) != chromosome_len:
            sequence = [Gen([random.randint(0, 6) for _ in range(4)])
                        for _ in range(chromosome_len)]
        self.set_sequence(sequence)

    def set_sequence(self, sequence) -> None:
        if len(sequence) != chromosome_len:
            print(f"The sequence need {chromosome_len} elements")
            return None
        for i, element in enumerate(sequence):
            if type(element) != Gen:
                print(f"The element {i} is not a Gen is {type(element)}")
                return None
        self.sequence = sequence

    def get_sequence(self) -> list:
        return self.sequence.copy()

    def mute(self) -> None:
        for _ in range(random.randint(0, 15)):
            new_sequence = self.get_sequence()
            index = random.randint(0, chromosome_len - 1)
            new_sequence[index].mute()
            self.set_sequence(new_sequence)

    def mix(self, parent):
        mother = self.get_sequence()
        father = parent.get_sequence()
        new_sequence = mother + father
        random.shuffle(new_sequence)
        new_sequence = new_sequence[:chromosome_len]
        children = Chromosome(new_sequence)

        return children


class NN():
    """ This class represent a Neuronal Network that is create from a Chromosome
    The NN have as input 6 parameters
    1. The x coordenate of the obstacle
    2. The y coordenate of the obstacle
    3. The high of the obstacle 
    4. The weight of the obstacle
    5. The y coordenate of the dino
    6. The velocity of the game 
    """

    def __init__(self, chromosome: Chromosome) -> None:
        self.chromosome = chromosome

    def predict(self, input: np.ndarray) -> np.ndarray:
        return np.dot(self.weights, input)


print("PADRE")
test1 = Chromosome()
for elem in test1.get_sequence():
    print(elem)

print("MADRE")
test2 = Chromosome()
for elem in test2.get_sequence():
    print(elem)
print("HIJO")
child = test1.mix(test2)
for elem in child.get_sequence():
    print(elem)

# test = Gen([2, 3, 0, 2])
# print(test.code)
# for _ in range(6):
#     test.mute()
#     print(test.code)
# test = NN(np.asarray([np.arange(5) for i in range(5)]))
# print(test.predict(np.arange(5)))
