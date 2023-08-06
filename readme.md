# Genetic Algorithm-Based Neural Network for Dino Runner AI

This project implements a genetic algorithm to evolve neural networks for playing the Chrome Dino runner game. The goal is to train agents that can navigate obstacles and achieve high scores in the game.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Overview

In this project, I aim to delve into the world of genetic algorithms by crafting a neural network (NN) from scratch using Python. The focus is on harnessing genetic algorithms to nurture agents that progressively enhance their performance over time. A genetic algorithm unfolds through a sequence of steps, constituting a machine learning process:

1. **Initial Solution:** We start with an initial solution, often a random one.
2. **Evaluation and Scoring:** The solution is put to the test, and its performance is assessed, resulting in a corresponding score.
3. **Selection and Reproduction:** Agents with the most favorable scores are chosen as parents and used to generate offspring through reproduction.
4. **Mutation:** These offspring undergo controlled mutations, introducing subtle variations to explore new possibilities.
5. **Iteration:** This cycle of selection, reproduction, and mutation is repeated iteratively, refining the solutions.

By traversing these steps, we harness the power of genetic algorithms to navigate the solution space and iteratively converge towards optimal or near-optimal solutions. This approach serves as a robust mechanism to tackle complex problems and uncover optimal strategies.

## Features

This project consists of three essential components:

### The Game

The `game.py` file contains a version of the Chrome Dino Runner game, developed using PyGame. This game serves as the environment in which the evolved agents will demonstrate their decision-making skills.

### The Machine Learning Algorithms

The core of the project resides in the `src/NN.py` file. The implementation centers around genetic algorithms and is structured using three main classes:

1. **Gen Class:** This class encapsulates a connection within a neural network. Each instance of Gen represents a connection with four attributes: start layer, departure neuron, arrival neuron, and the weight of the connection.

2. **Chromosome Class:** Chromosome is a collection of 24 Gen instances. It supports mixing two objects of this class and introducing mutations to the Gen instances.

3. **Agent Class:** The Agent class serves as the public face of the project. An Agent is capable of making decisions, undergoing mutations to introduce randomness into the population, and reproducing with another Agent to create offspring.

### The Simulation

In the `main.py` file, the logic for population selection is orchestrated. The simulation follows these steps:

1. Initiate a random population.
2. Run the game with this population and assign scores.
3. Create a new population, comprising a mix of random agents, offspring from the best-performing agents, copies of the best-performing agents, and mutated versions of top players.

This simulation process, driven by genetic algorithms, guides the evolution of the agents' decision-making abilities over successive generations.

## Getting Started

Follow these steps to set up and run the project:

1. Clone this repository:
   ```
   git clone https://github.com/CarlosMena01/chrome-dino-genetic-algorithm.git
   ```
2. Create a virtual environment (recommended for isolating dependencies):

- For Linux:

  ```
  python -m venv venv
  source venv/bin/activate
  ```

- For Windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the main script:
   ```
   python main.py
   ```

## Configuration

You can configurete some parameters of the project from the `utils/config.py` file.

## Results

---
