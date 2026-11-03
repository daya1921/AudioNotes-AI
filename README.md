# AudioNotes-AI

A small Windows desktop app for capturing microphone or system audio and creating a Hindi transcript with an English translation. Speech recognition runs locally with faster-whisper; no recording is uploaded to an online transcription service.

## Run on Windows

1. Install Python 3.11 or 3.12 (64-bit).
2. Open PowerShell in this folder.
3. Create and activate a virtual environment:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   python main.py
   ```

The first transcription downloads the Whisper Base model (roughly 150 MB). It runs on the CPU using int8 to reduce memory use. Select a microphone for room audio or a loopback source for audio playing on the PC. Click **Start recording**, then **Stop and make notes**. Audio is saved in `recordings/` and the transcript plus English translation in `notes/`.

## Notes

- The app uses the `base` model as a practical starting point for an 8 GB computer. Larger models may improve recognition but use more memory and run more slowly.
- The Hindi language is selected for the original transcript. The app also asks Whisper for an English translation.
- The project currently uses local Git only. Add a GitHub remote after signing in to GitHub and creating an empty repository there.
