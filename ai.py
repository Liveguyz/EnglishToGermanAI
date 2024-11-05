import os
import csv
import time
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound

# Die Verzeichnisse für die Eingabe- und Ausgabedateien
input_dir = '/Users/luka/Desktop/GitHub/EnglishToGermanAI/input'  # Klein geschrieben
output_dir = '/Users/luka/Desktop/GitHub/EnglishToGermanAI/output'  # Angepasst

def translate_text(text):
    """Übersetzt einen einzelnen Text."""
    try:
        return GoogleTranslator(source='en', target='de').translate(text)
    except TranslationNotFound:
        return text  # Bei Fehler die ursprünglichen Texte zurückgeben

def translate_batch(texts):
    """Übersetzt eine Liste von Texten in einer einzelnen Anfrage mit Threading."""
    translated_texts = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        translated_texts = list(executor.map(translate_text, texts))
    return translated_texts

def process_file(filename):
    input_file_path = os.path.join(input_dir, filename)

    if filename.endswith('.csv'):
        with open(input_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Flatten data for batch processing
        all_texts = [text for row in data for text in row if text.strip()]  # Nur nicht-leere Texte
        print(f"Gefundene Texte in {filename}: {len(all_texts)}")

        # Batch-Übersetzung
        translated_texts = translate_batch(all_texts)

        # Reformat the translated texts back to their original structure
        translated_data = []
        for i in range(0, len(translated_texts), len(data[0])):
            translated_data.append(translated_texts[i:i + len(data[0])])

        output_file_path = os.path.join(output_dir, filename)
        with open(output_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(translated_data)
            print(f"Ausgabedatei erstellt: {output_file_path}")

if __name__ == '__main__':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Filtern der Dateien im Input-Verzeichnis
    valid_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    print("Gefundene CSV-Dateien im Input-Verzeichnis:", valid_files)

    start_time = time.time()  # Startzeit erfassen

    for filename in valid_files:
        process_file(filename)

    end_time = time.time()  # Endzeit erfassen
    elapsed_time = end_time - start_time  # Verstrichene Zeit berechnen
    print(f"Übersetzung abgeschlossen! Zeit für die Übersetzung: {elapsed_time:.2f} Sekunden")