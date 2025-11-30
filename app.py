from textblob import TextBlob
from better_profanity import profanity
from flask import Flask, render_template, request, redirect
from db import Database
import spacy

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

dbo = Database()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration', methods=['post'])
def perform_registration():
    name = request.form.get('user_ka_name')
    email = request.form.get('user_ka_email')
    password = request.form.get('user_ka_password')

    response = dbo.insert(name, email, password)

    if response:
        return render_template('login.html', message="Registration Successful, Kindly login to proceed")
    else:
        return render_template('register.html', message="Email already exists")

@app.route('/perform_login', methods=['post'])
def perform_login():
    email = request.form.get('user_ka_email')
    password = request.form.get('user_ka_password')

    response = dbo.search(email,password)

    if response:
        return redirect('/profile')
    else:
        return render_template('login.html', message='Incorrect email/password')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/ner')
def ner():
    return render_template('ner.html')


@app.route('/perform_ner', methods=['post'])
def perform_ner():
    text = request.form.get('ner_text')

    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return render_template('ner.html', entities=entities, input_text=text)

@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

@app.route('/perform_sentiment', methods=['POST'])
def perform_sentiment():
    text = request.form.get('sent_text')
    blob = TextBlob(text)

    sentiment_score = blob.sentiment.polarity
    sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

    return render_template('sentiment.html',
                           input_text=text,
                           score=sentiment_score,
                           label=sentiment_label)


@app.route('/abuse')
def abuse():
    return render_template('abuse.html')

@app.route('/perform_abuse', methods=['POST'])
def perform_abuse():
    text = request.form.get('abuse_text')

    if profanity.contains_profanity(text):
        label = "Abusive / Hate Speech"
    else:
        label = "Clean Text"

    return render_template('abuse.html', input_text=text, label=label)


app.run(debug=True)
