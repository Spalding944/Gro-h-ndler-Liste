from flask import Flask, request, jsonify
import pandas as pd
import io
import os

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        filename = file.filename.lower()
        content = file.read()

        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content), nrows=500)
        elif filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(content), engine='xlrd', nrows=500)
        elif filename.endswith('.xlsx') or filename.endswith('.xlsm'):
            df = pd.read_excel(io.BytesIO(content), nrows=500)
        else:
            # Try xlsx as default
            try:
                df = pd.read_excel(io.BytesIO(content), nrows=500)
            except:
                df = pd.read_csv(io.BytesIO(content), nrows=500)

        # Clean up the dataframe
        df = df.dropna(how='all')
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
