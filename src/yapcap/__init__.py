import wave
from collections import deque
from datetime import datetime
from pathlib import Path

import numpy as np
import sounddevice as sd
import typer

# Parameters
DEFAULT_SAMPLERATE = 44100  # 44.1 kHz for quality
DEFAULT_SECONDS = 180  # 3 minutes
CHANNELS = 1  # Mono = 1, Stereo = 2


def start_recording(output_dir: Path, seconds: int, samplerate: int):
    # Ringbuffer for PCM Samples
    buffer = deque(maxlen=samplerate * seconds * CHANNELS)

    def callback(indata, frames, time, status):
        if status:
            print(status)  # Warnings on overruns/underruns
        buffer.extend(indata.flatten())

    # start audio-stream
    with sd.InputStream(channels=CHANNELS, samplerate=samplerate, callback=callback):
        print("Start recording...")
        running = True
        while running:
            try:
                inp = input("Press ENTER to save, CTRL+C to exit...")
            except KeyboardInterrupt:
                inp = "\n"
                running = False
            if inp == "":
                # copy data to not block the buffer
                data = np.array(buffer, dtype=np.float32)
                buffer.clear()

                # create file name with timestamp
                filename = output_dir / datetime.now().strftime(
                    "clip_%Y-%m-%d_%H-%M-%S.wav"
                )
                with wave.open(str(filename), "wb") as f:
                    f.setnchannels(CHANNELS)
                    f.setsampwidth(2)  # 16-bit
                    f.setframerate(samplerate)
                    f.writeframes((data * 32767).astype(np.int16).tobytes())
                print(f"Clip saved under {filename}")


app = typer.Typer()


@app.command()
def record(
    directory: Path,
    seconds: int = DEFAULT_SECONDS,
    samplerate: int = DEFAULT_SAMPLERATE,
):
    """
    Record audio and save buffered clips to DIRECTORY.
    """
    directory.mkdir(parents=True, exist_ok=True)

    start_recording(directory, seconds, samplerate)


if __name__ == "__main__":
    app()
