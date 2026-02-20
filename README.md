# Wyoming [Kitten TTS](https://github.com/KittenML/KittenTTS)

We're waiting for the developers to sort out their library's dependencies (remove spacy). For now, we're using this approach.

## Installation (venv)

### 1. Clone the repository
```bash
git clone https://github.com/mitrokun/wyoming_kitten_tts
cd wyoming_kitten_tts
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
**Important:** Install the CPU-only version of PyTorch first to keep the installation light (~200MB vs 2GB+ for CUDA).

```bash
# Install Torch CPU
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install KittenTTS (Note: pip will show a version mismatch warning, this is normal)
pip install "https://github.com/KittenML/KittenTTS/releases/download/0.8/kittentts-0.8.0-py3-none-any.whl"

# Install Wyoming and other requirements
pip install wyoming sentence-stream numpy
```

### 4. Run the Server

```bash
# Start with the nano model; port 20211 is used by default
python3 -m kitten_tts --model "KittenML/kitten-tts-nano-0.8"
```
