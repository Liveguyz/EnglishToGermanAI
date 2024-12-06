import pandas as pd
from transformers import MarianMTModel, MarianTokenizer

# Funktion zum Übersetzen von Text
def translate(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Lade das Modell und den Tokenizer
model_name = "Helsinki-NLP/opus-mt-en-de"  # Englisch zu Deutsch
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Lese die CSV-Datei
input_csv = "input.csv"  # Pfad zur Eingabedatei
output_csv = "translated_output.csv"  # Pfad zur Ausgabedatei
df = pd.read_csv(input_csv)

# Überprüfen, ob die 'text' Spalte existiert
if 'text' not in df.columns:
    raise ValueError("Die CSV-Datei muss eine 'text' Spalte enthalten.")

# Übersetze den Text in der 'text' Spalte
df['translated_text'] = df['text'].apply(translate)

# Speichere die übersetzte CSV-Datei
df.to_csv(output_csv, index=False)

print(f"Die Übersetzung wurde in '{output_csv}' gespeichert.")