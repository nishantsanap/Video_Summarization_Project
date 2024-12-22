
Video Summarization Platform
The Video Summarization Platform is a web application developed using Python and Flask, designed to summarize Marathi and English videos while providing summaries in Hindi, Marathi, and English languages. The platform leverages advanced machine learning and natural language processing (NLP) techniques to efficiently extract key information from videos.


## Screenshot

![Video Summarization Platform](Assets_results)

Features
Video Upload and Processing: Upload video files, and the platform will convert them into text (speech recognition) and generate a summary.
Multi-Language Support: Provides video summaries in English, Marathi, and Hindi.
YouTube Video Integration: Extracts transcript from YouTube videos and generates summaries.
Text Translation: Translates summaries into multiple languages.
User Authentication: User signup, login, and profile management.
Downloadable Files: Download translated text or summary as a file.
Technologies Used
Flask: Web framework for building the web application.
MoviePy: Extracts audio from video files.
SpeechRecognition: Converts speech to text using Google's speech recognition API.
Google Translator: Translates summaries into different languages.
TinyDB: Simple database for storing user data and summaries.
Machine Learning (SVC): A classifier model to predict the category of the summary.
Joblib: For saving and loading the trained models.
YouTube Transcript API: Extracts YouTube video transcripts.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/nishantsanap/Video_Summarization_Project.git
Navigate to the project directory:

bash
Copy code
cd Video_Summarization_Project
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Environment Setup: Make sure to set up your .env file for environment variables (like API keys).

Usage
Run the Flask app:

bash
Copy code
python app.py
Open your browser and go to http://127.0.0.1:5000.

You can upload a video directly or provide a YouTube link to summarize the content. The platform will:

Extract audio from the video
Perform speech-to-text conversion
Generate a summary of the text
Translate the summary into English, Marathi, and Hindi.
Sign Up/Log In:

Create a new user account or log in with an existing one.
You can view your previous video summaries in the profile section.
Download Summaries: You can download the summary or its translation as a .txt file.

Endpoints
/: Main page after logging in.
/get_notes: Upload a video and get a summary.
/get_notes_y: Provide a YouTube link and get a video summary.
/signup: User registration.
/login: User login.
/logout: User logout.
/translate: Translate a summary into a specified language.
/download_txt: Download the summary as a .txt file.
/profile: View all previous summaries associated with the logged-in user.
Example Flow
Upload Video: The user uploads a video file. The backend extracts the audio, converts it to text using speech recognition, and then generates a summary.

Summary Generation: The generated text is processed using machine learning techniques to summarize the content into meaningful points. The summary is then translated into the desired languages (Hindi, Marathi, English).

Download Summary: The user can download the translated summaries or view them on the platform.

Contributing
Fork the repository.
Create a new branch for your feature.
Make changes and commit them.
Push the changes to your branch.
Open a pull request to contribute to this project.
