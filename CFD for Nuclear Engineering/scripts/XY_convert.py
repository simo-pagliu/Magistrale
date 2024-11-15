import csv
import sys

def load_xy_data(filename):
    """
    Load data from an ANSYS Fluent .xy file.

    Parameters:
        filename (str): Path to the .xy file.

    Returns:
        tuple: Two lists containing x and y values.
    """
    x = []
    y = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith(("#", "(", ")")):
                x_val, y_val = map(float, line.split())
                x.append(x_val)
                y.append(y_val)
    return x, y

def convert_xy_to_csv(input_filename, output_filename=None):
    """
    Convert an ANSYS Fluent .xy file to a .csv file.

    Parameters:
        input_filename (str): Path to the .xy file.
        output_filename (str): Path to the output .csv file (optional).
                               If not provided, it will use the same name as the input file with .csv extension.
    """
    # Load data
    x, y = load_xy_data(input_filename)

    # Set default output filename if not provided
    if output_filename is None:
        output_filename = input_filename.rsplit(".", 1)[0] + ".csv"

    # Write to CSV
    with open(output_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["x", "y"])  # Header
        csv_writer.writerows(zip(x, y))

    print(f"Data has been written to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_xy_to_csv.py <input_filename.xy> [output_filename.csv]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_xy_to_csv(input_file, output_file)
