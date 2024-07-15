import pygame
import sys
import os
import threading
from gtts import gTTS
import speech_recognition as sr

# Initialize Pygame
pygame.init()

language = 'en'
r = sr.Recognizer()

# Define button mappings for DualSense
BUTTON_SQUARE = 0 
BUTTON_X = 1 
BUTTON_CIRCLE = 2 
BUTTON_TRIANGLE = 3
BUTTON_L1 = 4
BUTTON_R1 = 5
BUTTON_L2 = 6
BUTTON_R2 = 7
BUTTON_SHARE = 8
BUTTON_OPTIONS = 9
BUTTON_L3 = 10
BUTTON_R3 = 11
BUTTON_PS = 12
BUTTON_TOUCHPAD = 13
BUTTON_MICROPHONE = 14

button_names = {
    BUTTON_SQUARE: "Square",
    BUTTON_X: "X",
    BUTTON_CIRCLE: "Circle",
    BUTTON_TRIANGLE: "Triangle",
    BUTTON_L1: "L1",
    BUTTON_R1: "R1",
    BUTTON_L2: "L2",
    BUTTON_R2: "R2",
    BUTTON_SHARE: "Share",
    BUTTON_OPTIONS: "Options",
    BUTTON_L3: "L3",
    BUTTON_R3: "R3",
    BUTTON_PS: "PS",
    BUTTON_TOUCHPAD: "Touchpad",
    BUTTON_MICROPHONE: "Microphone",
}

hat_directions = {
    (0, 1): "Up",
    (0, -1): "Down",
    (-1, 0): "Left",
    (1, 0): "Right",
    (1, 1): "Up-Right",
    (1, -1): "Down-Right",
    (-1, 1): "Up-Left",
    (-1, -1): "Down-Left",
    (0, 0): "Center"
}

def capture_audio(stop_event):
    print("Adjusting for ambient noise, please wait...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise

        print("Start speaking. Press the Circle button to stop.")

        while not stop_event.is_set():
            print("Listening...")
            audio = r.listen(source)
            try:
                print(r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                print("Check your internet connection")

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('PS5 DualSense Controller Input')

# Initialize the joystick
pygame.joystick.init()

# Check if any joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected!")
    sys.exit()

# Use the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of hats: {joystick.get_numhats()}")

# Main loop
running = True
microphone_button_pressed = False
stop_event = threading.Event()
audio_thread = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            stop_event.set()
            if audio_thread:
                audio_thread.join()
        elif event.type == pygame.JOYBUTTONDOWN:
            button_name = button_names.get(event.button, f"Unknown Button {event.button}")
            p_text = f"{button_name} pressed"
            print(p_text)
            speech_object = gTTS(text=p_text, lang=language, slow=False)
            speech_object.save("prediction.mp3")
            os.system("mpg321 prediction.mp3")
            
            if event.button == BUTTON_MICROPHONE and not microphone_button_pressed:
                microphone_button_pressed = True
                stop_event.clear()
                audio_thread = threading.Thread(target=capture_audio, args=(stop_event,))
                audio_thread.start()
        
        elif event.type == pygame.JOYBUTTONUP:
            button_name = button_names.get(event.button, f"Unknown Button {event.button}")
            p_text = f"{button_name} released"
            print(p_text)
            
            if event.button == BUTTON_CIRCLE and microphone_button_pressed:
                microphone_button_pressed = False
                stop_event.set()
                if audio_thread:
                    audio_thread.join()
        
        elif event.type == pygame.JOYHATMOTION:
            hat_position = event.value
            direction = hat_directions.get(hat_position, "Unknown Direction")
            p_text = f"D-pad moved to {direction}"
            print(p_text)
    
    # Clear the screen
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
