import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import requests
import json
import pyautogui
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import wikipedia
import random

class BEETA:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Change to voices[1] for female voice
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1.0)
        
    
        self.app_paths = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
            'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
            'vlc': r'C:\Program Files\VideoLAN\VLC\vlc.exe',
            'spotify': r'C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe',
            'vscode': r'C:\Program Files\Microsoft VS Code\Code.exe',
            'pycharm': r'C:\Program Files\JetBrains\PyCharm Community Edition\bin\pycharm64.exe'
        }
        
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'rohit07@gmail.com',
            'password': 'absc287'
        }
        
        self.speak("BEETA initialized. How can I assist you today?")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"BEETA: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice commands"""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("I couldn't understand that. Please try again.")
            return ""
        except sr.RequestError:
            self.speak("Sorry, there's an issue with the speech recognition service.")
            return ""
    
    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        self.speak(f"The current time is {time_str}")
    
    def get_date(self):
        """Get current date"""
        today = datetime.datetime.now()
        date_str = today.strftime("%B %d, %Y")
        self.speak(f"Today's date is {date_str}")
    
    def open_application(self, app_name):
        """Open applications"""
        app_name = app_name.lower()
        if app_name in self.app_paths:
            try:
                if os.path.exists(self.app_paths[app_name]):
                    subprocess.Popen(self.app_paths[app_name])
                    self.speak(f"Opening {app_name}")
                else:

                    os.system(f"start {app_name}")
                    self.speak(f"Opening {app_name}")
            except Exception as e:
                self.speak(f"Sorry, I couldn't open {app_name}")
     
        else:
            try:
                os.system(f"start {app_name}")
                self.speak(f"Opening {app_name}")
            except:
                self.speak(f"Sorry, I don't know how to open {app_name}")
    
    def close_application(self, app_name):
        """Close applications"""
        try:
            os.system(f"taskkill /f /im {app_name}.exe")
            self.speak(f"Closing {app_name}")
        except:
            self.speak(f"Couldn't close {app_name}")
    
    def web_search(self, query):
        """Perform web search"""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        self.speak(f"Searching for {query}")
    
    def play_youtube(self, query):
        """Play YouTube video"""
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        self.speak(f"Playing {query} on YouTube")
    
    def get_weather(self, city="your_city"):
        """Get weather information"""
        if self.weather_api_key == "YOUR_API_KEY_HERE":
            self.speak("Weather API key not configured. Please set up your OpenWeatherMap API key.")
            return
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                self.speak(f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius")
            else:
                self.speak("Sorry, I couldn't get the weather information")
        except:
            self.speak("Sorry, there was an error getting weather data")
    
    def take_screenshot(self):
        """Take a screenshot"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        self.speak(f"Screenshot saved as {filename}")
    
    def system_info(self):
        """Get system information"""
        import psutil
    
        cpu_percent = psutil.cpu_percent(interval=1)
    
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_percent = battery.percent
                self.speak(f"CPU usage is {cpu_percent}%, Memory usage is {memory_percent}%, Battery is at {battery_percent}%")
            else:
                self.speak(f"CPU usage is {cpu_percent}%, Memory usage is {memory_percent}%")
        except:
            self.speak(f"CPU usage is {cpu_percent}%, Memory usage is {memory_percent}%")
    
    def create_file(self, filename, content=""):
        """Create a new file"""
        try:
            with open(filename, 'w') as file:
                file.write(content)
            self.speak(f"File {filename} created successfully")
        except:
            self.speak(f"Sorry, couldn't create file {filename}")
    
    def send_email(self, to_email, subject, body):
        """Send email (requires configuration)"""
        if self.email_config['email'] == 'your_email@gmail.com':
            self.speak("Email not configured. Please set up your email credentials.")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['email'], self.email_config['password'])
            
            text = msg.as_string()
            server.sendmail(self.email_config['email'], to_email, text)
            server.quit()
            
            self.speak("Email sent successfully")
        except:
            self.speak("Sorry, couldn't send email")
    
    def wikipedia_search(self, query):
        """Search Wikipedia"""
        try:
            result = wikipedia.summary(query, sentences=2)
            self.speak(result)
        except:
            self.speak(f"Sorry, couldn't find information about {query}")
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
    
    def volume_control(self, action):
        """Control system volume"""
        if action == "up":
            pyautogui.press("volumeup")
            self.speak("Volume increased")
        elif action == "down":
            pyautogui.press("volumedown")
            self.speak("Volume decreased")
        elif action == "mute":
            pyautogui.press("volumemute")
            self.speak("Volume muted")
    
    def process_command(self, command):
        """Process voice commands"""
        command = command.lower()
        
        if any(word in command for word in ['hello', 'hi', 'hey']):
            greetings = ["Hello! How can I help you?", "Hi there! What can I do for you?", "Hey! I'm here to assist you."]
            self.speak(random.choice(greetings))
        
        elif 'time' in command:
            self.get_time()
        elif 'date' in command:
            self.get_date()
        
        elif 'open' in command:
            app = command.replace('open', '').strip()
            self.open_application(app)
        elif 'close' in command:
            app = command.replace('close', '').strip()
            self.close_application(app)
        
        elif 'search' in command or 'google' in command:
            query = command.replace('search', '').replace('google', '').strip()
            self.web_search(query)
        elif 'youtube' in command or 'play' in command:
            query = command.replace('youtube', '').replace('play', '').strip()
            self.play_youtube(query)
        
        elif 'weather' in command:
            self.get_weather()
        
        elif 'screenshot' in command:
            self.take_screenshot()
        elif 'system info' in command or 'system information' in command:
            self.system_info()
        
        elif 'volume up' in command:
            self.volume_control('up')
        elif 'volume down' in command:
            self.volume_control('down')
        elif 'mute' in command:
            self.volume_control('mute')
    
        elif 'wikipedia' in command or 'tell me about' in command:
            query = command.replace('wikipedia', '').replace('tell me about', '').strip()
            self.wikipedia_search(query)
        
        elif 'joke' in command:
            self.tell_joke()
        
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye! Have a great day!")
            return False

        else:
            responses = [
                "I didn't understand that command. Can you please repeat?",
                "Sorry, I'm not sure how to help with that.",
                "Could you please rephrase that?"
            ]
            self.speak(random.choice(responses))
        
        return True
    
    def run(self):
        """Main execution loop"""
        self.speak("BEETA is now active. Say 'exit' to stop.")
        
        while True:
            try:
                command = self.listen()
                if command:
                    if not self.process_command(command):
                        break
                
                time.sleep(1)  
                
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, there was an error. Please try again.")

if __name__ == "__main__":
    print("=== BEETA Voice Assistant ===")
    print("Initializing...")
    
    print("\nMake sure you have installed:")
    print("pip install speechrecognition pyttsx3 pyautogui requests wikipedia psutil")
    print("pip install pyaudio  # For microphone input")
    print("\nStarting JARVIS...")
    
    try:
        BEETA = BEETA()
        BEETA.run()
    except Exception as e:
        print(f"Error starting BEETA: {e}")
        print("Please make sure all required packages are installed.")
