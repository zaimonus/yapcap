import wave
from collections import deque
from datetime import datetime
from pathlib import Path

import numpy as np
import sounddevice as sd
import typer
from rich.console import Console
from rich.text import Text

# Parameters
DEFAULT_SAMPLERATE = 44100  # 44.1 kHz for quality
DEFAULT_SECONDS = 180  # 3 minutes
CHANNELS = 1  # Mono = 1, Stereo = 2

console = Console()


def log(*objects: Text, end: str = "\n"):
    time = datetime.now().strftime("[%X]")
    display_time = Text(time, style="blue")
    console.print(display_time, end=" ")
    console.print(*objects, end=end)


def start_recording(output_dir: Path, seconds: int, samplerate: int):
    # Ringbuffer for PCM Samples
    buffer = deque(maxlen=samplerate * seconds * CHANNELS)

    def callback(indata, frames, time, status):
        if status:
            log(Text(str(status)))  # Warnings on overruns/underruns
        buffer.extend(indata.flatten())

    # start audio-stream
    with sd.InputStream(channels=CHANNELS, samplerate=samplerate, callback=callback):
        console.rule("[red]WARNING[/]", style="red")
        console.print(
            "\n".join(
                [
                    "This tool is intended for use only with the consent of all participants.",
                    "Recording people without their knowledge or consent may be illegal or unethical.",
                    "So please make sure everyone involved has agreed to be recorded.",
                ]
            ),
            justify="center",
        )
        console.rule(style="red")

        log(Text("Start recording ..."))

        running = True
        while running:
            try:
                log(
                    Text("Press"),
                    Text("ENTER", "purple"),
                    Text("to save clip ..."),
                )
                log(
                    Text("Press"),
                    Text("CTRL+C", "purple"),
                    Text("or"),
                    Text("CTRL+D", "purple"),
                    Text("to exit ..."),
                    end="",
                )
                inp = console.input()
            except KeyboardInterrupt:
                running = False
                continue

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

                log(Text("Clip saved under"), Text(str(filename), "bold yellow"))


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
