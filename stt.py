import time
import azure.cognitiveservices.speech as speechsdk

from api_keys import azure_region, azure_key

# endpoint=f"wss://{azure_region}.tts.speech.microsoft.com/cognitiveservices/websocket/v2", 
speech_config = speechsdk.SpeechConfig(region=azure_region, subscription=azure_key)
speech_config.speech_recognition_language = 'en-US'

# Use the default microphone as the audio input
# audio_config = speechsdk.audio.AudioConfig(filename="OSR_us_000_0010_8k.wav")
# audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

def listen_stt():

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return ''
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return ''

# def create_stt_listener(on_recognizing, on_recognized):
    
#     def recognizing(event):
#         print("STT recognizing")
#         on_recognizing()

#     def recognized(event):
#         utterance = event.result.text
#         print(f"STT recognized: {utterance}")
#         on_recognized(utterance)
        

#     def canceled(event):
#         cancellation_details = speechsdk.CancellationDetails(event.result)
#         print(f'STT connection canceled. Error message: {cancellation_details.error_details}')

#     listening = False

#     def started(event):
#         listening = True
#         print('STT started')

#     def stopped(event):
#         listening = False
#         print('STT stopped')

#     speech_recognizer.recognized.connect(recognized)
#     speech_recognizer.canceled.connect(canceled)
#     speech_recognizer.recognizing.connect(recognizing)
#     speech_recognizer.session_started.connect(started)
#     speech_recognizer.session_stopped.connect(stopped)

#     def start():
#         speech_recognizer.start_continuous_recognition_async()

#     def stop():
#         speech_recognizer.stop_continuous_recognition_async()

#     def is_listening():
#         return listening

#     return start, stop, is_listening
