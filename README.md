# 🎙️ YapCap - The Audio Buffer Recorder

Ever wished you could save audio *after* something interesting already happened?
This little Python tool has your back 😄

It continuously records audio into a rolling **3-minute buffer**.
When you press **Enter**, the last 3 minutes are instantly saved as a `.wav` file.
Recording then continues like nothing happened.

Perfect for “wait, I should’ve recorded that” moments ✨

## ✨ Features

* 🎧 Continuous audio recording
* ⏱️ Rolling buffer of the last **3 minutes**
* ⌨️ Press **Enter** to save the buffer to a `.wav` file
* 📂 Clips are stored in a directory you choose
* 🔁 Keeps recording after each save

## 📦 Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management 🚀

1. Install `uv` (if you haven’t already):

    ```bash
    pip install uv
    ```

2. a) Create and sync the environment:

    ```bash
    uv sync
    ```

    b) Or just install the local repo with `uv tool`:

    ```bash
    uv tool install .
    ```

## ▶️ Usage

Run the script and tell it **where to save your clips**:

```bash
# When inside this repo, you can do
uv run yapcap clips/

# If you have installed it with uv tools, you can simply do
yapcap clips/
```

What happens next:

1. Recording starts immediately 🎶
2. Audio is continuously buffered (last 3 minutes)
3. Press **Enter ⏎** at any time
4. The buffered audio is saved as a `.wav` file in `clips/`
5. Recording continues automatically 🔄

## ⚙️ Options

You can also change the **duration** (in seconds) and the **samplerate** (in Hz):

```bash
# buffer and save the last 10 minutes
yapcap clips/ --seconds 600

# use an adequate rate for speech (according to the audacity manual)
yapcap clips/ --samplerate 32000
```

See more about sample rates on [Audacity Manual - Sample Rates](https://manual.audacityteam.org/man/sample_rates.html).
