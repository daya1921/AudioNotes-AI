"""Local Hindi transcription and English translation using faster-whisper."""

from dataclasses import dataclass
from pathlib import Path

from faster_whisper import WhisperModel


@dataclass
class TranscriptionResult:
    transcript: str
    translation: str
    detected_language: str


def transcribe_audio(
    audio_path: str | Path,
    *,
    model_size: str = "base",
    language: str | None = "hi",
    model: WhisperModel | None = None,
) -> TranscriptionResult:
    """Transcribe audio, then translate it to English, entirely on-device.

    Supplying ``model`` lets callers reuse one loaded model and keeps this
    function straightforward to exercise without downloading model weights.
    """
    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")

    whisper = model or WhisperModel(model_size, device="cpu", compute_type="int8")
    transcribe_segments, info = whisper.transcribe(
        str(path),
        task="transcribe",
        language=language,
        beam_size=3,
        vad_filter=True,
    )
    transcript = " ".join(segment.text.strip() for segment in transcribe_segments).strip()

    # faster-whisper's translate task returns English speech text for supported
    # non-English audio. Reuse the detected language so both passes are aligned.
    translation_segments, _ = whisper.transcribe(
        str(path),
        task="translate",
        language=info.language,
        beam_size=3,
        vad_filter=True,
    )
    translation = " ".join(segment.text.strip() for segment in translation_segments).strip()

    return TranscriptionResult(
        transcript=transcript,
        translation=translation,
        detected_language=info.language,
    )


def save_transcription(result: TranscriptionResult, output_path: str | Path) -> Path:
    """Save both original-language transcript and English translation."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        f"Detected language: {result.detected_language}\n\n"
        f"Transcript\n{result.transcript}\n\n"
        f"English translation\n{result.translation}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path
