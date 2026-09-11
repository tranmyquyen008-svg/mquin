from flask import Flask, render_template, request, send_file
import pdfplumber
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    file = request.files['pdf_file']
    if not file:
        return "Vui lòng chọn file!"

    data = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            data.append({"Noi_dung": text})

    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, engine='openpyxl')
    excel_file.seek(0)

    return send_file(excel_file, download_name="Hoa_don_Excel.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
