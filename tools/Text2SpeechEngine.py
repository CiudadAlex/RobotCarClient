import pyttsx3


class Text2SpeechEngine:

    def __init__(self, language):

        self.engine = pyttsx3.init()
        available_languages = ["en", "es"]

        if language not in available_languages:
            raise Exception(f"Unrecognized language: {language}. Available languages: {available_languages}")

        if "en" == language:
            voice_id = self.find_voice_id_by_language("English")
            self.engine.setProperty('voice', voice_id)
        elif "es" == language:
            voice_id = self.find_voice_id_by_language("Spanish")
            self.engine.setProperty('voice', voice_id)

    def find_voice_id_by_language(self, language_name):

        for voice in self.engine.getProperty('voices'):

            if language_name.lower() in voice.name.lower():
                print("Using voice: " + str(voice))
                return voice.id

    def say(self, text):

        self.engine.say(text)
        self.engine.runAndWait()
