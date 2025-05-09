import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import requests
from bs4 import BeautifulSoup

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Flask server URL
BASE_URL = "http://127.0.0.1:5000"

def speak(text):
    """
    Converts text to speech.
    """
    engine.say(text)
    engine.runAndWait()

def open_page(page):
    """
    Opens the specified page in the default web browser.
    """
    url = f"{BASE_URL}/{page}"
    webbrowser.open(url, new=0)  # `new=0` opens in the same tab
    time.sleep(2)  # Allow time for the page to load

def listen_for_command(prompt):
    """
    Listens for a voice command and returns the recognized text.
    """
    print(prompt)
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return None

def start_voice_assistant():
    """
    Main assistant loop that processes commands.
    """
    while True:
        command = listen_for_command("Listening for a command...")
        if not command:
            print("Could not understand the command. Please try again.")
            continue

        print(f"Command received: {command}")

        # Process commands
        if "home" in command:
            speak("Redirecting you to the home page.")
            open_page("home")

        elif "logout" in command:
            speak("Logging you out.")
            open_page("logout")

        elif "login" in command:
            speak("Redirecting you to the login page.")
            open_page("custlogin")
            # After opening the login page, start the login process
            login_via_voice()

        elif "register" in command:
            speak("Redirecting you to the registration page.")
            open_page("custreg")

        elif "book service" in command:
            speak("Redirecting you to booking a service page.")
            open_page("bookservice")
        
        elif "booked services" in command:
            speak("Redirecting you to your bookings.")
            open_page("bookedservice")

        elif "feedback" in command:
            speak("Redirecting you to the feedback page.")
            open_page("custprofeed")
       
        elif "exit" in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that command.")

def login_via_voice():
    """
    Automates the login process using voice commands for email and password.
    """
    speak("Please provide your email address for login.")
    email = listen_for_command("Please say your email address.")
    if not email:
        speak("Sorry, I couldn't hear the email. Try again.")
        return

    speak(f"Received email: {email}. Now, please provide your password.")
    password = listen_for_command("Please say your password.")
    if not password:
        speak("Sorry, I couldn't hear the password. Try again.")
        return

    # Flask login URL
    login_url = f"{BASE_URL}/custlogin"

    # Use a session to handle cookies
    with requests.Session() as session:
        # Debugging: Log cookies before and after the request
        print("Initial cookies:", session.cookies.get_dict())

        # Send POST request to login
        response = session.post(login_url, data={'email': email, 'password': password})

        # Debugging: Log cookies after the POST request
        print("Cookies after login:", session.cookies.get_dict())

        if response.status_code == 200 and "/home" in response.url:
            speak("Login successful. Redirecting to the home page.")
            open_page("home")
        else:
            speak("Login failed. Please check your credentials.")
            print("Login failed response:", response.text)




def main():
    """
    Entry point for the assistant.
    """
    print("Listening for 'hello ai'...")
    while True:
        command = listen_for_command("Listening for 'hello ai'...")
        if command and "hello ai" in command:
            speak("Hello, how can I assist you today?")
            start_voice_assistant()

if __name__ == "__main__":
    main()
