import pandas as pd
import requests
import joblib
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

# Configuration
BASE_URL = "https://huggingface.co/datasets/AmazonScience/massive/resolve/refs%2Fconvert%2Fparquet/en-US"
URLS = {
    "train": f"{BASE_URL}/train/0000.parquet",
    "val": f"{BASE_URL}/validation/0000.parquet",
    "test": f"{BASE_URL}/test/0000.parquet"
}

MODEL_FILE = "model.pkl"

def load_data(url, split_name):
    """Downloads Parquet file and loads into DataFrame."""
    filename = f"{split_name}.parquet"
    print(f"Downloading/Loading {filename}...")
    
    if not os.path.exists(filename):
        try:
            print(f"Fetching from {url}...")
            response = requests.get(url, allow_redirects=True, timeout=60)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            return [], []
            
    try:
        df = pd.read_parquet(filename)
        required_columns = {"utt", "intent"}
        missing_columns = required_columns.difference(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

        # MASSIVE exposes intent as integer IDs in parquet; map them back to string labels.
        INTENTS = ['datetime_query', 'iot_hue_lightchange', 'transport_ticket', 'takeaway_query', 'qa_stock', 'general_greet', 'recommendation_events', 'music_dislikeness', 'iot_wemo_off', 'cooking_recipe', 'qa_currency', 'transport_traffic', 'general_quirky', 'weather_query', 'audio_volume_up', 'email_addcontact', 'takeaway_order', 'email_querycontact', 'iot_hue_lightup', 'recommendation_locations', 'play_audiobook', 'lists_createoradd', 'news_query', 'alarm_query', 'iot_wemo_on', 'general_joke', 'qa_definition', 'social_query', 'music_settings', 'audio_volume_other', 'calendar_remove', 'iot_hue_lightdim', 'calendar_query', 'email_sendemail', 'iot_cleaning', 'audio_volume_down', 'play_radio', 'cooking_query', 'datetime_convert', 'qa_maths', 'iot_hue_lightoff', 'iot_hue_lighton', 'transport_query', 'music_likeness', 'email_query', 'play_music', 'audio_volume_mute', 'social_post', 'alarm_set', 'qa_factoid', 'calendar_set', 'play_game', 'alarm_remove', 'lists_remove', 'transport_taxi', 'recommendation_movies', 'iot_coffee', 'music_query', 'play_podcasts', 'lists_query']
        
        intent_strings = [INTENTS[int(i)] for i in df['intent']]
        return df['utt'].astype(str).tolist(), intent_strings
            
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return [], []

def train():
    print("Initializing training with MASSIVE dataset (1.15M+ source, loading English partition)...")
    
    # Load separate splits
    X_train, y_train = load_data(URLS["train"], "train_massive")
    X_val, y_val = load_data(URLS["val"], "val_massive")
    X_test, y_test = load_data(URLS["test"], "test_massive")
    
    # Combine Train + Val
    X_train.extend(X_val)
    y_train.extend(y_val)

    print(f"Training on {len(X_train)} examples.")
    print(f"Testing on {len(X_test)} examples.")
    print(f"Number of Intents: {len(set(y_train))}")
    print(f"Example Intents: {list(set(y_train))[:5]}")

    if not X_train:
        print("No training data. Exiting.")
        return

    # Build Pipeline
    print("\nTraining model...")
    text_clf = Pipeline([
        ('vect', CountVectorizer(ngram_range=(1, 2))), 
        ('tfidf', TfidfTransformer()),
        ('clf', LogisticRegression(random_state=42, max_iter=5000, n_jobs=-1)),
    ])
    
    text_clf.fit(X_train, y_train)
    
    # Evaluate
    if X_test:
        print("\nEvaluating on Test Set...")
        predicted = text_clf.predict(X_test)
        score = accuracy_score(y_test, predicted)
        print(f"Test Accuracy: {score:.4f}")
    else:
        print("\nSkipping evaluation because no test data was loaded.")
    
    # Save Model
    joblib.dump(text_clf, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

if __name__ == "__main__":
    train()
