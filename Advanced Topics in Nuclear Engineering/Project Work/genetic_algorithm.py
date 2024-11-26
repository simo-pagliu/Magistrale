import random
import numpy as np
import matplotlib.pyplot as plt
import json
import time
import os
import struct
import pandas as pd  # To store results in a DataFrame for easy comparison
from concurrent.futures import ProcessPoolExecutor, as_completed

# Set working directory to the location of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

################################################################################
# FITNESS FUNCTION
# Define the Styblinski-Tang function to minimize
# Set the domain limits to -5 to 5 for both x and y
# The global minimum is at f(-2.903534, -2.903534) = -78.332
def styblinski_tang(x, y):
    return (x**4 - 16 * x**2 + 5 * x + y**4 - 16 * y**2 + 5 * y) / 2

limit = 5
################################################################################

################################################################################
# Probability based on fitness (for minimization)
# The probability is inversely proportional to the fitness value
# The higher the fitness, the lower the probability
def fitness_probability(set):
    fitness_values = [styblinski_tang(pair[0], pair[1]) for pair in set]
    if max(fitness_values) == min(fitness_values):
        probabilities = [1 / len(set)] * len(set)
    else:
        max_fitness = max(fitness_values)
        inverted_fitness = [(max_fitness - fitness) for fitness in fitness_values]
        total_inverted_fitness = sum(inverted_fitness)
        probabilities = [fit / total_inverted_fitness for fit in inverted_fitness]
    return probabilities
################################################################################

################################################################################
# Initialize Population
# Randomly initialize the population within the given domain limits
def initialize_population(population_size, x_min, x_max, y_min, y_max):
    return [[random.uniform(x_min, x_max), random.uniform(y_min, y_max)] for _ in range(population_size)]
################################################################################

################################################################################
# Selection
# Tournament selection is basically doing nothing as it keeps the # the same
# Roulette selection is reducing the population size
def tournament_selection(population, tournament_size):
    """Selects the best individual from a random subset of the population.
    Chooses the one with the highest fitness value."""
    selected_parents = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        probabilities = fitness_probability(tournament)
        selected = max(tournament, key=lambda x: probabilities[tournament.index(x)])
        selected_parents.append(selected)
    return selected_parents

def roulette_selection(population, tournament_size):
    """Selects the best individual from a random subset of the population.
    Based on a probability related to the fitness value."""
    selected_parents = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        probabilities = fitness_probability(tournament)
        selected = random.choices(tournament, weights=probabilities, k=1)[0]
        selected_parents.append(selected)
    return selected_parents
################################################################################

################################################################################
# Crossover
# Right now I'm replacing the parents with the children
# Is it correct? Should I append the children to the population?
def punnet_crossover(population, probability):
    """ Analogy to the Punnet Square.
    Performs crossover between two parents.
    Combines the x and y values of the parents to create two new children.
    Chosen by probability weighted on fitness."""
    crossed_over = population.copy()
    for _ in range(len(population) // 2):
        if random.random() < probability:
            indexes = random.sample(range(len(population)), 2)
            parent1, parent2 = population[indexes[0]], population[indexes[1]]
            children = [[parent1[0], parent2[1]], [parent2[0], parent1[1]], parent1, parent2]
            probabilities = fitness_probability(children)
            selected = random.choices(children, weights=probabilities, k=2)
            crossed_over[indexes[0]], crossed_over[indexes[1]] = selected
    return crossed_over

def bit_crossover(population, probability):
    """Crosses over a portion of the bits of the binary representation of the two parents."""
    crossed_over = population.copy()

    for _ in range(len(population) // 2):
        if random.random() < probability:
            # Select two random parents
            indexes = random.sample(range(len(population)), 2)
            parent1, parent2 = population[indexes[0]], population[indexes[1]]

            # Initialize new offspring
            offspring1, offspring2 = [], []

            for i in range(2):  # Loop over the two variables of the parents
                # Convert the current variable of the parents to binary
                binary1 = f"{struct.unpack('!I', struct.pack('!f', parent1[i]))[0]:032b}"
                binary2 = f"{struct.unpack('!I', struct.pack('!f', parent2[i]))[0]:032b}"

                # Randomly choose crossover points
                start = random.randint(0, 31)
                end = random.randint(start + 1, 32)

                # Perform crossover
                new_binary1 = binary1[:start] + binary2[start:end] + binary1[end:]
                new_binary2 = binary2[:start] + binary1[start:end] + binary2[end:]

                # Convert back to floats
                new_float1 = struct.unpack('!f', struct.pack('!I', int(new_binary1, 2)))[0]
                new_float2 = struct.unpack('!f', struct.pack('!I', int(new_binary2, 2)))[0]

                # Add to offspring
                offspring1.append(new_float1)
                offspring2.append(new_float2)

            # Update the population
            crossed_over[indexes[0]] = offspring1
            crossed_over[indexes[1]] = offspring2

    return crossed_over
################################################################################

################################################################################
# Mutation
# Right now I'm replacing the parents with the children
# Is it correct? Should I append the children to the population?
def redefine_mutation(population, probability):
    """ Randomly redifines the x and y values, indipendently."""
    mutated = population.copy()
    for i in range(len(population)):
        # Mutate x
        if random.random() < probability:
            mutated[i] = [random.uniform(-limit, limit), population[i][1]]
        # Mutate y
        if random.random() < probability:
            mutated[i] = [population[i][0], random.uniform(-limit, limit)]
    return mutated

def bit_mutation(population, probability):
    """
    Randomly flips a bit in the binary representation of the gene.
    Each bit flip is determined by the given probability.
    """
    mutated = population.copy()
    for i in range(len(population)):
        if random.random() < probability:
            # Apply mutation for each gene in the individual
            for j in range(len(population[i])):
                value = population[i][j]
                
                # Convert the float to its binary representation as an integer
                packed_value = struct.unpack('!I', struct.pack('!f', value))[0]
                
                # Choose a random bit to flip
                bit_index = random.randint(0, 31)
                
                # Flip the specified bit using XOR
                flipped_value = packed_value ^ (1 << bit_index)
                
                # Convert back to float
                mutated[i][j] = struct.unpack('!f', struct.pack('!I', flipped_value))[0]
    return mutated
################################################################################

################################################################################
# Save and Load State
def save_state(population, avg_fitness_history, filename="ga_state.json"):
    state = {
        "population": population,
        "avg_fitness_history": avg_fitness_history
    }
    with open(filename, "w") as f:
        json.dump(state, f)
    print("State saved to", filename)

def load_state(filename=f"ga_state.json"):
    with open(filename, "r") as f:
        state = json.load(f)
    print("State loaded from", filename)
    return state["population"], state["avg_fitness_history"]
################################################################################

################################################################################
# Genetic Algorithm
def GA_loop(max_iterations, initial_population_size, probability_of_crossover,
              probability_of_mutation, tournament_fraction,
              selection, crossover, mutation,
              plot_enabled, load_previous, save_enabled, print_result, log):
    
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
    converged = False
    for iteration in range(max_iterations):
        tournament_size = max(2, int(tournament_fraction * len(population)))
        population = selection(population, tournament_size)
        population = crossover(population, probability_of_crossover)
        population = mutation(population, probability_of_mutation)

        # Check for any NaN values and remove them
        population = [pair for pair in population if not any(np.isnan(gene) for gene in pair)]

        # Track average fitness
        fitness_values = [styblinski_tang(pair[0], pair[1]) for pair in population]
        avg_fitness = sum(fitness_values) / len(fitness_values)
        avg_fitness_history.append(avg_fitness)
        
        # Update plot if enabled
        if plot_enabled:
            line.set_xdata(range(len(avg_fitness_history)))
            line.set_ydata(avg_fitness_history)
            ax.set_xlim(0, max(len(avg_fitness_history), max_iterations))
            fig.canvas.draw()  # Redraw the figure
            fig.canvas.flush_events()  # Process the events
            plt.pause(0.01)

        # Convergence check
        if len(avg_fitness_history) > 1 and abs(avg_fitness_history[-1] - avg_fitness_history[-2]) < 0.001 or len(population) == 1:
            print(f"\033[92mConverged after {iteration + 1} iterations.\033[0m")
            convergence_string = f"CONVERGED @ {iteration + 1}"
            converged = True
            break
    
    if not converged:
        residuals = []
        for i in range(len(avg_fitness_history)):
            residuals.append(abs(avg_fitness_history[i] - avg_fitness_history[i-1]))
        residual = sum(residuals) / len(residuals)
        print(f"\033[93mStopped after reaching the maximum number of iterations without reaching convergence, avg residual is {residual}.\033[0m")
        convergence_string = f"MAXED @ {residual}"

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
    
    if print_result:
        print(f"Best solution: {best_solution}")
        print(f"Best fitness: {best_fitness}")

    # Logging best result if enabled
    if log:
        log_file = "genetic_algotithm.log"
        with open(log_file, "a") as f:
            selections = "Tournament" if selection == tournament_selection else "Roulette"
            crossovers = "Punnet" if crossover == punnet_crossover else "Bit"
            mutations = "Redefine" if mutation == redefine_mutation else "Bit"
            method = f"{selections} - {crossovers} - {mutations}"
            stats = f"I: {max_iterations}, Pop: {initial_population_size}, P_CS: {probability_of_crossover}, P_M: {probability_of_mutation}, P_S: {tournament_fraction}" 
            results = f"Result: {best_fitness} @ x: {best_solution[0]} y: {best_solution[1]}"
            f.write(f"{method}, {stats}, {results}, {convergence_string}\n")
        print(f"Results logged in {log_file}")

    # Return performance metrics
    return {
        "iterations": iteration + 1,
        "final_fitness": best_fitness,
        "best_solution": best_solution,
    }
################################################################################

################################################################################
# Parallel GA_loop with Optional Population Division
def run_ga_loop_partition(params):
    """Wrapper function to run GA_loop on a partition of the population."""
    partition, max_iterations, probability_of_crossover, probability_of_mutation, tournament_frac, selection, crossover, mutation = params
    return GA_loop(
        max_iterations=max_iterations,
        initial_population_size=len(partition),
        probability_of_crossover=probability_of_crossover,
        probability_of_mutation=probability_of_mutation,
        tournament_fraction=tournament_frac,
        selection=selection,
        crossover=crossover,
        mutation=mutation,
        plot_enabled=False,
        log=False
    )

def parallel_ga_loop(population, max_iterations, probability_of_crossover,
                     probability_of_mutation, tournament_frac, selection, crossover, mutation,
                     divide_population=False):
    """Runs GA_loop in parallel or processes population in a single process based on a flag."""
    if divide_population:
        # Divide population across multiple processes
        num_cores = os.cpu_count() or 1
        partition_size = len(population) // num_cores
        partitions = [
            population[i * partition_size:(i + 1) * partition_size] for i in range(num_cores)
        ]
        if len(population) % num_cores != 0:
            partitions[-1].extend(population[num_cores * partition_size:])

        params_list = [
            (partition, max_iterations, probability_of_crossover, probability_of_mutation, tournament_frac, selection, crossover, mutation)
            for partition in partitions
        ]

        results = []
        print("Running with population division across multiple processes...")
        start_time = time.time()

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(run_ga_loop_partition, params) for params in params_list]
            for future in as_completed(futures):
                results.append(future.result())

        end_time = time.time()
        print(f"Total time taken with population division: {end_time - start_time:.2f} seconds")

        # Combine results from all partitions
        combined_population = []
        for result in results:
            combined_population.extend(result["best_solution"])  # Assuming best_solution is a list

        return combined_population

    else:
        # Process entire population in a single process
        print("Running on a single process without population division...")
        return GA_loop(
            max_iterations=max_iterations,
            initial_population_size=len(population),
            probability_of_crossover=probability_of_crossover,
            probability_of_mutation=probability_of_mutation,
            tournament_fraction=tournament_frac,
            selection=selection,
            crossover=crossover,
            mutation=mutation,
            plot_enabled=False,
            log=True
        )
################################################################################

################################################################################
# Main Function
if __name__ == "__main__":
    run_type = "loop"  # Set to "single" for a single run or "parametric" for a parametric test or "loop" for looping the single test
    divide_population = False  # Set to True to divide population into multiple processes

    if run_type == "single":
        ################################################################################################
        # Single Run
        ################################################################################################
        initial_population_size = 200  # Initialize a population
        max_iterations = 100
        crossover_prob = 0.7
        mutation_prob = 0.1
        tournament_frac = 0.3
        selection = tournament_selection  # Replace with your selection function # Options: tournament_selection, roulette_selection
        crossover = punnet_crossover  # Replace with your crossover function # Options: punnet_crossover, bit_crossover
        mutation = redefine_mutation  # Replace with your mutation function # Options: redefine_mutation, bit_mutation

        # Run GA with or without population division
        final_population = GA_loop(
            max_iterations, initial_population_size, crossover_prob, mutation_prob, tournament_frac,
            selection, crossover, mutation,
            plot_enabled=True, load_previous=False, save_enabled=False, print_result=True, log = False
        )  
    elif run_type == "loop":
        ################################################################################################
        # Loop over a single run
        ################################################################################################
        loop_iterations = 250
        initial_population_size = 200  # Initialize a population
        max_iterations = 100
        crossover_prob = 0.7
        mutation_prob = 0.1
        tournament_frac = 0.3
        selection = tournament_selection  # Replace with your selection function # Options: tournament_selection, roulette_selection
        crossover = punnet_crossover  # Replace with your crossover function # Options: punnet_crossover, bit_crossover
        mutation = redefine_mutation  # Replace with your mutation function # Options: redefine_mutation, bit_mutation

        # Run GA with or without population division
        for i in range(loop_iterations):
            final_population = GA_loop(
                max_iterations, initial_population_size, crossover_prob, mutation_prob, tournament_frac,
                selection, crossover, mutation,
                plot_enabled=False, load_previous=False, save_enabled=False, print_result=True, log = True
            )  
    elif run_type == "parametric":
        ################################################################################################
        # Parametric Test
        ################################################################################################
        max_iterations = 100

        param_combinations = [
            (initialize_population(200, -limit, limit, -limit, limit), max_iterations, crossover_prob, mutation_prob, tournament_frac, selection_fun, crossover_fun, mutation_fun)
            for crossover_prob in [0.2, 0.6, 0.8]
            for mutation_prob in [0.2, 0.6, 0.8]
            for tournament_frac in [0.2, 0.6, 0.8]
            for selection_fun in [tournament_selection, roulette_selection]
            for crossover_fun in [punnet_crossover, bit_crossover]
            for mutation_fun in [redefine_mutation, bit_mutation]
        ]

        results = []

        print("Running parametric test in parallel for parameter combinations...")
        start_time = time.time()

        # Run parametric tests in parallel
        with ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(parallel_ga_loop, population, max_iterations, crossover_prob, mutation_prob, tournament_frac, selection, crossover, mutation, divide_population=False)
                for (population, max_iterations, crossover_prob, mutation_prob, tournament_frac, selection, crossover, mutation) in param_combinations
            ]
            for future in as_completed(futures):
                results.append(future.result())

        end_time = time.time()
        print(f"Parametric test completed in {end_time - start_time:.2f} seconds.")

        # Save and display results
        results_df = pd.DataFrame(results)
        results_df.to_csv("parametric_test_results.csv", index=False)
        print("Parametric test results saved to 'parametric_test_results.csv'.")
################################################################################