import librosa
import numpy

def audio_data(file):
    a_data, s_rate = librosa.load(file, sr=None)

    spectogram = librosa.feature.melspectrogram(y=a_data, sr=s_rate, n_mels=128)
    spectogram_db = librosa.power_to_db(spectogram, ref=numpy.max)

    data_export= {
        "sample_rate": int(s_rate),
        "duration": float(librosa.get_duration(filename=file, sr=s_rate)),
        "waveforms": a_data[::100].tolist(),
        "spectogram": list(spectogram_db.shape),
    }

    return data_export

