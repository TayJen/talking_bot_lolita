# Own Jarvis

## Installation (macOS only!)

### Download the weights
https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/blob/main/codellama-7b.Q4_0.gguf

and put them into `weights` folder

### Install libraries

```
python -m venv venv
source venv/bin/activate
CMAKE_ARGS="-DLLAMA_METAL=on" pip install -U llama-cpp-python --no-cache-dir
pip install -r requirements.txt
```

First start up will be the longest, as the whisper model must be downloaded. After that the startup takes approx 5-10 seconds.

To start the bot run:

```
python main.py
```

## What's done

Several modules have been implemented:
- `llama.c` as the main LLM
- `say` macOS command as the main TTS (text-to-speech)
- `whisper` as the realtime speech recognizer STT (speech-to-text)
- `langchain` as the agent workflow with prompt template and chat history

## Further improvements

These issues are unresolved for now:
- Interrupt the saying command (the model can't be interrupted)
- More context (llama2 prefix-match limit is being hit fast)
- Better model with more compute (for now quantized llama is a little bit hallucinative)
