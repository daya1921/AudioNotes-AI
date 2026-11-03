# AudioNotes-AI

A small Windows desktop app for capturing microphone or system audio and creating a Hindi transcript with an English translation. Speech recognition runs locally with faster-whisper; recordings are not sent to an online transcription service.

## Run from source

1. Open PowerShell in this folder.
2. Create and activate a virtual environment:

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Start the app with `python main.py`.

Choose a microphone for room audio or a loopback source for audio playing on the PC. Click **Start recording**, then **Stop and make notes**. Audio is saved in `recordings/`; the transcript and English translation are saved in `notes/`.

## Build the Windows app

With the project environment activated and dependencies installed, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1
```

The app is created at `dist\AudioNotesAI\AudioNotesAI.exe`. Keep the entire `dist\AudioNotesAI` folder together when moving the app. The first transcription downloads the Whisper Base model (roughly 150 MB) to the local model cache. The Base model runs on CPU with int8 to limit memory use on an 8 GB computer.

## GitHub

The project has a local Git repository. To publish it, create an empty GitHub repository, sign in with GitHub CLI, add that repository as the `origin` remote, then push the `master` branch.
