from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
import os
import time
from datetime import datetime
import webbrowser

r = sr.Recognizer()

def speak(text):
    print("Asistan:", text)
    tts = gTTS(text=text, lang="tr")
    file = "answer.mp3"
    tts.save(file)
    playsound(file)
    os.remove(file)

def record(prompt=False):
    with sr.Microphone() as source:
        if prompt:
            speak(prompt)
        print("Dinleniyor...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            voice = r.recognize_google(audio, language="tr-TR")
            print("Sen:", voice)
            return voice.lower()
        except sr.WaitTimeoutError:
            print("Zaman aşımı: Konuşma algılanmadı.")
            return ""
        except sr.UnknownValueError:
            speak("Seni anlayamadım.")
            return ""
        except sr.RequestError:
            speak("Sistem çalışmıyor.")
            return ""


def response(voice):
    if "merhaba" in voice or "selam" in voice:
        speak("Sana da merhaba!")
    elif "teşekkür" in voice:
        speak("Rica ederim.")
    elif "görüşürüz" in voice:
        speak("Görüşürüz, hoşça kal!")
        exit()
    elif "hangi gündeyiz" in voice:
        days = {
            "Monday": "Pazartesi",
            "Tuesday": "Salı",
            "Wednesday": "Çarşamba",
            "Thursday": "Perşembe",
            "Friday": "Cuma",
            "Saturday": "Cumartesi",
            "Sunday": "Pazar"
        }
        today = time.strftime("%A")
        speak(f"Bugün {days.get(today, today)}.")
    elif "saat kaç" in voice:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"Şu an saat {current_time}")
    elif "google'da ara" in voice:
        search = record("Ne aramamı istersin?")
        if search:
            url = f"https://www.google.com/search?q={search}"
            webbrowser.open(url)
            speak(f"{search} için Google'da bulabildiklerimi listeliyorum.")
    else:
        speak("Bunu henüz bilmiyorum.")

def main():
    speak("Charlie hazır, komutunu bekliyorum.")
    while True:
        voice = record()
        if "charlie" in voice:
            playsound("Ding.mp3")
            command = record("Seni dinliyorum.")
            if command:
                response(command)

if __name__ == "__main__":
    main()
