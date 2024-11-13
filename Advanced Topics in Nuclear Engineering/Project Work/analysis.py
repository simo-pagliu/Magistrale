import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

width = 5
height = 5

# Analytical solution for the Styblinski-Tang function minimum
analytical_solution = -78.33233

# Load the results data
def load_results(filename="parametric_test_results.csv"):
    return pd.read_csv(filename)

# Plot convergence time vs different parameters
def plot_convergence_time(results):
    plt.figure(figsize=(6, 4))
    sns.set_palette("Blues_d")    # Set blue color palette for markers
    sns.scatterplot(
        data=results, 
        x="population_size", 
        y="execution_time", 
        hue="mutation_probability", 
        style="crossover_probability", 
        s=70,          # Set marker size for visibility
        palette="Blues_d",
        alpha=0.8      # Adjust marker transparency for better readability
    )
    plt.title("Convergence Time vs Population Size\n(Color: Mutation Probability, Shape: Crossover Probability)")
    plt.xlabel("Population Size")
    plt.xticks(range(0, 201, 50))
    plt.xlim(25, 225)
    plt.ylabel("Execution Time (s)")

    # Adjust legend placement inside the plot in the top-left corner
    plt.legend(
        title="Legend:\n- Color: Mutation Probability\n- Shape: Crossover Probability", 
        loc='upper left', 
        bbox_to_anchor=(0.05, 0.95),  # Adjusted location within the plot
        borderaxespad=0.5,
        fontsize=9,
        title_fontsize=10
    )

    plt.tight_layout(pad=2)  # Add padding for aesthetics
    plt.show()

# Plot Final Fitness vs Mutation Probability
def plot_fitness_vs_mutation(results):
    plt.figure(figsize=(width, height))
    sns.set_palette("Blues")
    sns.boxplot(data=results, x="mutation_probability", y="final_fitness")
    plt.title("Final Fitness vs Mutation Probability")
    plt.xlabel("Mutation Probability")
    plt.ylabel("Final Fitness")
    plt.axhline(analytical_solution, linestyle="--", color="dodgerblue", label="Analytical Solution")
    
    legend_handles = [
        plt.Line2D([0], [0], color="dodgerblue", linestyle="--", label="Analytical Solution"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="black", markersize=6, label="Outliers"),
        plt.Line2D([0], [0], color="skyblue", lw=6, label="Interquartile Range (IQR)"),
        plt.Line2D([0], [0], color="black", lw=2, label="Median Line"),
    ]
    plt.legend(handles=legend_handles, loc='upper right', title="Legend")
    plt.figtext(0.5, -0.05, "Boxplots show median, quartiles, and outliers (⧫)", ha='center', color="gray")
    plt.show()

# Plot Final Fitness vs Crossover Probability
def plot_fitness_vs_crossover(results):
    plt.figure(figsize=(width, height))
    sns.set_palette("Blues")
    sns.boxplot(data=results, x="crossover_probability", y="final_fitness")
    plt.title("Final Fitness vs Crossover Probability")
    plt.xlabel("Crossover Probability")
    plt.ylabel("Final Fitness")
    plt.axhline(analytical_solution, linestyle="--", color="dodgerblue", label="Analytical Solution")
    
    legend_handles = [
        plt.Line2D([0], [0], color="dodgerblue", linestyle="--", label="Analytical Solution"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="black", markersize=6, label="Outliers"),
        plt.Line2D([0], [0], color="skyblue", lw=6, label="Interquartile Range (IQR)"),
        plt.Line2D([0], [0], color="black", lw=2, label="Median Line"),
    ]
    plt.legend(handles=legend_handles, loc='upper right', title="Legend")
    plt.figtext(0.5, -0.05, "Boxplots show median, quartiles, and outliers (⧫)", ha='center', color="gray")
    plt.show()

# Plot Final Fitness vs Population Size
def plot_fitness_vs_population_size(results):
    plt.figure(figsize=(width, height))
    sns.set_palette("Blues")
    boxplot = sns.boxplot(data=results, x="population_size", y="final_fitness", color="skyblue")
    plt.title("Final Fitness vs Initial Population Size")
    plt.xlabel("Population Size")
    plt.ylabel("Final Fitness")
    plt.axhline(analytical_solution, linestyle="--", color="dodgerblue", label="Analytical Solution")
    
    legend_handles = [
        plt.Line2D([0], [0], color="dodgerblue", linestyle="--", label="Analytical Solution"),
        plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="black", markersize=6, label="Outliers"),
        plt.Line2D([0], [0], color="skyblue", lw=6, label="Interquartile Range (IQR)"),
        plt.Line2D([0], [0], color="black", lw=2, label="Median Line"),
    ]
    plt.legend(handles=legend_handles, loc='upper right', title="Legend")

    # plt.figtext(0.5, -0.1, "Explanation:\n"
                            # "- Blue dotted line: Analytical solution for the global minimum\n"
                            # "- Outliers (⧫): Values outside 1.5 times the IQR from the quartiles\n"
                            # "- Interquartile Range (IQR): Contains the middle 50% of data\n"
                            # "- Median Line: The middle value within the IQR", ha='center', color="gray")
    plt.show()

# Main analysis function
def analyze_parametric_results(filename="parametric_test_results.csv"):
    results = load_results(filename)
    print(results.describe())   

    # Plot convergence time vs parameters
    plot_convergence_time(results)

    # Plot fitness vs mutation probability
    plot_fitness_vs_mutation(results)

    # Plot fitness vs crossover probability
    plot_fitness_vs_crossover(results)

    # Plot fitness vs population size
    plot_fitness_vs_population_size(results)

if __name__ == "__main__":
    analyze_parametric_results()
