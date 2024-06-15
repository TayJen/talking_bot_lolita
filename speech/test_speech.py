from speech.recorder import get_mic_source, get_model, get_recorder
from speech.recorder import start_recording, transcription_queue


def main():
    source = get_mic_source()
    recorder = get_recorder()
    audio_model = get_model()

    start_recording(source, recorder, audio_model)

    while True:
        if not transcription_queue.empty():
            # combine text data from queue
            transcription = ",".join(transcription_queue.queue())
            transcription_queue.queue.clear()
            print(transcription)


if __name__ == "__main__":
    main()
