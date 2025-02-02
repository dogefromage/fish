import azure.cognitiveservices.speech as speechsdk

from api_keys import azure_region, azure_key

speech_config = speechsdk.SpeechConfig(region=azure_region, subscription=azure_key)

models = [
    "en-US-ChristopherNeural",
    "en-US-AndrewNeural", # fish-like
    "en-US-DavisNeural", # whispers
    "en-US-TonyNeural", # boy-ish
    
    "en-GB-OllieMultilingualNeural", # narrator
]

def simple_tts(text, on_word_boundary):
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config)

    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="en-GB-OllieMultilingualNeural">
            <prosody rate="1.2" pitch="-0.1st">
                <mstts:express-as style="angry" styledegree="3">
                    {text}
                </mstts:express-as>
            </prosody>
        </voice>
    </speak>
    """

    def word_boundary_event(event):
        # print(f"Word: {event.text}, Offset: {event.audio_offset / 10000} ms")
        on_word_boundary(event.text)

    speech_synthesizer.synthesis_word_boundary.connect(word_boundary_event)

    result = speech_synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("TTS canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

