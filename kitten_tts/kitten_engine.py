import logging
import numpy as np
import asyncio

_LOGGER = logging.getLogger(__name__)

class KittenEngine:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tts = None
        self.sample_rate = 24000
        self.available_voices = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']

    def load(self):
        _LOGGER.info(f"Loading KittenTTS model: {self.model_name}...")

        from kittentts import KittenTTS

        self.tts = KittenTTS(self.model_name)
        _LOGGER.info(f"KittenTTS engine ready. Sample rate: {self.sample_rate}Hz")

    async def synthesize(self, text: str, voice_name: str):

        if self.tts is None:
            raise RuntimeError("Engine is not loaded!")
        
        if voice_name not in self.available_voices:
            _LOGGER.warning(f"Voice '{voice_name}' not found, falling back to {self.available_voices[0]}")
            voice_name = self.available_voices[0]

        audio_array = await asyncio.to_thread(self.tts.generate, text, voice=voice_name)

        if audio_array is None or len(audio_array) == 0:
            return b""

        audio_int16 = (audio_array * 32767).astype(np.int16)
        
        return audio_int16.tobytes()