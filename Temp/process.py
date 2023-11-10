def process_numbers(input_file_path, output_file_path):
    try:
        # Open the input file for reading
        with open(input_file_path, 'r') as input_file:
            # Read numeric values from the file
            numbers = [float(line.strip()) for line in input_file]

        # Process the numbers by adding 2
        processed_numbers = [num + 2 for num in numbers]

        # Open the output file for writing
        with open(output_file_path, 'w') as output_file:
            # Write the processed numbers to the new file
            for result in processed_numbers:
                output_file.write(f'{result}\n')

        print(f"Processing complete. Results written to {output_file_path}")

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file_path = 'd:/Temp/input.txt'  # Replace with your input file path
output_file_path = 'd:/Temp/output.txt'  # Replace with your desired output file path

process_numbers(input_file_path, output_file_path)
