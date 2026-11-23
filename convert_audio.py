import os
import ffmpeg
from visual_data import audio_data

SUPPORTED_CODECS = {
    'mp3': {'codec': 'libmp3lame', 'container': 'mp3', 'type': 'lossy'},
    'flac': {'codec': 'flac', 'container': 'flac', 'type': 'lossless'},
    'ogg': {'codec': 'libopus', 'container': 'ogg', 'type': 'lossy'},
    'wav': {'codec': 'pcm_s16le', 'container': 'wav', 'type': 'lossless'},
    'aac': {'codec': 'aac', 'container': 'm4a', 'type': 'lossy'},
    'wma': {'codec': 'wmav2', 'container': 'wma', 'type': 'lossy'}
}

def convert_audio_file(input_path, output_folder, base_filename, selected_codecs):


    stream = ffmpeg.input(input_path)
    original_size = os.path.getsize(input_path)
    download_links = []

    for codec_key in selected_codecs:
        if codec_key not in SUPPORTED_CODECS:
            continue

        cfg = SUPPORTED_CODECS[codec_key]
        output_name = f"{base_filename}_output.{cfg['container']}"
        output_path = os.path.join(output_folder, output_name)

        out = ffmpeg.output(stream, output_path, acodec=cfg['codec'])
        out.run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

        output_size = os.path.getsize(output_path)
        file_size_kb = round(output_size / 1024, 2)
        savings_percent = round((1 - (output_size / original_size)) * 100, 1)
        if savings_percent < 0:
            savings_percent = 0.0
        audio_info = audio_data(output_path)
        bitrate = audio_info.get('bitrate', 'N/A')

        download_links.append({
            'format': cfg['container'],
            'codec_key': codec_key,
            'type': cfg['type'],
            'url': f"/download/{output_name}",
            'filename': output_name,
            'waveform': audio_info['waveforms'],
            'duration': audio_info['duration'],
            'sample_rate': audio_info['sample_rate'],
            'size_kb': file_size_kb,
            'savings_percent': savings_percent,
            'bitrate': bitrate
        })

    return download_links