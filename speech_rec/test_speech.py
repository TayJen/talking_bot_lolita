import asyncio
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from speech_rec.recorder import get_mic_source, get_model, get_recorder
from speech_rec.recorder import start_recording


async def get_queue_msg(transcription_queue: asyncio.Queue):
    while True:
        msg = await transcription_queue.get()
        print(f"\nGot message: {msg}\n")


async def main():
    source = get_mic_source()
    recorder = get_recorder()
    audio_model = get_model()

    transcription_queue = asyncio.Queue()

    tasks = [
        asyncio.create_task(get_queue_msg(transcription_queue)),
        asyncio.create_task(start_recording(source, recorder, audio_model, transcription_queue)),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
