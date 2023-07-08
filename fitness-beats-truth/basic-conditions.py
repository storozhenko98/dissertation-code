import numpy as np
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, n_food, n_predators):
        self.food = np.random.rand(n_food, 2)
        self.predators = np.random.rand(n_predators, 2)

class Organism:
    def __init__(self, position, truth_seeing):
        self.position = position
        self.truth_seeing = truth_seeing
        self.fitness = 0

    def perceive(self, environment):
        # Fitness-seeing organisms ignore predators
        if not self.truth_seeing:
            return environment.food
        else:
            return np.concatenate((environment.food, environment.predators))

    def act(self, environment):
        perceived_entities = self.perceive(environment)
        if perceived_entities.size == 0:
            return
        closest_entity = min(perceived_entities, key=lambda x: np.linalg.norm(x - self.position))
        self.move_towards(closest_entity)
        self.interact_with_environment(environment)

    def move_towards(self, position):
        self.position = position

    def interact_with_environment(self, environment):
        for i, food in enumerate(environment.food):
            if np.all(food == self.position):
                self.fitness += 1
                environment.food = np.delete(environment.food, i, axis=0)
                return
        for i, predator in enumerate(environment.predators):
            if np.all(predator == self.position):
                self.fitness -= 1
                environment.predators = np.delete(environment.predators, i, axis=0)
                return

def run_simulation(n_organisms, n_food, n_predators):
    environment = Environment(n_food, n_predators)
    organisms = [Organism(np.random.rand(2), i % 2 == 0) for i in range(n_organisms)]
    fitness_over_time = []

    while len(environment.food) > 0 and len(organisms) > 0:
        for organism in organisms:
            organism.act(environment)
        fitness_over_time.append(np.mean([o.fitness for o in organisms if o.truth_seeing]))
        fitness_over_time.append(np.mean([o.fitness for o in organisms if not o.truth_seeing]))
        organisms = [o for o in organisms if o.fitness >= 0]

    plt.plot(fitness_over_time[::2], label='Truth-seeing')
    plt.plot(fitness_over_time[1::2], label='Fitness-seeing')
    plt.xlabel('Time')
    plt.ylabel('Average Fitness')
    plt.legend()
    plt.show()

run_simulation(n_organisms=100, n_food=1000, n_predators=500)
