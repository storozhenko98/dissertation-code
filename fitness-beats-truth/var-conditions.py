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

    return fitness_over_time

n_cycles = 10
n_time_points = 1000  # set this to a large enough number that it's greater than the length of any cycle
fitness_over_time_all = np.full((n_cycles, n_time_points * 2), np.nan)  # initialize 2D array with np.nan

for i in range(n_cycles):
    n_organisms = np.random.randint(50, 150)
    n_food = np.random.randint(500, 1500)
    n_predators = np.random.randint(250, 750)
    fitness_over_time = run_simulation(n_organisms, n_food, n_predators)
    fitness_over_time_all[i, :len(fitness_over_time)] = fitness_over_time  # fill in fitness values for this cycle
    #print which cycle out of which 
    print('Cycle {} out of {}'.format(i + 1, n_cycles))

average_fitness_over_time = np.nanmean(fitness_over_time_all, axis=0)  # take mean across all cycles for each time point, ignoring np.nan values

plt.plot(average_fitness_over_time[::2], label='Truth-seeing')
plt.plot(average_fitness_over_time[1::2], label='Fitness-seeing')
plt.xlabel('Time')
plt.ylabel('Average Fitness')
plt.legend()
plt.show()
