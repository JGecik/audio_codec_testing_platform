import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import ffmpeg

from visual_data import audio_data
from convert_audio import convert_audio_file

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('webapp.html')

UPLOAD_FOLDER = 'converted_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file was uploaded'}), 400

    file = request.files['file']

    filename = file.filename

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    base_name = os.path.splitext(file.filename)[0]


    selected_codecs = request.form.getlist('codecs')
    if not selected_codecs:
        selected_codecs = ['mp3', 'flac', 'ogg', 'wav', 'aac', 'wma']



    try:

        original_info = audio_data(input_path)
        original_size_kb = round(os.path.getsize(input_path) / 1024, 2)


        download_links = convert_audio_file(
            input_path=input_path,
            output_folder=UPLOAD_FOLDER,
            base_filename=base_name,
            selected_codecs=selected_codecs
        )

        return jsonify({
            'original': {
                'name': filename,
                'size_kb': original_size_kb,
                'duration': original_info['duration'],
                'sample_rate': original_info['sample_rate']
            },
            'links': download_links
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)