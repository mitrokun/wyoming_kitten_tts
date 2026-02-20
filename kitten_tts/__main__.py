import argparse
import asyncio
import logging
from functools import partial
import os


from wyoming.info import Attribution, Info, TtsProgram, TtsVoice
from wyoming.server import AsyncServer

from .kitten_engine import KittenEngine
from .handler import KittenEventHandler

_LOGGER = logging.getLogger(__name__)
__version__ = "0.8.0"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", default="tcp://0.0.0.0:10211", help="Server URI")
    parser.add_argument("--model", default="KittenML/kitten-tts-nano-0.8", help="HuggingFace model ID")
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    parser.add_argument("--log-format", default="%(asctime)s %(levelname)s:%(name)s:%(message)s", help="Log format")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format)

    _LOGGER.info("Initializing Kitten Engine...")
    engine = KittenEngine(model_name=args.model)
    
    try:
        engine.load()
    except Exception as e:
        _LOGGER.critical(f"Failed to load engine: {e}")
        return

    wyoming_voices = []
    for voice_id in engine.available_voices:
        wyoming_voices.append(
            TtsVoice(
                name=voice_id,
                description=f"{voice_id}",
                attribution=Attribution(name="KittenML", url="https://github.com/KittenML/KittenTTS"),
                installed=True,
                version=__version__,
                languages=["en"],
            )
        )

    wyoming_info = Info(
        tts=[
            TtsProgram(
                name="KittenTTS",
                description="KittenTTS Wyoming Server",
                attribution=Attribution(name="KittenML", url="https://github.com/KittenML/KittenTTS"),
                installed=True,
                version=__version__,
                supports_synthesize_streaming=True,
                voices=wyoming_voices,
            )
        ],
    )

    server = AsyncServer.from_uri(args.uri)
    _LOGGER.info(f"Server ready at {args.uri}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(
            server.run(
                partial(
                    KittenEventHandler,
                    wyoming_info,
                    args,
                    engine,
                )
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

def run():
    main()

if __name__ == "__main__":

    run()
