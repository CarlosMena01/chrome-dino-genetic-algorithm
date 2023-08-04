# Implement the simulation using genetic algorithms

import random
import numpy as np
from src.NN import Agent

agents_len = 1000


def iteration(population):
    # Run the simulation and asing the scores
    # TODO implement the simulation

    for agent in population:
        for _ in range(100):
            pred = agent.predict(np.asarray(
                [random.random()*6 - 3 for _ in range(6)]))
            agent.score += sum(pred)
    for agent in population[:4]:
        print(agent.score)
    print("FINISH")

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
iteration(population)
