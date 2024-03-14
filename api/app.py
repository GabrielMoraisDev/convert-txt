from flask import Flask, render_template, request, send_file
import openpyxl
import os

app = Flask(__name__)

def process_text_file(file):
    lines = file.read().decode('utf-8').splitlines()
    data = [line.strip().split("  ") for line in lines]
    return data

def create_excel_file(data):
    wb = openpyxl.Workbook()
    ws = wb.active

    for row in data:
        ws.append(row)

    return wb

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data = process_text_file(file)
            wb = create_excel_file(data)
            filename = 'cleaned.xlsx'
            wb.save(filename)
            return send_file(filename, as_attachment=True)
    return 'Error processing file.'

if __name__ == '__main__':
    app.run(debug=True)
