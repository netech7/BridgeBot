# translate.py
from deep_translator import GoogleTranslator
from langdetect import detect

def translate_to_english(text):
    try:
        lang = detect(text)
        if lang == 'en':
            return text, lang
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated, lang
    except Exception as e:
        print(f"Translation to English failed: {e}")
        return text, 'en'

def translate_from_english(text, target_lang):
    if target_lang == 'en':
        return text
    try:
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Translation from English failed: {e}")
        return text
