
import soundcard as sc


def detect_audio_devices():

    print("\n===== AUDIO OUTPUT DEVICES =====")

    speakers = sc.all_speakers()

    for index, speaker in enumerate(speakers, start=1):
        print(f"{index}. {speaker.name}")

    print("\n===== LOOPBACK DEVICES =====")

    microphones = sc.all_microphones(
        include_loopback=True
    )

    for index, mic in enumerate(microphones, start=1):
        if mic.isloopback:
            print(f"{index}. {mic.name}")

    print("\n===== DEFAULT AUDIO DEVICE =====")

    default_speaker = sc.default_speaker()

    print("Default speaker:", default_speaker.name)

    print("\nAudio device detection completed!")


if __name__ == "__main__":
    detect_audio_devices()
