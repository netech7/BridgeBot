# test_translation.py
from translate import translate_to_english, translate_from_english

test_texts = [
    "こんにちは",          # Japanese
    "आप कैसे हैं?",        # Hindi
    "तुम कसे आहात?",       # Marathi
    "Hello, how are you?"  # English
]

for text in test_texts:
    translated, lang = translate_to_english(text)
    back = translate_from_english(translated, lang)
    print(f"Original: {text}\nDetected Lang: {lang}\nTranslated to English: {translated}\nBack to original: {back}\n---")
