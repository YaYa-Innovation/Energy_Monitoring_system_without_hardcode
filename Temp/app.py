from flask import Flask, render_template
import re

app = Flask(__name__)

def read_temperatures(file_path='d:/Temp/temperatures.txt'):
    with open(file_path, 'r') as file:
        content = file.read()
    # Extract temperatures using regex
    temperatures = re.findall(r'temperature (\d+) = (\d+),', content)
    return temperatures

@app.route('/')
def index():
    temperatures = read_temperatures()
    return render_template('index.html', temperatures=temperatures)

if __name__ == '__main__':
    app.run(debug=True)
