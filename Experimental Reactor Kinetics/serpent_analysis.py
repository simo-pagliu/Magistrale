import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from PIL import Image
import serpentTools

# Load detector mesh data
meshFile = 'Experimental Reactor Kinetics/TRIGA_FULL_CORE_det0.m'
mesh = serpentTools.read(meshFile).detectors['FissionRate']

# Extract grids and tallies
Z_old = mesh.grids['Z'][:, 2]  # Old Z
X_old = mesh.grids['X'][:, 2]  # Old X
Y_old = mesh.grids['Y'][:, 2]  # Old Y
tallies = mesh.tallies

# Reorient axes: X -> Z, Y -> X, Z -> Y
Z = X_old  # New Z
X = Y_old  # New X
Y = Z_old  # New Y

# Rotate tallies to match new axes
tallies_rotated = np.transpose(tallies, (1, 2, 0))  # Reorient axes

# Create a uniform 3D Cartesian grid with reoriented axes
z_grid, x_grid, y_grid = np.meshgrid(Z, X, Y, indexing='ij')
tallies_normalized = tallies_rotated / np.max(tallies_rotated)

# Initialize Dash app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Controls"),
            html.Label("Threshold:"),
            dcc.Slider(id='threshold-slider', min=0.0, max=1.0, step=0.05, value=0.5, tooltip={"placement": "bottom"}),
            html.Label("Transparency:"),
            dcc.Slider(id='alpha-slider', min=0.1, max=1.0, step=0.1, value=1.0, tooltip={"placement": "bottom"}),
            html.Label("Y Cut Plane:"),
            dcc.Slider(id='y-slider', min=Y.min(), max=Y.max(), step=5, value=Y.mean(), tooltip={"placement": "bottom"}),
        ], width=3, style={"padding": "20px", "background-color": "#f8f9fa", "height": "100vh", "overflow": "auto"}),

        dbc.Col([
            dcc.Graph(id='3d-scatter-plot', style={"height": "100vh"})
        ], width=9)
    ])
], fluid=True)

@app.callback(
    Output('3d-scatter-plot', 'figure'),
    Input('threshold-slider', 'value'),
    Input('alpha-slider', 'value'),
    Input('y-slider', 'value')
)
def update_figure(threshold, alpha, y_cut):
    # Apply threshold and Y cut for scatter plot
    mask = (tallies_normalized >= threshold) & (y_grid <= y_cut)  # Points BELOW or ON the Y plane
    z_masked, x_masked, y_masked = z_grid[mask], x_grid[mask], y_grid[mask]
    tallies_filtered = tallies_normalized[mask]

    # Create scatter plot for the fission rate
    scatter = go.Scatter3d(
        x=z_masked,  # Z becomes X
        y=x_masked,  # X becomes Y
        z=y_masked,  # Y becomes Z
        mode='markers',
        marker=dict(size=3, color=tallies_filtered, colorscale='Viridis', opacity=alpha),
        name='Fission Rate'
    )

    # Extract the XZ slice for the Y cut plane
    y_index = np.abs(Y - y_cut).argmin()
    tallies_plane_xz = tallies_normalized[:, :, y_index]
    z_plane_xz = z_grid[:, :, y_index]
    x_plane_xz = x_grid[:, :, y_index]
    y_plane_fixed = np.full_like(tallies_plane_xz, y_cut)

    # Add the surface trace for the Y cut plane
    contour_surface_xz = go.Surface(
        x=z_plane_xz,  # New X axis (old Z)
        y=x_plane_xz,  # New Y axis (old X)
        z=y_plane_fixed,  # Fixed Y plane
        surfacecolor=tallies_plane_xz,
        colorscale='Viridis',
        opacity=0.7,
        showscale=True,
        name='Y Cut Plane'
    )

    # Calculate proportional ranges
    range_x = [Z.min(), Z.max()]
    range_y = [X.min(), X.max()]
    range_z = [Y.min(), Y.max()]
    max_range = max((range_x[1] - range_x[0]), (range_y[1] - range_y[0]), (range_z[1] - range_z[0]))

    # Adjust ranges to enforce equal proportions
    mid_x = (range_x[0] + range_x[1]) / 2
    mid_y = (range_y[0] + range_y[1]) / 2
    mid_z = (range_z[0] + range_z[1]) / 2
    adjusted_range_x = [mid_x - max_range / 2, mid_x + max_range / 2]
    adjusted_range_y = [mid_y - max_range / 2, mid_y + max_range / 2]
    adjusted_range_z = [mid_z - max_range / 2, mid_z + max_range / 2]

    # Build the figure
    fig = go.Figure(data=[scatter, contour_surface_xz])

    # Update layout with adjusted ranges
    fig.update_layout(
        scene=dict(
            xaxis_title='Z (cm)',
            yaxis_title='X (cm)',
            zaxis_title='Y (cm)',
            xaxis=dict(range=adjusted_range_x),
            yaxis=dict(range=adjusted_range_y),
            zaxis=dict(range=adjusted_range_z)
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
