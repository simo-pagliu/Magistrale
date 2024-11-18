from datetime import datetime

def get_input(prompt, allow_empty=False, default=None):
    """
    Helper function to get user input, with validation and optional default handling.
    """
    while True:
        value = input(prompt)
        if allow_empty and value.strip() == "":
            return default
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a number or leave blank to use the default.")

def calculate_wall_shear_y():
    """
    Calculate the wall shear stress, friction velocity, and characteristic y-value
    based on user inputs for y+, friction factor, velocity, density, and viscosity.
    """
    log = []  # List to accumulate log entries
    log.append(f"=== Wall Shear Stress Calculation Log ===")
    log.append(f"Date & Time: {datetime.now()}\n")

    # Interactive inputs
    y_plus = get_input("Enter y+ limit (default 1): ", allow_empty=True, default=1)
    log.append(f"y+ limit: {y_plus}")

    friction_factor = get_input("Enter friction factor: ")
    log.append(f"Friction factor: {friction_factor}")

    velocity = get_input("Enter velocity (m/s): ")
    log.append(f"Velocity: {velocity} m/s")

    density = get_input("Enter density (kg/m³, default air: 1.225): ", allow_empty=True, default=1.225)
    log.append(f"Density: {density} kg/m³")

    viscosity = get_input("Enter viscosity (kg/m·s, default air: 1.789e-5): ", allow_empty=True, default=1.789e-5)
    log.append(f"Viscosity: {viscosity} kg/m·s")

    # Calculations
    wall_shear_stress = 1/2 * friction_factor / 4 * density * velocity**2
    friction_velocity = (wall_shear_stress / density)**0.5
    y = ((y_plus * viscosity) / (density * friction_velocity) ) * 1000 # Convert to mm

    # Results
    log.append(f"Wall shear stress: {wall_shear_stress:.5f} Pa")
    log.append(f"Friction velocity: {friction_velocity:.5f} m/s")
    log.append(f"Characteristic y: {y:.5f} mm")

    print("\nResults:")
    print(f"Wall shear stress: {wall_shear_stress:.5f} Pa")
    print(f"Friction velocity: {friction_velocity:.5f} m/s")
    print(f"y: {y:.5f} mm")

    # Save log to file
    with open("wall_shear_log.txt", "a") as log_file:
        log_file.write("\n".join(log) + "\n\n")
    print("\nCalculation log saved to 'wall_shear_log.txt'.")

if __name__ == "__main__":
    print("=== Wall Shear Calculator ===")
    calculate_wall_shear_y()
