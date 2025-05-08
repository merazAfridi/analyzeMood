from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from textblob import TextBlob
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

def analyze_mood(text):
    # Get sentiment polarity (-1 to 1)
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    # Map polarity to mood
    if polarity > 0.1:
        return "Happy", "😊"
    elif polarity < -0.1:
        return "Sad", "😞"
    else:
        return "Neutral", "😐"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    mood, emoji = analyze_mood(text)
    return jsonify({
        'mood': mood,
        'emoji': emoji
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
    