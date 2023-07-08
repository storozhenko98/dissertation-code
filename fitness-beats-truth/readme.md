In my endeavor to model Donald Hoffman's "Fitness Beats Truth" hypothesis, I developed a Python simulation to abstractly represent the competition between organisms that perceive the world as it is (truth-seeing) and organisms that perceive only what is necessary for survival (fitness-seeing). This simulation represents an artificial environment where these organisms interact with food and predator entities.

The simulation is structured around two key constructs: `Environment` and `Organism`.

The `Environment` class encapsulates the state of the world in which the organisms exist. It consists of two-dimensional positions of food and predator entities, which are initialized as random coordinates.

The `Organism` class represents an individual organism in this environment. Each organism is characterized by its position, a truth-seeing attribute that indicates its perception mode, and a fitness score. The organisms are designed to perceive their environment, move based on this perception, and interact with the environment.

The perception mode plays a pivotal role in this simulation. Fitness-seeing organisms are oblivious to the predators and perceive only the food, while truth-seeing organisms perceive both food and predators. This difference in perception influences their subsequent actions and interactions with the environment.

The core of the simulation is the `run_simulation` function. It creates the environment and a set of organisms, half of which are truth-seeing and the other half fitness-seeing. The simulation proceeds in a loop, iterating until all the food is consumed or all organisms are eliminated by predators. Within each iteration, each organism acts according to its perception of the environment. The average fitness scores of the truth-seeing and fitness-seeing organisms are computed and recorded at each time step. Organisms with a non-positive fitness score are removed from the simulation, symbolizing their death.

Once the simulation concludes, I plot the average fitness scores of both organism types over time. The x-axis represents the simulation time in terms of iterations, and the y-axis represents the average fitness score at each time step. Two lines are plotted: one for the truth-seeing organisms and the other for the fitness-seeing organisms.

While the real world is significantly more complex, this simulation provides an insightful representation of the principles behind the "Fitness Beats Truth" hypothesis. As suggested by Hoffman himself, the evolutionary advantage of fitness-seeing organisms over their truth-seeing counterparts has been demonstrated in various simulations, indicating the potential realism and applicability of this simplified model. It is, however, essential to remember that the results of this simulation heavily depend on the specific parameters and initial conditions provided. To address the role initial conditions may have, check out `var-conditions.py` file, which simulates the same environment with different initial conditions for as many cycles as specified.

-Storozhenko, July 8, 2023