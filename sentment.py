# import nltk
# nltk.download("vader_lexicon")

# from nltk.sentiment import SentimentIntensityAnalyzer

# sia = SentimentIntensityAnalyzer()


# def  detect_mood(text):
#     score = sia.polarity_scores(text)['compound']

#     if score >= 0.5:
#         return "😄 Happy"
#     elif score <= -0.5:
#         return "😢 Sad"
#     else :
#         return "😐 Neutral/Confused"
    
# print("Type something (type 'exit' to quit) :")

# while True:
#     message = input("You: ")
#     if message.lower() == "exit":
#         break
#     mood = detect_mood(message)
#     print(f'Detected Mood : {mood}')
