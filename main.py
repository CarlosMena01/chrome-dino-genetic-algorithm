# Implement the simulation using genetic algorithms

import random
import numpy as np
from src.NN import Agent
from game import *
from utils.config import *
from datetime import date

path = "./data/"


def iteration(population, generation):
    # Run the simulation and asing the scores
    dinos = []
    for agent in population:
        dinos.append(Dinosaur(agent))
    dinos = main(dinos, generation)
    # Get again the agents
    for i, dino in enumerate(dinos):
        population[i] = dino.agent
    # Sort the agents based on their 'score' attribute in descending order
    population = sorted(population, key=lambda obj: obj.score, reverse=True)
    # Write in a file the best score genomes
    # extract current local date
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    file_name = f"{path}results_{today}.txt"
    with open(file_name, "a") as f:
        f.write(f"GENERATION {generation}\n")
        for agent in population:
            f.write(f"{agent.score} // {agent.chromosome.get_sequence()}\n")

    new_population = []
    # Reproduce to create the new population
    # The reproduction is random and can be just a copy, a mix, mute or combination
    # The random agents
    for _ in range(int(agents_len*random_percent/100)):
        new_population.append(Agent())
    # The copies
    for i in range(int(agents_len*copy_percent/100)):
        agent = Agent(population[i % 5].chromosome)
        new_population.append(agent)
    # The childrens
    for _ in range(int(agents_len*childrens_percent/100)):
        new_agent = population[random.randint(0, 2)]
        new_agent = new_agent.reproduce(population[random.randint(0, 2)])
        new_population.append(new_agent)
    # The mutations
    for _ in range(int(agents_len*muted_percent/100)):
        new_agent = population[random.randint(0, 2)]
        new_agent.mute()
        new_population.append(new_agent)
    # Others
    while len(new_population) < agents_len:
        new_agent = Agent()  # Start as a random agent
        # Can be remplaced by a good agent
        if random.choice([True, False]):
            new_agent = population[random.randint(0, 2)]
        # Make some mutations
        for _ in range(random.randint(0, 3)):
            new_agent.mute()
        # Make some mixes with random (but hight score) match
        for _ in range(random.randint(0, 3)):
            new_agent = new_agent.reproduce(population[random.randint(0, 2)])

        new_population.append(new_agent)

    return new_population


# Create the first population
population = [Agent() for _ in range(agents_len)]
for i in range(20):
    population = iteration(population, i+1)
