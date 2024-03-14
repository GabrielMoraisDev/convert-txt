from flask import Flask, render_template, request, send_file
import openpyxl
import io

app = Flask(__name__)

def process_text_file(file):
    try:
        lines = file.read().decode('utf-8').splitlines()
        print("Decodificação utf-8 bem sucedida.")
    except UnicodeDecodeError:
        # Se a decodificação utf-8 falhar, tenta com outra codificação
        lines = file.read().decode('latin-1').splitlines()
        print("Decodificação utf-8 falhou. Tentando com latin-1.")
        
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
            if data:
                wb = create_excel_file(data)
                
                # Salva o arquivo Excel em memória
                output = io.BytesIO()
                wb.save(output)
                output.seek(0)
                
                # Retorna o arquivo Excel como um anexo para download
                return send_file(output, as_attachment=True, download_name='converted.xlsx')
            else:
                return 'Os dados do arquivo estão vazios.'
    return 'Error processing file.'

if __name__ == '__main__':
    app.run(debug=True)
