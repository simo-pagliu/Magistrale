
# Project Documentation

This project includes scripts for fluid flow calculations, mixing temperature calculations, and data conversions from ANSYS Fluent `.xy` files. Each script is documented below with usage instructions and function descriptions.

---
## Wall_Shear_Calculator.py

This script calculates the wall shear stress, friction velocity, and characteristic y-value based on user inputs for friction factor, velocity, density, and viscosity.
Usage

To run the script, use the following command:

```bash
py Wall_Shear_Calculator.py
```

The script will guide you through entering properties interactively. Default values are provided for y+, density, and viscosity, but friction factor and velocity must be specified.
Logging

Each run of the script logs the input parameters, intermediate calculations, and results to wall_shear_log.txt.

#### Example
```bash
Enter y+ limit (default 1): 
Enter friction factor: 0.005
Enter velocity (m/s): 10
Enter density (kg/m³, default air: 1.225): 
Enter viscosity (kg/m·s, default air: 1.789e-5): 

Results:
Wall shear stress: 0.00765 Pa
Friction velocity: 0.07802 m/s
y: 0.00182 m

Calculation log saved to 'wall_shear_log.txt'.
```

#### Function Documentation

 -   **`get_input(prompt, allow_empty=False, default=None)`**
      - **Description**: Helper function to get validated user input with optional default values.
      - **Parameters**:
          - `prompt` (str): Prompt message for the user.
          - `allow_empty` (bool): Whether to allow empty input.
          - `default` (any): Default value if the user presses Enter.

    **calculate_wall_shear_y()**
        **Description**: Main function to calculate wall shear stress, friction velocity, and y.


## XY_convert.py

This script converts `.xy` files produced by ANSYS Fluent to a more usable format, such as `.csv`, for further analysis. The script can be run as a standalone tool from the command line or used as a function in other Python scripts.

### Usage

To convert a `.xy` file to a `.csv` file, use the following command:

```bash
python XY_convert.py data.xy output.csv
```

- `data.xy`: Path to the input `.xy` file.
- `output.csv`: Path to the output `.csv` file (optional). If not provided, it will default to the same name as the input file with a `.csv` extension.

#### Example

```bash
python XY_convert.py example_data.xy example_data.csv
```

If `output.csv` is not specified, the script will save the output as `data.csv` in the same directory.

### Using as a Function in Other Scripts

The function `load_xy_data` is available for importing into other scripts, allowing you to load `.xy` data directly.

#### Usage

```python
from XY_convert import load_xy_data  

# Load x and y data from the .xy file
x, y = load_xy_data("data.xy")

# Now you can work with x and y data in your script
```

#### Function Documentation

- **`load_xy_data(filename)`**  
  - **Description**: Loads data from an ANSYS Fluent `.xy` file, filtering out comments and irrelevant lines.
  - **Parameters**: 
    - `filename` (str): Path to the `.xy` file.
  - **Returns**: 
    - `tuple`: Two lists containing `x` and `y` values, respectively.

---

## Flow_Data.py

This script calculates missing fluid flow properties, such as Reynolds number, velocity, or mass flow rate, given certain input parameters. It allows for interactive input and logs calculations to a file named `fluid_flow_log.txt`.

### Usage

To run the script, use the following command:

```bash
python Flow_Data.py
```

The script will prompt you to enter values for density, viscosity, area, wetted perimeter, and any known fluid properties (Reynolds number, velocity, or mass flow rate). You can leave fields blank to have the script calculate missing values.

### Logging

Each run of the script logs the input parameters, calculated values, and results to `fluid_flow_log.txt`. This file is updated with a new entry every time the script is run.

#### Example Interaction

```plaintext
Enter density (kg/m³, default 1.225): 
Enter viscosity (kg/m·s, default 1.789e-5): 
Enter area (m²): 1.5
Enter wetted perimeter (m): 2.0
Enter known values. Leave blank if unknown.
Reynolds number (Re): 50000
Velocity: 
Mass flow rate: 
```

### Function Documentation

- **`get_input(prompt, allow_empty=False)`**  
  - **Description**: Helper function to get validated user input.
  - **Parameters**: 
    - `prompt` (str): Prompt message for the user.
    - `allow_empty` (bool): Whether to allow empty input.

- **`compute_missing_values()`**  
  - **Description**: Main function that calculates missing fluid properties based on the inputs. This function also logs the calculations.

---

## Two Flows Mixing.py

This script calculates the outlet temperature of two mixing fluid streams with different properties, such as temperature, viscosity, density, flow area, and specific heat capacity. It also supports calculating unknown velocities based on Reynolds number or mass flow rate. The results are logged to a file named `mixing_log.txt`.

### Usage

To run the script, use the following command:

```bash
python Two\ Flows\ Mixing.py
```

The script will guide you through entering properties for the first and second streams. For the second stream, you have the option to use the same values as the first stream by pressing Enter.

### Logging

Each run of the script logs the input parameters, calculated values, and results to `mixing_log.txt`. This file is updated with a new entry every time the script is run.

#### Example Interaction

```plaintext
Enter properties for the first (cold) stream:
Temperature (°C): 25
Viscosity (kg/(m·s)): 0.001
Density (kg/m³): 1000
Flow area (m²): 0.5
Hydraulic diameter (m): 0.2
Specific heat capacity (Cp) (J/(kg·K)): 4182
Is the Reynolds number known for the first stream? (y/n): y
Reynolds number (Re): 20000

Enter properties for the second (hot) stream. Press Enter to use the same value as the first stream.
Temperature (°C): 80
```

### Function Documentation

- **`get_input(prompt, default=None)`**  
  - **Description**: Helper function to get validated user input with optional default values.
  - **Parameters**: 
    - `prompt` (str): Prompt message for the user.
    - `default` (any): Default value if the user presses Enter.

- **`compute_velocity_from_reynolds(Re, density, viscosity, Dh)`**  
  - **Description**: Calculates velocity based on Reynolds number, density, viscosity, and hydraulic diameter.
  - **Parameters**: 
    - `Re` (float): Reynolds number.
    - `density` (float): Density of the fluid.
    - `viscosity` (float): Viscosity of the fluid.
    - `Dh` (float): Hydraulic diameter.
  - **Returns**: 
    - `float`: Calculated velocity.

- **`compute_velocity_from_mass_flow(mass_flow_rate, density, area)`**  
  - **Description**: Calculates velocity based on mass flow rate, density, and flow area.
  - **Parameters**: 
    - `mass_flow_rate` (float): Mass flow rate of the fluid.
    - `density` (float): Density of the fluid.
    - `area` (float): Cross-sectional area.
  - **Returns**: 
    - `float`: Calculated velocity.

- **`calculate_outlet_temperature()`**  
  - **Description**: Main function to calculate the outlet temperature of two mixing streams and log the calculations.

---

This documentation provides an overview of each script, including usage instructions, examples, and detailed explanations for each function. This setup allows users to utilize the scripts both as standalone command-line tools and as modules in larger Python projects.
