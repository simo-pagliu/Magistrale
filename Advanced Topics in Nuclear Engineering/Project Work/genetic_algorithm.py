import random

# Define the Styblinski-Tang function to minimize
def styblinski_tang(x, y):
    return (x**4 - 16 * x**2 + 5 * x + y**4 - 16 * y**2 + 5 * y) / 2

limit = 5

########################################
# Probability based on fitness
########################################
def fitness_probability(set):
    fitness_values = [styblinski_tang(pair[0], pair[1]) for pair in set]

    # Check if all fitness values are identical
    if max(fitness_values) == min(fitness_values):
        # If all are identical, assign equal probabilities
        probabilities = [1 / len(set)] * len(set)
    else:
        # Invert fitness for minimization
        max_fitness = max(fitness_values)
        inverted_fitness = [(max_fitness - fitness) for fitness in fitness_values]
        total_inverted_fitness = sum(inverted_fitness) + 1e-10  # Avoid division by zero
        probabilities = [fit / total_inverted_fitness for fit in inverted_fitness]

    return probabilities

########################################
# Debug function
########################################
def debug(old_pop, new_pop):
    fitness_values_old = [styblinski_tang(pair[0], pair[1]) for pair in old_pop]
    fitness_values_new = [styblinski_tang(pair[0], pair[1]) for pair in new_pop]
    
    avg_fitness_old = sum(fitness_values_old) / len(fitness_values_old)
    avg_fitness_new = sum(fitness_values_new) / len(fitness_values_new)
    
    change = (avg_fitness_new - avg_fitness_old) / avg_fitness_old * 100
    
    print(f"Change: {change:.2f}%, Average Fitness: {avg_fitness_new:.2f}", end="\r")

########################################
# Initialize Population
########################################
def initialize_population(population_size, x_min, x_max, y_min, y_max):
    return [[random.uniform(x_min, x_max), random.uniform(y_min, y_max)] for _ in range(population_size)]

########################################
# Tournament Selection
########################################
def tournament_selection(population, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        probabilities = fitness_probability(tournament)
        selected = random.choices(tournament, weights=probabilities, k=1)[0]
        selected_parents.append(selected)
    
    return selected_parents

########################################
# Crossover Operation
########################################
def crossover_1(population, probability):
    crossed_over = population.copy()
    for i in range(len(population) // 2):
        if random.random() < probability:
            indexes = random.sample(range(len(population)), 2)
            parent1, parent2 = population[indexes[0]], population[indexes[1]]
            
            children = [
                [parent1[0], parent2[1]],
                [parent2[0], parent1[1]],
                parent1,
                parent2
            ]
            
            probabilities = fitness_probability(children)
            selected = random.choices(children, weights=probabilities, k=2)
            crossed_over[indexes[0]], crossed_over[indexes[1]] = selected
            
    return crossed_over

########################################
# Mutation Operation
########################################
def mutation_1(population, probability):
    mutated = population.copy()
    for i in range(len(population)):
        if random.random() < probability:
            mutated[i] = [random.uniform(-limit, limit), random.uniform(-limit, limit)]
    return mutated

########################################
# Finite Loop Test
########################################
def loop_test():
    initial_population_size = 100  # INPUT
    probability_of_crossover = 0.7 # INPUT
    probability_of_mutation = 0.1 # INPUT
    tournament_fraction = 0.3 # INPUT
    max_iterations = 1000 # INPUT
    
    population = initialize_population(initial_population_size, -limit, limit, -limit, limit)
    
    j = 0
    for _ in range(max_iterations):
        j += 1
        population_old = population.copy()
        
        tournament_size = max(2, int(tournament_fraction * len(population)))
        population = tournament_selection(population, tournament_size)
        population = crossover_1(population, probability_of_crossover)
        population = mutation_1(population, probability_of_mutation)
        
        debug(population_old, population)
        
        if len(population) <= 2:
            break

    best_solution = min(population, key=lambda x: styblinski_tang(x[0], x[1]))
    best_fitness = styblinski_tang(best_solution[0], best_solution[1])
    print(f"\nBest Solution: {best_solution} --> MIN: {best_fitness:.5f}")
    print("Expected Solution from analytical analysis: [-2.903534, -2.903534]")

def plot_it():
    import numpy as np
    import matplotlib.pyplot as plt
    # plot the function
    x = np.linspace(-limit, limit, 100)
    y = np.linspace(-limit, limit, 100)
    X, Y = np.meshgrid(x, y)
    Z = styblinski_tang(X, Y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    plt.show()
    
########################################
# Run the Test
########################################
if __name__ == "__main__":
    loop_test()
    plot_it()