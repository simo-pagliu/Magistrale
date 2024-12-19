import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import serpentTools

# Load detector mesh data
meshFile = 'Experimental Reactor Kinetics/TRIGA_FULL_CORE_det0.m'
mesh = serpentTools.read(meshFile).detectors['FissionRate']

# Extract grids and tallies
Z_old = mesh.grids['Z'][:, 2]  # Old Z (vertical)
X_old = mesh.grids['X'][:, 2]  # Old X
Y_old = mesh.grids['Y'][:, 2]  # Old Y
tallies = mesh.tallies

# Axis Mapping: Swap X and Z to make the XZ plane the XY plane
Z = X_old  # X stays as X
Y = Z_old  # Old Z becomes the new Y
X = Y_old  # Old Y becomes the new Z (vertical)

# Rotate tallies to match the new axes
tallies_rotated = np.transpose(tallies, (2, 1, 0))  # Adjust axis order

# Create a new meshgrid
x_grid, y_grid, z_grid = np.meshgrid(X, Y, Z, indexing='ij')
tallies_normalized = tallies_rotated / np.max(tallies_rotated)

# Flatten the grids and tallies
x_flat = x_grid.flatten()
y_flat = y_grid.flatten()
z_flat = z_grid.flatten()
tallies_flat = tallies_normalized.flatten()

# Define a mask for the cylindrical region (radius <= 30)
r_flat = np.sqrt(x_flat**2 + y_flat**2)  # Radius in cylindrical coordinates
cylinder_mask = r_flat <= 30  # Complete cylinder boundary

# Apply mask for cylinder
x_cylinder = x_flat[cylinder_mask]
y_cylinder = y_flat[cylinder_mask]
z_cylinder = z_flat[cylinder_mask]
tallies_cylinder = tallies_flat[cylinder_mask]

# Calculate non-linear transparency (alpha) based on intensity
alpha_values = tallies_cylinder ** 3  # Apply power-law scaling for non-linearity

# Create a custom colormap with blue tones
blue_only_cmap = LinearSegmentedColormap.from_list(
    "blue_only", ["#00008B", "#ADD8E6"], N=256  # Dark blue to light blue
)

# Create a figure with black background
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d', proj_type='persp', facecolor='black')

# Map the normalized tallies to the custom colormap
colors = blue_only_cmap(tallies_cylinder)  # Get RGBA colors
colors[:, -1] = alpha_values  # Set alpha channel non-linearly

# Plot the points for the complete cylinder
ax.scatter(
    x_cylinder, y_cylinder, z_cylinder,
    facecolors=colors, s=10, edgecolors='none'  # Larger points (s=10)
)

# Adjust axis limits and proportions
ax.set_xlim([X.min(), X.max()])
ax.set_ylim([Y.min(), Y.max()])
ax.set_zlim([Z.min(), Z.max()])
ax.set_box_aspect([1, 1, 1])  # Equal scaling for all axes

# Set view angle
ax.view_init(elev=35, azim=-90)  # Perspective view

# Remove axes and ticks
ax.set_axis_off()

# Save and display the figure
output_file = "TRIGA.png"
plt.savefig(output_file, dpi=800, facecolor='black', bbox_inches='tight')

print(f"Image saved as: {output_file}")
