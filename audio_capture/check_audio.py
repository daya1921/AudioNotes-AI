import soundfile as sf
import numpy as np

audio, sample_rate = sf.read("recordings/test_audio.wav")

print("Sample rate:", sample_rate)
print("Audio shape:", audio.shape)
print("Duration:", len(audio) / sample_rate, "seconds")
print("Maximum volume:", np.max(np.abs(audio)))
print("Average volume:", np.sqrt(np.mean(audio ** 2)))