from flask import Flask, request, jsonify
import pandas as pd
import io
import os
import base64

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Try file upload first
        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename.lower() if file.filename else 'file.xlsx'
            content = file.read()
        # Try base64 encoded data
        elif request.is_json:
            data = request.get_json()
            content = base64.b64decode(data.get('data', ''))
            filename = data.get('filename', 'file.xlsx').lower()
        # Try raw binary
        else:
            content = request.get_data()
            filename = 'file.xlsx'

        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content), nrows=500)
        elif filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(content), engine='xlrd', nrows=500)
        else:
            df = pd.read_excel(io.BytesIO(content), nrows=500)

        # Clean up
        df = df.dropna(how='all')
        # Fill NaN with empty string
        df = df.fillna('')
        text = df.to_csv(index=False)

        return jsonify({'text': text, 'rows': len(df)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
