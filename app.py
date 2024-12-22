from flask import Flask, render_template, request, redirect, url_for, session, send_file
from tinydb import TinyDB, Query
import time
import hashlib
from moviepy.editor import *
import speech_recognition as sr
from googletrans import Translator
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pandas as pd
import joblib
from functools import wraps

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = TinyDB('database.json')
users_table = db.table('users')
db = TinyDB('db.json')

load_dotenv()
genai.configure(api_key="AIzaSyDKiKefeHJHN78kx5lsi0nCx8MdgouYnaI")

# Load the model
model = joblib.load('classifier.pkl')
# model = joblib.load('D:/final_code/final_code/Code/classifier.pkl')
# vectorizer = joblib.load('D:/final_code/final_code/Code/tfidf_vectorizer.pkl')



# Load the TF-IDF vectorizer
vectorizer = joblib.load('tfidf_vectorizer.pkl')

prompt = """You are a Youtube Video Summarizer. You will be taking transcript text
and summarizing the entire video and providing the important summary in points within 150 words.
Please provide the summary of the text given here: """

translator = Translator()


def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path)
    return audio_path


def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='mr-IN')
    return text


def translate_text(text, dest_lang='en'):
    translated_text = translator.translate(text, dest=dest_lang).text
    return translated_text


def generate_gemini_content(text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + text)
    return response.text


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text']
        return transcript
    except Exception as e:
        raise e


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/get_notes', methods=['POST'])
@login_required
def get_notes():
    try:
        if 'video' not in request.files:
            return "No file part"
        video_file = request.files['video']
        if video_file.filename == '':
            return "No selected file"
        if video_file:
            video_path = os.path.join('uploads', video_file.filename)
            video_file.save(video_path)
            audio_path = extract_audio_from_video(video_path)
            marathi_text = speech_to_text(audio_path)
            english_text = translate_text(marathi_text)
            summary = generate_gemini_content(english_text)
            predicted_label = None
            text_input = summary
            text_input_vectorized = vectorizer.transform([text_input])
            predicted_label = model.predict(text_input_vectorized)[0]
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            filename = video_file.filename
            link = "-"
            text = summary
            lang = "hi"
            translated_texth = translator.translate(text, dest=lang).text
            text = summary
            lang = "en"
            translated_texte = translator.translate(text, dest=lang).text
            db.insert({'timestamp': timestamp, 'filename': filename, 'link': link, 'label': predicted_label})
            translated_summary = translate_text(summary, dest_lang='mr')
            return render_template('result.html', summary=translated_summary, predicted_label=predicted_label, summarym=translated_texte, summaryh=translated_texth)
    except sr.RequestError as e:
        return redirect(url_for('error'))
    return "Error occurred!"


@app.route('/error')
def error():
    return render_template('error2.html')


@app.route('/get_notes_y', methods=['POST'])
@login_required
def get_notes_y():
    youtube_link = request.form['youtube_link']
    if youtube_link:
        video_id = youtube_link.split('=')[1]
        image_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text)
            predicted_label = None
            text_input = summary
            text_input_vectorized = vectorizer.transform([text_input])
            predicted_label = model.predict(text_input_vectorized)[0]
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            filename = "-"
            link = youtube_link
            text = summary
            lang = "hi"
            translated_texth = translator.translate(text, dest=lang).text
            text = summary
            lang = "mr"
            translated_textm = translator.translate(text, dest=lang).text
            db.insert({'timestamp': timestamp, 'filename': filename, 'link': link, 'label': predicted_label})
            return render_template('result.html', image_url=image_url, summary=summary, predicted_label=predicted_label, summarym=translated_textm, summaryh=translated_texth)
    return "Error occurred!"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['firstName']
        lname = request.form['lastName']
        email = request.form['emailId']
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert user data into the database
        users_table.insert({
            'first_name': fname,
            'last_name': lname,
            'email': email,
            'username': username,
            'password': hashed_password,
        })

        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        User = Query()
        user = users_table.get(User.username == username)
        if user and user['password'] == hashed_password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)


@app.route('/logout')
def logout():
    # Logout process
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/translate', methods=['POST'])
@login_required
def translate():
    text = request.form['text']
    lang = request.form['lang']
    translated_text = translator.translate(text, dest=lang).text
    with open("translated_output.txt", "w", encoding="utf-8") as text_file:
        text_file.write(translated_text)
    return send_file("translated_output.txt", as_attachment=True)


@app.route('/download_txt', methods=['POST'])
@login_required
def download_txt():
    text = request.form['text']
    with open("output.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text)
    return send_file("output.txt", as_attachment=True)


@app.route('/profile')
@login_required
def profile():
    data = db.all()
    records = []
    for record in data:
        records.append({'timestamp': record['timestamp'], 'filename': record['filename'], 'link': record['link'], 'label': record['label']})
    return render_template('profile.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)