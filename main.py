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
        return jsonify({'error': 'No file added'}), 400

    file = request.files['file']
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    base_name = os.path.splitext(file.filename)[0]

    try:

        audio_info = audio_data(input_path)
        download_links = convert_audio_file(
            input_path=input_path,
            output_folder=UPLOAD_FOLDER,
            base_filename=base_name
        )

        return jsonify({
            'links': download_links,
            'waveform': audio_info['waveforms'],
            'duration': audio_info['duration'],
            'sample_rate': audio_info['sample_rate']
        })

    except ffmpeg.Error as e:
        error_msg = e.stderr.decode('utf-8') if e.stderr else str(e)
        return jsonify({'error': f'Error during conversion: {error_msg}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)