# AudioNotes-AI

A Windows desktop app that records microphone or system audio and creates a Hindi transcript with an English translation. Speech recognition runs locally with faster-whisper.

## Features

- Select an available microphone or system-audio loopback device.
- Record audio and save it as a WAV file.
- Transcribe Hindi speech and generate an English translation on the CPU.
- Detect silent recordings and tell the user how to fix the selected audio source.
- Save transcripts and translations as UTF-8 text files.
- Build a portable Windows app folder with PyInstaller.

## Demo

Add a short screen recording or a screenshot showing a successful transcription here before sharing the repository with interviewers. Avoid including private recordings or personal information.

## Tech

- Python and Tkinter for the Windows desktop interface
- SoundCard for microphone and loopback capture
- faster-whisper with the Whisper Base model for local speech recognition and translation
- NumPy and SoundFile for audio processing and WAV output
- PyInstaller for Windows packaging

## Run from source

Use the project's existing `venv` if it is already set up. Otherwise, install 64-bit Python and run these commands in PowerShell from the project folder:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Choose a microphone to record nearby speech. Choose a loopback device to record audio playing through that device; make sure the audio is playing while recording. Click **Start recording**, then **Stop and make notes**.

## Build the Windows app

With the virtual environment active and dependencies installed, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1
```

The app is created at `dist-updated\AudioNotesAI\AudioNotesAI.exe`. Keep the entire `dist-updated\AudioNotesAI` folder together when moving the app. Audio and text outputs are saved in `recordings/` and `notes/` beside the executable.

The first transcription downloads the Whisper Base model (about 150 MB). Later runs use the local model cache. Base runs on CPU with int8 to limit memory use on an 8 GB computer.

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
