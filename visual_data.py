import librosa
import ffmpeg

def audio_data(file):
    try:
        y, sample_rate = librosa.load(file, sr=None)


        duration = float(librosa.get_duration(y=y, sr=sample_rate))


        probe = ffmpeg.probe(file)
        format_info = probe.get('format', {})
        bit_rate_bps = format_info.get('bit_rate', None)

        if bit_rate_bps:
            bitrate = round(int(bit_rate_bps) / 1000)
        else:
            bitrate = 'N/A'


        waveforms = y[::500].tolist() if len(y) > 0 else []
        return {
            "duration": duration,
            "sample_rate": int(sample_rate),
            "bitrate": bitrate,
            "waveforms": waveforms
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {
        "duration": 0.0,
        "sample_rate": 44100,
        "bitrate": 'N/A',
        "waveforms": []
    }

