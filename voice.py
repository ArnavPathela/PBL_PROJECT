import speech_recognition as sr
import pyttsx3
import requests
import time
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()

BASE_URL = "http://127.0.0.1:5000"
NLU_URL = "http://127.0.0.1:8000/nlu"

GLOBAL_SESSION = None


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen_for_command(prompt):
    print(prompt)
    speak(prompt)
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return None


def nlu_parse(utterance: str) -> dict:
    try:
        r = requests.post(NLU_URL, json={"utterance": utterance}, timeout=3)
        if r.ok:
            return r.json()
    except Exception as e:
        print("NLU error:", e)
    return {}


def login_via_voice():
    global GLOBAL_SESSION

    speak("Please provide your email address for login.")
    email = listen_for_command("Say your email address.")
    if not email:
        speak("Sorry, I could not hear the email. Try again.")
        return

    speak("Now provide your password.")
    password = listen_for_command("Say your password.")
    if not password:
        speak("Sorry, I could not hear the password. Try again.")
        return

    login_url = f"{BASE_URL}/custlogin"
    dash_url = f"{BASE_URL}/customerdash"

    session = requests.Session()

    # initialize session
    session.get(login_url)

    # submit credentials and follow redirects
    response = session.post(
        login_url,
        data={"email": email, "password": password},
        allow_redirects=True
    )

    print("Final URL:", response.url)
    print("Status:", response.status_code)
    print("Cookies:", session.cookies.get_dict())

    if response.url.endswith("/customerdash"):
        speak("Login successful.")
        GLOBAL_SESSION = session
    else:
        speak("Login failed. Please check your credentials and try again.")


def start_voice_assistant():
    global GLOBAL_SESSION

    while True:
        command = listen_for_command("Listening for a command...")
        if not command:
            speak("Sorry, I did not catch that.")
            continue

        print(f"Command received: {command}")

        if "login" in command:
            login_via_voice()

        elif "exit" in command:
            speak("Goodbye.")
            break

        else:
            nlu = nlu_parse(command)
            print("NLU Output:", nlu)
            speak("Sorry, I don't understand that command yet.")


def main():
    print("Listening for 'hello ai' to start.")
    while True:
        command = listen_for_command("Say 'hello ai' to begin.")
        if command and "hello ai" in command:
            speak("Hello, how can I assist you today?")
            start_voice_assistant()


if __name__ == "__main__":
    main()
