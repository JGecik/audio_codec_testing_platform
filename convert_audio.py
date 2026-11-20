import os
import ffmpeg
from visual_data import audio_data

def convert_audio_file(input_path, output_folder, base_filename):
    acontainer = ['mp3', 'flac', 'ogg', 'wav']
    avcodec = ['libmp3lame', 'flac', 'libopus', 'pcm_s16le']

    stream = ffmpeg.input(input_path)
    download_links = []

    for i in range(len(acontainer)):
        output_name = f"{base_filename}_output.{acontainer[i]}"
        output_path = os.path.join(output_folder, output_name)

        out = ffmpeg.output(stream, output_path, acodec=avcodec[i])
        out.run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

        audio_info = audio_data(output_path)

        download_links.append({
            'format': acontainer[i],
            'url': f"/download/{output_name}",
            'waveform': audio_info['waveforms']
        })

    return download_links