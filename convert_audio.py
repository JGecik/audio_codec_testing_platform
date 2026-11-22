import os
import ffmpeg
from visual_data import audio_data

SUPPORTED_CODECS = {
    'mp3': {'codec': 'libmp3lame', 'container': 'mp3'},
    'flac': {'codec': 'flac', 'container': 'flac'},
    'ogg': {'codec': 'libopus', 'container': 'ogg'},
    'wav': {'codec': 'pcm_s16le', 'container': 'wav'},
    'aac': {'codec': 'aac', 'container': 'm4a'},
    'wma': {'codec': 'wmav2', 'container': 'wma'}
}

def convert_audio_file(input_path, output_folder, base_filename, selected_codecs):
    acontainer = ['mp3', 'flac', 'ogg', 'wav']
    avcodec = ['libmp3lame', 'flac', 'libopus', 'pcm_s16le']

    stream = ffmpeg.input(input_path)
    download_links = []

    for codec_key in selected_codecs:
        if codec_key not in SUPPORTED_CODECS:
            continue

        cfg = SUPPORTED_CODECS[codec_key]
        output_name = f"{base_filename}_output.{cfg['container']}"
        output_path = os.path.join(output_folder, output_name)

        out = ffmpeg.output(stream, output_path, acodec=cfg['codec'])
        out.run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

        file_size_bytes = os.path.getsize(output_path)
        file_size_kb = round(file_size_bytes / 1024, 2)

        audio_info = audio_data(output_path)

        download_links.append({
            'format': cfg['container'],
            'url': f"/download/{output_name}",
            'waveform': audio_info['waveforms'],
            'duration': audio_info['duration'],
            'sample_rate': audio_info['sample_rate'],
            'size_kb': file_size_kb
        })

    return download_links