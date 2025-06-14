import nltk
import os

# Set NLTK_DATA environment variable for the build environment
nltk_data_path = "/opt/render/nltk_data"
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

# Download vader_lexicon to the correct path
nltk.download("vader_lexicon", download_dir=nltk_data_path)