from flask import Flask, render_template , request           # importing render template cuz it will help too display out HTML file , Importing request to access user's session ID (SID) 
from flask_socketio import SocketIO, send , join_room, leave_room , emit        # impoting send function  so that whavtever text im writing must be visiable to the other client
from pymongo import MongoClient                    # to connect and interact with MongoDB Atlas
from nltk.sentiment import SentimentIntensityAnalyzer  # sentiment analysis using VADER
import nltk
from datetime import datetime                      # to store message timestamps
from dotenv import load_dotenv
import requests
import os


app = Flask(__name__)   
app.config["SECRET_KEY"] = "secretekey"            # Used to secure the session       WE can write anything i have written(secretekey)                   
socketio = SocketIO(app)
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()                 # We are creating an object sia and assign SentimentIntensityAnalyzer() to it 

# MongoDB Atlas connection (replace <password> with your actual MongoDB user password)
load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["chat_db"]
collection = db["messages"]

def detect_sarcasm(text):
    HF_TOKEN = os.getenv("HF_TOKEN")
    API_URL = "https://api-inference.huggingface.co/models/SkolkovoInstitute/sarcasm-detector"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    try:
        result = response.json()
        if isinstance(result, list) and result:
            label = result[0]['label']
            score = result[0]['score']
            return f"{label} ({score:.2f})"
        return "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"

def detect_topic(text):
    HF_TOKEN = os.getenv("HF_TOKEN")
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    candidate_labels = ["off-topic", "death", "politics", "casual", "joke", "angry", "sports", "technology"]
    payload = {"inputs": text, "parameters": {"candidate_labels": candidate_labels}}

    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        result = response.json()
        if "labels" in result and result["labels"]:
            return result["labels"][0]
        return "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def login():
    return render_template('login.html')  # Show login page first

@app.route('/chat')
def char():
    return render_template('index.html')           # to Fetch the html code and display on the server 

@socketio.on("join_room")               # Handle a user joining a room

def handel_join(data):
    name = data["name"]
    room = data["room"]
    join_room(room)                                  # add this socket to the room
    print(f"{name} has Joined the room {room}")
    emit("message",{"name": "System", "message": f"{name} has joined the room."}, room = room)      # Notify everyone in the room

@socketio.on("message")                            # adding  Listner function and giving event name as (message)

def handel_message(data):                           # passing parameter (msg) to function
    name = data.get("name", "User")
    room = data.get("room","general")
    msg = data.get("message", "")

    print(f"{name} Message in {room}:  {msg}")                # Print message on server




# Use VADER Which is a part Nltk Liabrary to analyze the sentiment of the message
# Save message to MongoDB with timestamp
    collection.insert_one({
        "name": name,
        "text": msg,
        "room": room,
        "timestamp": datetime.utcnow()              # Save time so we can later fetch "latest" messages
    })

    emit("message", {"name": name, "message": msg}, room = room)   # Send the message to everyone in the same room

@socketio.on("end_chat")
def handel_end_chat():
    # Get the last 10–15 messages (most recent first, then reverse)
    recent_messages = list(collection.find().sort("timestamp", -1).limit(15))
    recent_messages.reverse()                       # Reverse the messages so we go from oldest → latest

    # Analyze sentiment scores for each message and compute average
    total_score = 0
    full_text = ""
    
    for item in recent_messages:                    # Loop over each message
        text = item['text']
        full_text += text + " "
        total_score += sia.polarity_scores(item['text'])['compound']      # Get compound sentiment score and add it

    avg_score = total_score / len(recent_messages) if recent_messages else 0       # Calculate the average sentiment score of the 15 messages


# Here is th logic i have Written  to Dteremine the Mood based on the Score 
    if avg_score >= 0.05:
        mood = "😊 Positive sentiment so far"                       # If the score is high, it's a positive message
    elif avg_score <= -0.05:
        mood = "😢 Negative sentiment so far"                       # If the score is low, it's a negative message
    else:
        mood = "🙂 Neutral sentiment so far"                        # Or else scores are considered neutral

    # Add mood to message
    # message_with_mood =f"{name}: {msg}"                         # Using f String 
    # send(message_with_mood, broadcast = True)                 # Using Send function from socket.oi  to send the msg to all connected client and itself too cuz we are braodcasting it 

    detected_sarcasm = detect_sarcasm(full_text)
    detected_topic = detect_topic(full_text)

    final_mood = f"{mood} — With Tone of : {detected_sarcasm}, On Topic: {detected_topic}"

    # Send mood separately
    socketio.emit("mood_update", final_mood, to=request.sid)        # request.sid = unique session ID of the connected user who sent the request  ensures that only that one user gets the mood result.

# So here we are Runnig Our app through Socketio and not Flask and we have Kept Degub = True so that it will show any error online     
if (__name__) ==  '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)





    # socketio.run(app, host='0.0.0.0', port=3000, debug=True)

    # socketio.run(app, debug= True)                 # So here we are RInnig Our app through Socketio and not Flask and we have Kept Degub = True so that it will show any error online 







