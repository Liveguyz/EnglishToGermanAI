import os
import csv
import json
import time
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound

input_dir = 'Input'
output_dir = 'Output'

def translate_batch(texts):
    """Übersetzt eine Liste von Texten in einer einzigen Anfrage."""
    try:
        return GoogleTranslator(source='en', target='de').translate_batch(texts)
    except TranslationNotFound:
        return texts  # Bei Fehler die ursprünglichen Texte zurückgeben

def process_file(filename):
    input_file_path = os.path.join(input_dir, filename)

    # Bestimmen des Dateityps und Verarbeiten der Datei entsprechend
    if filename.endswith('.csv'):
        with open(input_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Flatten data for batch processing
        all_texts = [text for row in data for text in row]
        
        # Batch-Übersetzung
        translated_texts = []
        batch_size = 100  # Anzahl der Sätze pro Batch anpassen
        for i in range(0, len(all_texts), batch_size):
            batch = all_texts[i:i + batch_size]
            translated_batch = translate_batch(batch)
            translated_texts.extend(translated_batch)

        # Reformat the translated texts back to their original structure
        translated_data = []
        for i in range(0, len(translated_texts), len(data[0])):
            translated_data.append(translated_texts[i:i + len(data[0])])

        output_file_path = os.path.join(output_dir, filename)
        with open(output_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(translated_data)
            print(f"Ausgabedatei erstellt: {output_file_path}")

    elif filename.endswith('.txt'):
        with open(input_file_path, 'r', encoding='utf-8') as file:
            all_texts = file.readlines()

        # Batch-Übersetzung
        translated_texts = translate_batch([text.strip() for text in all_texts])

        # Ausgabe in eine neue TXT-Datei
        output_file_path = os.path.join(output_dir, filename)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines("\n".join(translated_texts))
            print(f"Ausgabedatei erstellt: {output_file_path}")

    elif filename.endswith('.json'):
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Überprüfen, ob die Daten eine Liste von Texten enthalten
        if isinstance(data, list):
            translated_texts = translate_batch(data)
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                json.dump(translated_texts, file, ensure_ascii=False, indent=4)
                print(f"Ausgabedatei erstellt: {output_file_path}")

if __name__ == '__main__':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Gefundene Dateien im Input-Verzeichnis:", os.listdir(input_dir))

    start_time = time.time()  # Startzeit erfassen

    for filename in os.listdir(input_dir):
        if filename.endswith(('.csv', '.txt', '.json')):
            process_file(filename)

    end_time = time.time()  # Endzeit erfassen
    elapsed_time = end_time - start_time  # Verstrichene Zeit berechnen
    print(f"Übersetzung abgeschlossen! Zeit für die Übersetzung: {elapsed_time:.2f} Sekunden")