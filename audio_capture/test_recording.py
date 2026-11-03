import soundcard as sc
import soundfile as sf

DURATION = 10
SAMPLE_RATE = 48000

print("Available loopback devices:")

devices = [
    mic for mic in sc.all_microphones(include_loopback=True)
    if mic.isloopback
]

for index, device in enumerate(devices):
    print(f"{index}: {device.name}")

device_index = int(input("\nEnter the loopback device number: "))
selected_device = devices[device_index]

print(f"\nRecording from: {selected_device.name}")
print("Play a video now. Recording for 10 seconds...")

audio = selected_device.record(
    samplerate=SAMPLE_RATE,
    numframes=SAMPLE_RATE * DURATION
)

sf.write("recordings/test_audio.wav", audio, SAMPLE_RATE)

print("\nRecording saved to recordings/test_audio.wav")