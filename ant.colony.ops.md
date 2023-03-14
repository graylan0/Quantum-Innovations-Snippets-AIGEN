```
import numpy as np

# Define parameters for the algorithm
num_ants = 10
num_iterations = 50
alpha = 1
beta = 2
rho = 0.5

# Define the problem and initialize pheromone trail
problem = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
pheromone = np.ones(problem.shape) / (problem.shape[0] * problem.shape[1])

# Run the Ant Colony Optimization algorithm
for iteration in range(num_iterations):
    # Initialize ant positions and visited flags
    ant_positions = np.zeros((num_ants, 2), dtype=int)
    visited_flags = np.zeros(problem.shape, dtype=bool)

    # Move the ants and update pheromone trail
    for ant_index in range(num_ants):
        current_position = ant_positions[ant_index]
        visited_flags[current_position[0], current_position[1]] = True

        # Choose the next position based on pheromone and heuristic information
        next_positions = []
        probabilities = []
        for i in range(problem.shape[0]):
            for j in range(problem.shape[1]):
                if not visited_flags[i, j]:
                    next_positions.append([i, j])
                    probabilities.append((pheromone[i, j] ** alpha) * (1 / problem[i, j] ** beta))
        probabilities = probabilities / np.sum(probabilities)
        chosen_position = next_positions[np.random.choice(len(next_positions), p=probabilities)]
        ant_positions[ant_index] = chosen_position

        # Update the pheromone trail based on the ants' paths
        for i in range(problem.shape[0]):
            for j in range(problem.shape[1]):
                if [i, j] in ant_positions:
                    pheromone[i, j] *= (1 - rho)
                    pheromone[i, j] += rho / (problem.shape[0] * problem.shape[1])

    # Print the best solution found so far
    best_solution = np.argmax(problem)
    best_solution_position = [best_solution // problem.shape[1], best_solution % problem.shape[1]]
    print("Iteration {}: Best solution: {}, Position: {}".format(iteration, problem[best_solution], best_solution_position))
```
