from datetime import datetime

def get_input(prompt, allow_empty=False):
    """
    Helper function to get user input, with validation.
    """
    while True:
        value = input(prompt)
        if allow_empty and value.strip() == "":
            return None
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a number or leave blank.")

def compute_missing_values():
    log = []  # List to accumulate log entries

    # Start logging input
    log.append(f"=== Fluid Flow Computation Log ===")
    log.append(f"Date & Time: {datetime.now()}\n")

    # Always known quantities
    density = get_input("Enter density (kg/m³, default 1.225): ", allow_empty=True) or 1.225
    viscosity = get_input("Enter viscosity (kg/m·s, default 1.789e-5): ", allow_empty=True) or 1.789e-5
    Area = get_input("Enter area (m²): ")
    Wetted_perimeter = get_input("Enter wetted perimeter (m): ")

    # Log the known quantities
    log.append(f"Density: {density} kg/m³")
    log.append(f"Viscosity: {viscosity} kg/m·s")
    log.append(f"Area: {Area} m²")
    log.append(f"Wetted perimeter: {Wetted_perimeter} m")

    # Derived geometric quantity
    hydraulic_diameter = Area / Wetted_perimeter
    log.append(f"Hydraulic diameter (Dh): {hydraulic_diameter} m")

    # Inputs for the computation
    print("Enter known values. Leave blank if unknown.")
    Re = get_input("Reynolds number (Re): ", allow_empty=True)
    velocity = get_input("Velocity (m/s): ", allow_empty=True)
    mass_flow_rate = get_input("Mass flow rate (kg/s): ", allow_empty=True)

    # Log the initial known values
    log.append(f"Reynolds number (Re): {Re if Re is not None else 'Unknown'}")
    log.append(f"Velocity: {velocity if velocity is not None else 'Unknown'} m/s")
    log.append(f"Mass flow rate: {mass_flow_rate if mass_flow_rate is not None else 'Unknown'} kg/s")

    # Calculate missing values
    if velocity is None and mass_flow_rate is not None:
        velocity = mass_flow_rate / (density * Area)
        log.append(f"Computed Velocity from mass flow rate: {velocity} m/s")
    elif velocity is not None and mass_flow_rate is None:
        mass_flow_rate = velocity * density * Area
        log.append(f"Computed Mass flow rate from velocity: {mass_flow_rate} kg/s")

    if Re is None and velocity is not None:
        Re = (velocity * density * hydraulic_diameter) / viscosity
        log.append(f"Computed Reynolds number (Re) from velocity: {Re}")
    elif Re is not None and velocity is None:
        velocity = (Re * viscosity) / (density * hydraulic_diameter)
        mass_flow_rate = velocity * density * Area
        log.append(f"Computed Velocity from Reynolds number: {velocity} m/s")
        log.append(f"Computed Mass flow rate from computed velocity: {mass_flow_rate} kg/s")

    # Output and log results
    print("\nComputed Results:")
    log.append("\nComputed Results:")
    result_Re = f"Reynolds number (Re): {Re if Re is not None else 'Could not compute'}"
    result_velocity = f"Velocity: {velocity if velocity is not None else 'Could not compute'} m/s"
    result_mass_flow_rate = f"Mass flow rate: {mass_flow_rate if mass_flow_rate is not None else 'Could not compute'} kg/s"

    print(result_Re)
    print(result_velocity)
    print(result_mass_flow_rate)

    log.append(result_Re)
    log.append(result_velocity)
    log.append(result_mass_flow_rate)

    # Write log to a file
    with open("fluid_flow_log.txt", "a") as log_file:
        log_file.write("\n".join(log) + "\n\n")
    print("\nCalculation log saved to 'fluid_flow_log.txt'.")

if __name__ == "__main__":
    print("=== Fluid Flow Calculator ===")
    compute_missing_values()
