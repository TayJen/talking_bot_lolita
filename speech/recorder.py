from datetime import datetime, timedelta
from queue import Queue
from time import sleep

import numpy as np
import torch
import whisper
from speech_recognition import AudioData, Recognizer, Microphone

MICROPHONE_NAME = "MacBook Pro Microphone"
MODEL_NAME = "small.en"
RECORD_TIMEOUT = 2
PHRASE_TIMEOUT = 3

audio_queue = Queue()
transcription_queue = Queue()


def get_mic_source() -> Microphone:
    for mic_index, mic_name_available in enumerate(Microphone.list_microphone_names()):
        if MICROPHONE_NAME in mic_name_available:
            source = Microphone(sample_rate=16000, device_index=mic_index)
            break
    else:
        raise Exception(f"No microphone named {MICROPHONE_NAME}")
    return source


def get_recorder() -> Recognizer:
    recorder = Recognizer()
    recorder.energy_threshold = 1000  # how loud should be the voice
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically
    # to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False
    return recorder


def get_model() -> whisper.Whisper:
    audio_model = whisper.load_model("small.en")
    print("Model loaded.\n")
    return audio_model


def start_recording(source: Microphone, recorder: Recognizer, audio_model: whisper.Whisper):
    def record_callback(_, audio: AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        audio_queue.put(data)

    with source:
        recorder.adjust_for_ambient_noise(source)

    recorder.listen_in_background(source, record_callback, phrase_time_limit=RECORD_TIMEOUT)
    phrase_time = None

    while True:
        now = datetime.utcnow()
        # Pull raw recorded audio from the queue.
        if not audio_queue.empty():
            phrase_complete = False
            # If enough time has passed between recordings, consider the phrase complete.
            # Clear the current working audio buffer to start over with the new data.
            if phrase_time and now - phrase_time > timedelta(seconds=PHRASE_TIMEOUT):
                phrase_complete = True
            # This is the last time we received new audio data from the queue.
            phrase_time = now

            # Combine audio data from queue
            audio_data = b"".join(audio_queue.queue)
            audio_queue.queue.clear()

            # Convert in-ram buffer to something the model can use directly without needing a temp file.
            # Convert data from 16-bit wide integers to floating point with a width of 32 bits.
            # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            # Read the transcription.
            result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
            text = result["text"].strip()

            # If we detected a pause between recordings, add a new item to our transcription.
            # Otherwise, edit the existing one.
            if phrase_complete:
                transcription_queue.put(text)
        else:
            # Infinite loops are bad for processors, must sleep.
            sleep(0.25)
