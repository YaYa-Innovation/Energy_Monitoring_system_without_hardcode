# app.py

from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def read_temperatures(file_path='d:/Temp/temperatures.txt'):
    with open(file_path, 'r') as file:
        content = file.read()

    temperatures = []
    for match in re.finditer(r'temperature (\d+) = ([\d.]+), normal_color=([\d.]+), warning_color=([\d.]+), danger_color=([\d.]+), label=([^,\n]+)', content):
        temperatures.append(match.groups())

    return temperatures

def update_temperature(file_path='d:/Temp/temperatures.txt', box_number=None, new_temperature=None):
    if box_number and new_temperature:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if f'temperature {box_number} =' in line:
                lines[i] = f'temperature {box_number} = {new_temperature}, normal_color=50, warning_color=60, danger_color=70, label=Updated Label,\n'
                break

        with open(file_path, 'w') as file:
            file.writelines(lines)

def get_temperature_style(box_number, file_path='d:/Temp/temperatures.txt'):
    temperatures = read_temperatures(file_path)
    for temp_data in temperatures:
        if temp_data[0] == box_number:
            try:
                normal_color = float(temp_data[2])
                warning_color = float(temp_data[3])
                danger_color = float(temp_data[4])
            except ValueError:
                return 'gray'

            if float(temp_data[1]) < normal_color:
                return 'blue'
            elif normal_color <= float(temp_data[1]) < warning_color:
                return 'yellow'
            else:
                return 'red'
    return 'gray'

@app.route('/')
def index():
    temperatures = read_temperatures()
    return render_template('index.html', temperatures=temperatures, get_temperature_style=get_temperature_style)

@app.route('/update_temperature', methods=['POST'])
def update_temperature_route():
    box_number = request.form.get('box_number')
    new_temperature = request.form.get('new_temperature')

    update_temperature(box_number=box_number, new_temperature=new_temperature)

    return jsonify({'status': 'success'})

@app.route('/get_temperature/<box_number>', methods=['GET'])
def get_temperature(box_number):
    temperatures = read_temperatures()
    temperature_data = next((temp for temp in temperatures if temp[0] == box_number), None)

    if temperature_data:
        return jsonify({
            'temperature': temperature_data[1],
            'label': temperature_data[5],
            'color_values': (box_number, temperature_data[1], temperature_data[2], temperature_data[3], temperature_data[4])
        })

    return jsonify({'error': 'Box number not found'})

if __name__ == '__main__':
    app.run(debug=True)
