import librosa
import numpy as np
import librosa
from sklearn.metrics.pairwise import cosine_similarity
from pydub import AudioSegment

def amongus(num):
    audio_1, sr_1 = librosa.load(f"ans{num}.wav")
    audio_2, sr_2 = librosa.load(f"voice{num}.wav")

    mfcc_1 = librosa.feature.mfcc(y=audio_1, sr=sr_1, n_mfcc=13)
    mfcc_2 = librosa.feature.mfcc(y=audio_2, sr=sr_2, n_mfcc=13)

    mfcc_1_normalized = (mfcc_1 - mfcc_1.mean()) / mfcc_1.std()
    mfcc_2_normalized = (mfcc_2 - mfcc_2.mean()) / mfcc_2.std()

    similarity_score = cosine_similarity(mfcc_1_normalized.T, mfcc_2_normalized.T)

    return similarity_score[0, 0]

def main():
    threshold2 = 0.85
    scores = []

    audio_file, sr = librosa.load('recording.wav')
    audio = AudioSegment.from_file('recording.wav')

    amplitude_env = np.abs(librosa.effects.preemphasis(audio_file))

    mean_amp = np.mean(amplitude_env)
    std_amp = np.std(amplitude_env)

    threshold = mean_amp + 3 * std_amp

    min_pause_duration = 0.2

    pauses = []
    is_in_pause = False
    pause_start = 0

    for i, amp_value in enumerate(amplitude_env):
        if amp_value < threshold:
            if not is_in_pause:
                pause_start = i
                is_in_pause = True
        else:
            if is_in_pause:
                pause_end = i
                pause_duration = (pause_end - pause_start) / sr 
                if pause_duration >= min_pause_duration:
                    pauses.append((pause_start, pause_end))
                is_in_pause = False

    pause_intervals = [(start / sr, end / sr) for start, end in pauses]

    for i in range(len(pause_intervals)-1):
        cut_audio = audio[pause_intervals[i][1]*1000:pause_intervals[i+1][0]*1000]
        cut_audio.export('voice'+str(i)+'.wav', format="wav")
        scores.append(amongus(i))
    cut_audio = audio[pause_intervals[-1][1]*1000:]
    cut_audio.export('voice'+str(len(pause_intervals)-1)+'.wav', format="wav")
    scores.append(amongus(len(pause_intervals)-1))

    final_scores = [x > threshold2 for x in scores]

    print(final_scores)
    return final_scores


if __name__ == "__main__":
    main()
