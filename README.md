# AudioNotes-AI

A Windows desktop app that records microphone or system audio and creates a Hindi transcript with an English translation. Speech recognition runs locally with faster-whisper.

## Features

- Select an available microphone or system-audio loopback device.
- Record audio and save it as a WAV file.
- Transcribe Hindi speech and generate an English translation on the CPU.
- Detect silent recordings and tell the user how to fix the selected audio source.
- Save transcripts and translations as UTF-8 text files.
- Build a portable Windows app folder with PyInstaller.

## Tech

- Python and Tkinter for the Windows desktop interface
- SoundCard for microphone and loopback capture
- faster-whisper with the Whisper Base model for local speech recognition and translation
- NumPy and SoundFile for audio processing and WAV output
- PyInstaller for Windows packaging

## Data and limitations

- Audio is processed on the computer; it is not sent to an online transcription service.
- Hindi is selected as the source language. Results depend on audio clarity, microphone quality, and background noise.
- The app currently creates a transcript and translation; it does not yet generate summaries or action items.
- Designed and packaged for Windows.

## Project layout

```text
main.py                    Tkinter interface and recording flow
transcription/transcribe.py Hindi transcription and English translation
audio_capture/             Audio-device inspection utilities
build_windows.ps1          Windows packaging command
AudioNotesAI.spec           PyInstaller configuration
recordings/                 Runtime WAV files (not tracked by Git)
notes/                      Runtime text output (not tracked by Git)
```
