import json
import pandas as pd
from transformers import pipeline
from tabulate import tabulate

def analyze_sentiments(lines):
    classifier = pipeline('sentiment-analysis', model='j-hartmann/emotion-english-distilroberta-base')
    all_results = []

    for line in lines:
        results = classifier(line)
        for result in results:
            all_results.append(result['label'])
    return all_results

def calculate_emotion_percentages(results):
    emotion_counts = {}
    total_emotions = len(results)

    for emotion in results:
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
        else:
            emotion_counts[emotion] = 1

    emotion_percentages = {emotion: round((count / total_emotions) * 100, 2) for emotion, count in emotion_counts.items()}

    return emotion_percentages

def main(json_file_path):
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    table_data = []

    for album, songs in data.items():
        for song, lyrics in songs.items():
            
            lines = lyrics.split('\n')
            results = analyze_sentiments(lines)
            emotion_percentages = calculate_emotion_percentages(results)
            row = {'Álbum': album, 'Canción': song}
            row.update(emotion_percentages)
            table_data.append(row)

    df = pd.DataFrame(table_data)
    return df

if __name__ == '__main__':

    json_file_path = r'C:\Users\Usuario\Documents\Shakira\letras.json'
    emotion_analysis_df = main(json_file_path)
    emotion_analysis_df.fillna(0, inplace=True)
    emotion_analysis_df.to_csv('emotions.csv', index=False)

    print(tabulate(emotion_analysis_df, headers='keys', tablefmt='pretty'))
