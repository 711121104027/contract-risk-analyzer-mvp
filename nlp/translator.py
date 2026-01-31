import argostranslate.translate

def translate_hi_to_en(text):
    try:
        translated = argostranslate.translate.translate(text, "hi", "en")
        return translated
    except:
        return text