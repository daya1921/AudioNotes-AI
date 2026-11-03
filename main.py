"""AudioNotes-AI desktop app: record audio and create local AI notes."""

from __future__ import annotations

import queue
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
import soundcard as sc
import soundfile as sf

from transcription.transcribe import TranscriptionResult, save_transcription, transcribe_audio


ROOT = Path(__file__).resolve().parent
RECORDINGS = ROOT / "recordings"
TRANSCRIPTS = ROOT / "notes"
SAMPLE_RATE = 16_000
CHUNK_SECONDS = 3


class AudioNotesApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("AudioNotes AI")
        self.root.geometry("760x590")
        self.root.minsize(580, 440)
        self.root.configure(bg="#f4f6f8")

        self.devices: list[object] = []
        self.device_names: list[str] = []
        self.selected_device = tk.StringVar()
        self.status = tk.StringVar(value="Choose an audio source and start recording.")
        self.stop_event = threading.Event()
        self.messages: queue.Queue[tuple[str, object]] = queue.Queue()
        self.busy = False

        self._build_ui()
        self.refresh_devices()
        self.root.after(100, self._poll_messages)

    def _build_ui(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6f8")
        style.configure("TLabel", background="#f4f6f8", foreground="#17212b")
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Hint.TLabel", foreground="#576574")
        style.configure("TButton", padding=(12, 8))

        frame = ttk.Frame(self.root, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="AudioNotes AI", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            frame,
            text="Record Hindi audio, then create a transcript and English translation on this PC.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(4, 18))

        source_row = ttk.Frame(frame)
        source_row.pack(fill="x", pady=(0, 12))
        ttk.Label(source_row, text="Audio source").pack(side="left", padx=(0, 10))
        self.device_box = ttk.Combobox(
            source_row, textvariable=self.selected_device, state="readonly", width=58
        )
        self.device_box.pack(side="left", fill="x", expand=True)
        self.refresh_button = ttk.Button(source_row, text="Refresh", command=self.refresh_devices)
        self.refresh_button.pack(side="left", padx=(8, 0))

        action_row = ttk.Frame(frame)
        action_row.pack(fill="x", pady=(0, 12))
        self.start_button = ttk.Button(action_row, text="Start recording", command=self.start_recording)
        self.start_button.pack(side="left")
        self.stop_button = ttk.Button(
            action_row, text="Stop and make notes", command=self.stop_recording, state="disabled"
        )
        self.stop_button.pack(side="left", padx=8)
        ttk.Label(action_row, textvariable=self.status, style="Hint.TLabel").pack(
            side="left", padx=10
        )

        ttk.Label(frame, text="Transcript and translation").pack(anchor="w", pady=(4, 6))
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill="both", expand=True)
        self.output = tk.Text(
            text_frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg="white",
            fg="#17212b",
            relief="flat",
            padx=12,
            pady=12,
        )
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        ttk.Label(
            frame,
            text="Audio processing runs locally. The first run downloads the Whisper Base model (~150 MB).",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(10, 0))

    def refresh_devices(self) -> None:
        try:
            self.devices = sc.all_microphones(include_loopback=True)
            self.device_names = [
                f"{device.name}  ({'system audio' if device.isloopback else 'microphone'})"
                for device in self.devices
            ]
            self.device_box["values"] = self.device_names
            if self.device_names:
                default = None
                try:
                    default = sc.default_microphone()
                except Exception:
                    pass
                selected = next(
                    (i for i, device in enumerate(self.devices) if device is default), 0
                )
                self.device_box.current(selected)
                self.status.set("Ready to record.")
            else:
                self.selected_device.set("")
                self.status.set("No audio sources found. Connect a microphone and refresh.")
        except Exception as exc:
            self.status.set(f"Could not list audio sources: {exc}")

    def start_recording(self) -> None:
        index = self.device_box.current()
        if index < 0 or index >= len(self.devices):
            messagebox.showerror("Audio source needed", "Select an available audio source first.")
            return
        self.stop_event.clear()
        self.busy = True
        self.start_button.configure(state="disabled")
        self.refresh_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status.set("Recording… click Stop and make notes when finished.")
        device = self.devices[index]
        threading.Thread(target=self._record_and_transcribe, args=(device,), daemon=True).start()

    def stop_recording(self) -> None:
        self.stop_event.set()
        self.stop_button.configure(state="disabled")
        self.status.set("Finishing the recording…")

    def _record_and_transcribe(self, device: object) -> None:
        try:
            chunks: list[np.ndarray] = []
            with device.recorder(samplerate=SAMPLE_RATE) as recorder:
                while not self.stop_event.is_set():
                    chunk = recorder.record(numframes=SAMPLE_RATE * CHUNK_SECONDS)
                    if len(chunk):
                        chunks.append(np.asarray(chunk))
            if not chunks:
                raise RuntimeError("No audio was captured. Check the selected source and try again.")

            audio = np.concatenate(chunks, axis=0)
            if audio.ndim == 2:
                audio = audio.mean(axis=1)
            RECORDINGS.mkdir(parents=True, exist_ok=True)
            TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = RECORDINGS / f"recording_{stamp}.wav"
            note_path = TRANSCRIPTS / f"notes_{stamp}.txt"
            sf.write(audio_path, audio, SAMPLE_RATE)
            self.messages.put(("status", "Audio saved. Loading the local speech model…"))
            result = transcribe_audio(audio_path)
            save_transcription(result, note_path)
            self.messages.put(("success", (result, audio_path, note_path)))
        except Exception as exc:
            self.messages.put(("error", str(exc)))

    def _poll_messages(self) -> None:
        try:
            while True:
                kind, payload = self.messages.get_nowait()
                if kind == "status":
                    self.status.set(str(payload))
                elif kind == "success":
                    result, audio_path, note_path = payload  # type: ignore[misc]
                    self._show_result(result)
                    self.status.set(f"Saved notes: {note_path.name}")
                    messagebox.showinfo(
                        "Notes ready",
                        f"Transcript and English translation saved.\n\nAudio: {audio_path}\nNotes: {note_path}",
                    )
                    self._set_ready()
                elif kind == "error":
                    self.status.set("Recording or transcription failed.")
                    messagebox.showerror("AudioNotes AI", str(payload))
                    self._set_ready()
        except queue.Empty:
            pass
        self.root.after(100, self._poll_messages)

    def _show_result(self, result: TranscriptionResult) -> None:
        self.output.delete("1.0", "end")
        self.output.insert(
            "end",
            f"Detected language: {result.detected_language}\n\n"
            f"TRANSCRIPT\n{result.transcript}\n\n"
            f"ENGLISH TRANSLATION\n{result.translation}\n",
        )

    def _set_ready(self) -> None:
        self.busy = False
        self.start_button.configure(state="normal")
        self.refresh_button.configure(state="normal")
        self.stop_button.configure(state="disabled")


def main() -> None:
    root = tk.Tk()
    AudioNotesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
