import os
import nltk

# Ensure the NLTK_DATA env var is used
nltk_data_path = os.environ.get("NLTK_DATA", "/opt/render/nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
nltk.download("vader_lexicon", download_dir=nltk_data_path)