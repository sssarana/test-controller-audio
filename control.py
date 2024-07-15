import pygame
import sys
import os
from gtts import gTTS 

# Initialize Pygame
pygame.init()
language = 'en'

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

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            button_name = button_names.get(event.button, f"Unknown Button {event.button}")
            p_text = f"{button_name} pressed"
            print(p_text)
            speech_object = gTTS(text=p_text, lang=language, slow=False)
            speech_object.save("prediction.mp3")
            os.system("mpg321 prediction.mp3")
        
        elif event.type == pygame.JOYBUTTONUP:
            button_name = button_names.get(event.button, f"Unknown Button {event.button}")
            p_text = f"{button_name} released"
            print(p_text)
        elif event.type == pygame.JOYHATMOTION:
            hat_position = event.value
            direction = hat_directions.get(hat_position, "Unknown Direction")
            p_text = f"D-pad moved to {direction}"
            print(p_text)
    
    # Clear the screen
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
