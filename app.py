from flask import Flask, request, jsonify
import pandas as pd
import io
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        if 'file' in request.files:
            file = request.files['file']
            content = file.read()
        else:
            content = request.get_data()

        df = None
        errors = []

        # Try openpyxl (xlsx)
        try:
            df = pd.read_excel(io.BytesIO(content), engine='openpyxl', nrows=500)
        except Exception as e:
            errors.append(f'openpyxl: {e}')

        # Try xlrd (xls)
        if df is None:
            try:
                df = pd.read_excel(io.BytesIO(content), engine='xlrd', nrows=500)
            except Exception as e:
                errors.append(f'xlrd: {e}')

        # Try CSV
        if df is None:
            try:
                df = pd.read_csv(io.BytesIO(content), nrows=500)
            except Exception as e:
                errors.append(f'csv: {e}')

        if df is None:
            return jsonify({'error': 'Could not parse file', 'details': errors}), 500

        df = df.dropna(how='all').fillna('')
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
