from datetime import datetime

def get_input(prompt, default=None):
    """
    Helper function to get user input, with validation and default handling.
    """
    while True:
        value = input(prompt)
        if value.strip() == "" and default is not None:
            return default
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a number or leave blank to use the default.")

def compute_velocity_from_reynolds(Re, density, viscosity, Dh):
    """Compute velocity using Reynolds number, density, viscosity, and hydraulic diameter."""
    return (Re * viscosity) / (density * Dh)

def compute_velocity_from_mass_flow(mass_flow_rate, density, area):
    """Compute velocity using mass flow rate, density, and area."""
    return mass_flow_rate / (density * area)

# Function to calculate outlet temperature
def calculate_outlet_temperature():
    log = []  # List to accumulate log entries

    # Start logging input
    log.append(f"=== Mixing Calculation Log ===")
    log.append(f"Date & Time: {datetime.now()}\n")

    print("Enter properties for the first (cold) stream:")
    log.append("First Stream (Cold) Properties:")

    # Input for the first stream
    T_cold = get_input("Temperature (°C): ")
    viscosity_cold = get_input("Viscosity (kg/(m·s)): ")
    density_cold = get_input("Density (kg/m³): ")
    area_cold = get_input("Flow area (m²): ")
    Dh_cold = get_input("Hydraulic diameter (m): ")
    cp_cold = get_input("Specific heat capacity (Cp) (J/(kg·K)): ")

    # Log the inputs
    log.append(f"Temperature: {T_cold} °C")
    log.append(f"Viscosity: {viscosity_cold} kg/(m·s)")
    log.append(f"Density: {density_cold} kg/m³")
    log.append(f"Flow area: {area_cold} m²")
    log.append(f"Hydraulic diameter: {Dh_cold} m")
    log.append(f"Specific heat capacity (Cp): {cp_cold} J/(kg·K)")

    # Determine velocity for the first stream
    Re_known_cold = input("Is the Reynolds number known for the first stream? (y/n): ").strip().lower()
    if Re_known_cold == 'y':
        Re_cold = get_input("Reynolds number (Re): ")
        velocity_cold = compute_velocity_from_reynolds(Re_cold, density_cold, viscosity_cold, Dh_cold)
        log.append(f"Reynolds number (Re): {Re_cold}")
    else:
        mass_flow_rate_cold = get_input("Mass flow rate (kg/s): ")
        velocity_cold = compute_velocity_from_mass_flow(mass_flow_rate_cold, density_cold, area_cold)
        log.append(f"Mass flow rate: {mass_flow_rate_cold} kg/s")

    log.append(f"Velocity: {velocity_cold} m/s")

    # Calculate mass flow rate if not already provided
    mass_flow_rate_cold = density_cold * area_cold * velocity_cold

    # Convert temperature to Kelvin for calculations
    T_cold_K = T_cold + 273.15  

    print("\nEnter properties for the second (hot) stream. Press Enter to use the same value as the first stream.")
    log.append("\nSecond Stream (Hot) Properties:")

    # Input for the second stream with defaulting to first stream values
    T_hot = get_input("Temperature (°C): ", T_cold)
    viscosity_hot = get_input("Viscosity (kg/(m·s)): ", viscosity_cold)
    density_hot = get_input("Density (kg/m³): ", density_cold)
    area_hot = get_input("Flow area (m²): ", area_cold)
    Dh_hot = get_input("Hydraulic diameter (m): ", Dh_cold)
    cp_hot = get_input("Specific heat capacity (Cp) (J/(kg·K)): ", cp_cold)

    # Log the inputs
    log.append(f"Temperature: {T_hot} °C")
    log.append(f"Viscosity: {viscosity_hot} kg/(m·s)")
    log.append(f"Density: {density_hot} kg/m³")
    log.append(f"Flow area: {area_hot} m²")
    log.append(f"Hydraulic diameter: {Dh_hot} m")
    log.append(f"Specific heat capacity (Cp): {cp_hot} J/(kg·K)")

    # Determine velocity for the second stream
    Re_known_hot = input("Is the Reynolds number known for the second stream? (y/n, default: same as first): ").strip().lower()
    if Re_known_hot == 'y':
        Re_hot = get_input("Reynolds number (Re): ")
        velocity_hot = compute_velocity_from_reynolds(Re_hot, density_hot, viscosity_hot, Dh_hot)
        log.append(f"Reynolds number (Re): {Re_hot}")
    elif Re_known_hot == 'n':
        mass_flow_rate_hot = get_input("Mass flow rate (kg/s): ")
        velocity_hot = compute_velocity_from_mass_flow(mass_flow_rate_hot, density_hot, area_hot)
        log.append(f"Mass flow rate: {mass_flow_rate_hot} kg/s")
    else:
        velocity_hot = velocity_cold
        log.append("Using the same velocity as the first stream.")

    log.append(f"Velocity: {velocity_hot} m/s")

    # Calculate mass flow rate if not already provided
    mass_flow_rate_hot = density_hot * area_hot * velocity_hot

    # Convert temperature to Kelvin for calculations
    T_hot_K = T_hot + 273.15  

    # Energy balance for mixing with different specific heat capacities
    T_outlet_K = (mass_flow_rate_cold * cp_cold * T_cold_K + mass_flow_rate_hot * cp_hot * T_hot_K) / (mass_flow_rate_cold * cp_cold + mass_flow_rate_hot * cp_hot)
    T_outlet_C = T_outlet_K - 273.15  # Convert back to Celsius

    # Log and output results
    log.append("\nResults – Outlet Temperature")
    log.append(f"T outlet: {T_outlet_C:.2f} °C")
    log.append(f"T outlet: {T_outlet_K:.2f} K")

    print("\nResults – Outlet Temperature")
    print(f"T outlet: {T_outlet_C:.2f} °C")
    print(f"T outlet: {T_outlet_K:.2f} K")

    # Write log to a file
    with open("mixing_log.txt", "a") as log_file:
        log_file.write("\n".join(log) + "\n\n")
    print("\nCalculation log saved to 'mixing_log.txt'.")

if __name__ == "__main__":
    print("=== Mixing of Two Streams Calculator ===")
    calculate_outlet_temperature()
