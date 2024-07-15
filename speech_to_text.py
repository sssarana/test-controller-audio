import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Use a loop to keep capturing audio
try:
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise

        print("Start speaking. Press Ctrl+C to stop.")

        while True:
            #print("Say something!")
            audio = r.listen(source)

            try:
                print(r.recognize_google(audio))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                print("Check your internet connection")

except KeyboardInterrupt:
    print("\nStopped by user")
except Exception as e:
    print(f"An error occurred: {e}")
