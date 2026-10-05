"""VisionMate AI - a simple voice-based assistant for visually impaired people."""

import datetime
import webbrowser

import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 150)  # speaking speed (lower = slower)
recognizer = sr.Recognizer()


def speak(text):
    """Print and speak the given text."""
    print("VisionMate:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen from the microphone and return the text (lowercase)."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
            text = recognizer.recognize_google(audio)
            print("You:", text)
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I did not understand. Please say that again.")
            return ""
        except sr.RequestError:
            speak("Internet connection problem. Please check your network.")
            return ""


def handle_command(command):
    """Run an action based on the spoken command. Returns False to stop."""
    if not command:
        return True

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "date" in command or "day" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")

    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What should I search for?")

    elif "help" in command:
        speak("You can ask me the time, the date, or say search followed by a topic. "
              "Say exit to close.")

    elif "exit" in command or "stop" in command or "bye" in command:
        speak("Goodbye. Take care.")
        return False

    else:
        speak("I can not do that yet. Say help to know what I can do.")

    return True


def main():
    speak("Hello, I am VisionMate. Say help to know what I can do.")
    running = True
    while running:
        command = listen()
        running = handle_command(command)


if __name__ == "__main__":
    main()
