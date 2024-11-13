import random
import numpy as np
import matplotlib.pyplot as plt
import json
import time
import pandas as pd  # To store results in a DataFrame for easy comparison
from concurrent.futures import ProcessPoolExecutor, as_completed

################################################################################
# FITNESS FUNCTION
# Define the Styblinski-Tang function to minimize
# Set the domain limits to -5 to 5 for both x and y
# The global minimum is at f(-2.903534, -2.903534) = -78.332
################################################################################
def styblinski_tang(x, y):
    return (x**4 - 16 * x**2 + 5 * x + y**4 - 16 * y**2 + 5 * y) / 2

limit = 5

################################################################################
# Probability based on fitness (for minimization)
# The probability is inversely proportional to the fitness value
# The higher the fitness, the lower the probability
################################################################################
def fitness_probability(set):
    fitness_values = [styblinski_tang(pair[0], pair[1]) for pair in set]
    if max(fitness_values) == min(fitness_values):
        probabilities = [1 / len(set)] * len(set)
    else:
        max_fitness = max(fitness_values)
        inverted_fitness = [(max_fitness - fitness) for fitness in fitness_values]
        total_inverted_fitness = sum(inverted_fitness) + 1e-10
        probabilities = [fit / total_inverted_fitness for fit in inverted_fitness]
    return probabilities

################################################################################
# Initialize Population
# Randomly initialize the population within the given domain limits
################################################################################
def initialize_population(population_size, x_min, x_max, y_min, y_max):
    return [[random.uniform(x_min, x_max), random.uniform(y_min, y_max)] for _ in range(population_size)]

################################################################################
# Tournament Selection
################################################################################
def tournament_selection(population, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        probabilities = fitness_probability(tournament)
        selected = random.choices(tournament, weights=probabilities, k=1)[0]
        selected_parents.append(selected)
    return selected_parents

################################################################################
# Crossover Operation
################################################################################
def crossover_1(population, probability):
    crossed_over = population.copy()
    for i in range(len(population) // 2):
        if random.random() < probability:
            indexes = random.sample(range(len(population)), 2)
            parent1, parent2 = population[indexes[0]], population[indexes[1]]
            children = [[parent1[0], parent2[1]], [parent2[0], parent1[1]], parent1, parent2]
            probabilities = fitness_probability(children)
            selected = random.choices(children, weights=probabilities, k=2)
            crossed_over[indexes[0]], crossed_over[indexes[1]] = selected
    return crossed_over

################################################################################
# Mutation Operation
################################################################################
def mutation_1(population, probability):
    mutated = population.copy()
    for i in range(len(population)):
        if random.random() < probability:
            mutated[i] = [random.uniform(-limit, limit), random.uniform(-limit, limit)]
    return mutated

################################################################################
# Save and Load State
################################################################################
# Save the current state of the genetic algorithm
def save_state(population, avg_fitness_history, filename="ga_state.json"):
    state = {
        "population": population,
        "avg_fitness_history": avg_fitness_history
    }
    with open(filename, "w") as f:
        json.dump(state, f)
    print("State saved to", filename)

# Function to load the saved state
def load_state(filename=f"ga_state.json"):
    with open(filename, "r") as f:
        state = json.load(f)
    print("State loaded from", filename)
    return state["population"], state["avg_fitness_history"]

################################################################################
# Genetic Algorithm Loop Test
################################################################################
def GA_loop(max_iterations, initial_population_size=100, probability_of_crossover=0.7,
              probability_of_mutation=0.1, tournament_fraction=0.3,
              plot_enabled=False, load_previous=False, save_enabled=False):
    
    # Initialization
    if load_previous:
        population, avg_fitness_history = load_state()
    else:
        population = initialize_population(initial_population_size, -limit, limit, -limit, limit)
        avg_fitness_history = []

    # Initialize plot if enabled
    if plot_enabled:
        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 6))
        line, = ax.plot([], [], label="Average Fitness", color="orange")
        ax.set_xlim(0, max_iterations)
        ax.set_ylim(-80, 0)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Average Fitness")
        ax.set_title("Convergence of Average Fitness Over Iterations")
        ax.legend()
            
    # Main loop
    for iteration in range(max_iterations):
        tournament_size = max(2, int(tournament_fraction * len(population)))
        population = tournament_selection(population, tournament_size)
        population = crossover_1(population, probability_of_crossover)
        population = mutation_1(population, probability_of_mutation)
        

        # Track average fitness
        fitness_values = [styblinski_tang(pair[0], pair[1]) for pair in population]
        avg_fitness = sum(fitness_values) / len(fitness_values)
        avg_fitness_history.append(avg_fitness)
        
        # Update plot if enabled
        if plot_enabled:
            line.set_xdata(range(len(avg_fitness_history)))
            line.set_ydata(avg_fitness_history)
            ax.set_xlim(0, len(avg_fitness_history))
            plt.pause(0.01)

        # Convergence check
        if len(avg_fitness_history) > 1 and abs(avg_fitness_history[-1] - avg_fitness_history[-2]) < 0.001:
            break

    # Get final result
    best_solution = min(population, key=lambda x: styblinski_tang(x[0], x[1]))
    best_fitness = styblinski_tang(best_solution[0], best_solution[1])
    
    # Closing plot if enabled
    if plot_enabled:
        plt.ioff()
        plt.show()

    # Save state if enabled
    if save_enabled:
        save_state(population, avg_fitness_history)
        
    # Return performance metrics
    return {
        "iterations": iteration + 1,
        "final_fitness": best_fitness,
        "best_solution": best_solution,
    }

################################################################################
# Wrapper function to run GA_loop with parameters and capture execution time
################################################################################
def run_single_test(params):
    pop_size, mutation_prob, crossover_prob, tournament_frac, max_iterations = params
    start_time = time.time()
    result = GA_loop(
        max_iterations=max_iterations,
        initial_population_size=pop_size,
        probability_of_crossover=crossover_prob,
        probability_of_mutation=mutation_prob,
        tournament_fraction=tournament_frac,
        plot_enabled=False
    )
    end_time = time.time()
    
    # Add parameters and execution time to the result
    result["population_size"] = pop_size
    result["mutation_probability"] = mutation_prob
    result["crossover_probability"] = crossover_prob
    result["tournament_fraction"] = tournament_frac
    result["execution_time"] = end_time - start_time
    return result

################################################################################
# Parametric test function with parallel execution
################################################################################
def parametric_test(population_sizes, mutation_probs, crossover_probs, tournament_fractions, max_iterations):
    # Generate all parameter combinations
    param_combinations = [
        (pop_size, mutation_prob, crossover_prob, tournament_frac, max_iterations)
        for pop_size in population_sizes
        for mutation_prob in mutation_probs
        for crossover_prob in crossover_probs
        for tournament_frac in tournament_fractions
    ]

    # Results list to store each run’s result
    results = []

    # Run tests in parallel
    with ProcessPoolExecutor() as executor:
        # Submit all parameter combinations to the executor
        futures = [executor.submit(run_single_test, params) for params in param_combinations]

        # Collect results as they complete
        for future in as_completed(futures):
            results.append(future.result())

    # Convert results to a DataFrame and display
    results_df = pd.DataFrame(results)
    results_df.to_csv("parametric_test_results.csv", index=False)  # Save to CSV for further analysis


################################################################################
# Run the main function
################################################################################
if __name__ == "__main__": 
    # First look
    tic = time.time()
    parametric_test(
        population_sizes=[50, 100, 150, 200],
        mutation_probs=[0.2, 0.6, 0.8],
        crossover_probs=[0.2, 0.6, 0.8],
        tournament_fractions=[0.2, 0.6, 0.8],
        max_iterations=200
    )
    toc = time.time()
    print("Total time taken:", toc - tic, "seconds")
    
    # In depth look
    # parametric_test(
    #     population_sizes=[200],
    #     mutation_probs=[0, 0.2, 0.4, 0.6, 0.8, 1],
    #     crossover_probs=[0, 0.2, 0.4, 0.6, 0.8, 1],
    #     tournament_fractions=[0, 0.2, 0.4, 0.6, 0.8, 1],
    #     max_iterations=500
    # )
    
    # GA_loop(
    #     max_iterations = 100, 
    #     initial_population_size=100, 
    #     probability_of_crossover=0.7,
    #     probability_of_mutation=0.1, 
    #     tournament_fraction=0.3,
    #     plot_enabled=False, 
    #     load_previous=False, 
    #     save_enabled=False
    # )