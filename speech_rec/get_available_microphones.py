import speech_recognition as sr

if __name__ == "__main__":
    print("Available microphone devices are: ")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f'Microphone with name "{name}" found')
