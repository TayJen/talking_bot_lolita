import asyncio

from answer_bot.agent import chain
from answer_bot.utils import cleaning_text
from speech_gen.macos_say import pronounce_text
from speech_rec.recorder import get_mic_source, get_recorder, get_model, start_recording


async def get_queue_msg(transcription_queue: asyncio.Queue):
    while True:
        # Get answer from the queue from recording
        msg = await transcription_queue.get()
        print(f"\nGot message: {msg}\n")

        # Get answer from chain with the chat history
        answer = chain.predict(input=msg)

        # Clean it from tags like < >
        clean_answer = cleaning_text(answer)
        print(clean_answer)

        # TTS
        pronounce_text("woman", clean_answer)


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
