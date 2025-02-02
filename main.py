import random
from gpt import add_user_message, generate_fish_message, add_system_message
from stt import listen_stt
from tts import simple_tts
import movement
from movement import gpio_start, flap_forward, flap_backward, flap_neutral, mouth_open, mouth_close, mouth_neutral, gpio_cleanup
import time

scenes = [
    # "You seem to face death himself, the vampire, Nosferatu.",
    "An intruder has entered your place.",
    # "A storm is approaching.",
    # "A young sailor seeks your advice.",
    # "You encounter a rival captain at a tavern.",
    # "You encounter a ghost ship at sea.",
]

def verbose(msg):
    pass
    # print(msg)

def loop():

    scene = scenes[random.randint(0, len(scenes)-1)]
    print(f"Scene: {scene}")
    add_system_message(scene)

    gpio_start()

    while True:

        verbose("[Requesting GPT]")      
        message = ""
        for chunk in generate_fish_message():
            message += chunk

            if random.uniform(0, 1) < 0.2:
                if random.uniform(0, 1) < 0.5:
                    flap_forward()
                else:
                    flap_backward()


        # print(f"Fish: {message}")

        # filter commas they mess up the TTS
        message = message.replace(',', '')

        verbose("[Starting TTS]")      
        print(f"Fish: ", end='', flush=True)

        def on_spoken_word(text):
            if random.uniform(0, 1) < 0.7:
                mouth_open()
            else:
                mouth_close()
            print(text, end=' ', flush=True)

        flap_forward()

        # start the tts
        simple_tts(message, on_spoken_word)
        print('')

        mouth_close()
        mouth_neutral()

        verbose("[Starting STT]")      
        while True:
            utterance = listen_stt()

            if utterance is not None and len(utterance) > 0:
                # received input
                print(f"User: {utterance}")
                add_user_message(utterance)
                break

            elif random.uniform(0, 1) < 0.3:
                # didn't hear anything
                # the fish is impatient and answers before user
                msg = "No answer is returned."
                verbose(f"Scene: {msg}")
                add_system_message(msg)
                break

            print("...")

        # # demo user input
        # user_input = input("User: ")
        # add_user_message(user_input)



if __name__ == "__main__":  
  try:
    loop()
  except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    print("Program interrupted")
  finally:
    gpio_cleanup()