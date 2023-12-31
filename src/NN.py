import numpy as np
import random
# This code just work for the example, so lets define the architecture
nn_layers = [7, 6, 2]
chromosome_len = 24
nn_umbral = 0.5

mutation_range = [-1, 1]
mutations_cuantity = 2

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
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

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Gen):
            return __value.get_code() == self.get_code()
        return False

    def __str__(self) -> str:
        return str(self.get_code())

    def __repr__(self) -> str:
        return str(self.get_code())

    def get_code(self) -> list:
        return self.code.copy()

    def set_code(self, code: list) -> None:
        self.code = [0, 0, 0, 0]
        if ((code[0] >= 0) and (code[0] < (len(nn_layers)-1))):
            self.code[0] = int(code[0])
        if ((code[1] >= 0) and (code[1] < nn_layers[self.code[0]])):
            self.code[1] = int(code[1])
        if ((code[2] >= 0) and (code[2] < nn_layers[self.code[0] + 1])):
            self.code[2] = int(code[2])
        self.code[3] = code[3]

    def get_start_neuron(self) -> tuple:
        return (self.code[0], self.code[1])

    def get_end_neuron(self) -> tuple:
        return (self.code[0] + 1, self.code[2])

    def mute(self) -> None:
        for _ in range(random.randint(0, mutations_cuantity)):
            new_code = self.get_code()
            index = random.randint(0, 3)
            new_code[index] += mutation_range[0] + \
                random.random()*(mutation_range[1] - mutation_range[0])
            self.set_code(new_code)


class Chromosome():
    """Each Chromosome have 24 gens (the meaning of the life in reverse)
    also the Chromosome can combinate with other Chromosomes and just mutate itself.
    """
    global nn_layers, chromosome_len

    def __init__(self, sequence=[]) -> None:
        if len(sequence) != chromosome_len:
            # Then create a random Chromosome
            sequence = []
            for _ in range(chromosome_len):
                # Some optimizations for the architecture to get more uniform gens
                new_gen = [random.randint(0, len(nn_layers) - 1), random.randint(
                    0, nn_layers[0]), random.randint(0, nn_layers[0]), random.randint(-6, 6)]
                sequence.append(Gen(new_gen))

        self.set_sequence(sequence)

    def __str__(self) -> str:
        text = ""
        for gen in self.get_sequence():
            text += str(gen) + "\n"
        return text

    def set_sequence(self, sequence) -> None:
        # Check the sequence, need the specific len and all elements be Gen
        if len(sequence) != chromosome_len:
            print(f"The sequence need {chromosome_len} elements")
            return None
        for i, element in enumerate(sequence):
            if type(element) != Gen:
                print(f"The element {i} is not a Gen is {type(element)}")
                return None
        # Now, for optimization, if some gen have the same start and end neuron then
        # replace the gen with other randomn gen.

        def replace_duplicates_with_random(first_sequence) -> tuple:
            seen = {}  # Dictionary to keep track of seen lists
            result = []  # List to store the final result

            count = 0  # Counter for duplicates elements

            for gen in first_sequence:
                code = gen.get_code()
                key = tuple(code[:3])  # Use the first three elements as a key

                if key in seen:
                    # If duplicate found, replace with random elements
                    random_elements = [random.randint(0, len(nn_layers) - 1), random.randint(
                        0, nn_layers[0]), random.randint(0, nn_layers[0]), code[3]]
                    result.append(Gen(random_elements))
                    count += 1
                else:
                    seen[key] = code[:3]
                    result.append(Gen(code))
            return (result, count)
        duplicates = 1
        final_sequence = sequence
        while duplicates != 0:
            final_sequence, duplicates = replace_duplicates_with_random(
                final_sequence)
        self.sequence = final_sequence

    def get_sequence(self) -> list:
        return self.sequence.copy()

    def mute(self) -> None:
        for _ in range(random.randint(0, mutations_cuantity)):
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


class Agent():
    """ This class represent a Agent that based on his chromosome can make predictions
    the prediction have 2 values, in the game this values are the up-arrow and the down-arrow
    The NN have as input 7 parameters
    1. The x coordenate of the obstacle
    2. The y coordenate of the obstacle
    3. The height of the obstacle 
    4. The width of the obstacle
    5. The x coordenate of the dino
    6. The y coordenate of the dino
    7. The velocity of the game 
    """

    global nn_layers, chromosome_len, nn_umbral

    def __init__(self, chromosome=None) -> None:
        self.score = 0
        self.chromosome = chromosome
        if type(chromosome) != Chromosome:
            self.chromosome = Chromosome()
        self.activation_function = leaky_relu
        self.final_fuction = sigmoid

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Agent):
            return __value.chromosome.get_sequence() == self.chromosome.get_sequence()
        return False

    def __hash__(self):
        data = []
        for gen in self.chromosome.get_sequence():
            data.append(tuple(gen.get_code()))
        data = tuple(data)
        return hash(data)

    def mute(self) -> None:
        self.chromosome.mute()

    def reproduce(self, other_agent):
        childern_chromosome = self.chromosome.mix(other_agent.chromosome)
        childern = Agent(childern_chromosome)
        return childern

    def predict(self, input: np.ndarray) -> np.ndarray:
        """1. The x coordenate of the obstacle
            2. The y coordenate of the obstacle
            3. The height of the obstacle 
            4. The width of the obstacle
            5. The x coordenate of the dino
            6. The y coordenate of the dino
            7. The velocity of the game 
        """
        # Normalize the input
        def normalize(value, min, max):
            return (value - min)/(max - min)

        mins = np.asarray([0, 0, 0, 0, 0, 0, 0])
        maxs = np.asarray([SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT,
                          SCREEN_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, 100])
        input = normalize(input, mins, maxs)
        # Calculate the first layer (after the input)
        layer1 = np.zeros(nn_layers[1])
        # Get the ponderation for each connection
        for gen in self.chromosome.get_sequence():
            code = gen.get_code()
            if code[0] == 0:  # The connection start from the input layer
                layer1[code[2]] += input[code[1]]*code[3]
        # Use the activation fuction
        layer1 = self.activation_function(layer1)

        # Calculate the next layer
        layer2 = np.zeros(nn_layers[2])
        # Get the ponderation for each connection
        for gen in self.chromosome.get_sequence():
            code = gen.get_code()
            if code[0] == 1:  # The connection start from the first layer
                layer2[code[2]] += layer1[code[1]]*code[3]
        # Use the activation fuction
        layer2 = self.final_fuction(layer2)

        output = [0 if value <= nn_umbral else 1 for value in layer2]
        return output
