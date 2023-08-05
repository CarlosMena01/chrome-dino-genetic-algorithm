# Implement the simulation using genetic algorithms

import random
import numpy as np
from src.NN import Agent
from game import *

agents_len = 100


def iteration(population):
    # Run the simulation and asing the scores
    # TODO implement the simulation
    print("Start the simulation")
    dinos = []
    for agent in population:
        dinos.append(Dinosaur(agent))
    dinos = main(dinos)
    print("End simulation")
    # Get again the agents
    for i, dino in enumerate(dinos):
        population[i] = dino.agent
    # Sort the agents based on their 'score' attribute in descending order
    population = sorted(population, key=lambda obj: obj.score, reverse=True)
    new_population = []
    # Reproduce to create the new population
    # The reproduction is random and can be just a copy, a mix, mute or combination
    for _ in range(agents_len):
        new_agent = Agent()  # Start as a random agent
        # Can be remplaced by a good agent
        if random.choice([True, False]):
            new_agent = population[random.randint(0, 2)]
        # Make some mutations
        for _ in range(random.randint(0, 3)):
            new_agent.mute()
        # Make some mixes with random (but hight score) match
        for _ in range(random.randint(0, 3)):
            new_agent.reproduce(population[random.randint(0, 4)])
        new_population.append(new_agent)

    return new_population


# Create the first population
population = [Agent() for _ in range(agents_len)]
for _ in range(20):
    population = iteration(population)
