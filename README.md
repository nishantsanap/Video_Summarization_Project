# Video Summarization For Marathi Language Project

The **Video Summarization Platform** using Python Flask is a comprehensive web app designed to summarize Marathi and English videos while providing summaries in **Hindi**, **Marathi**, and **English** languages. Leveraging machine learning and natural language processing (NLP) techniques, this platform offers a sophisticated solution for efficiently extracting key information from videos.

## Features

- **Video Upload and Processing:** Upload video files, and the platform will convert them into text (speech recognition) and generate a summary.
- **Multi-Language Support:**  Provides video summaries in English, Marathi, and Hindi.
- **YouTube Video Integration:** Extracts transcript from YouTube videos and generates summaries.
- **Text Translation:** Translates summaries into multiple languages.
- **User Authentication:** User signup, login, and profile management.
- **Downloadable Files:** Download translated text or summary as a file.

## Screenshot

![Video Summarization Platform](Assets_results)

## Technologies Used
- Flask: Web framework for building the web application.
- MoviePy: Extracts audio from video files.
- SpeechRecognition: Converts speech to text using Google's speech recognition API.
- Google Translator: Translates summaries into different languages.
- TinyDB: Simple database for storing user data and summaries.
- Machine Learning (SVC): A classifier model to predict the category of the summary.
- Joblib: For saving and loading the trained models.
- YouTube Transcript API: Extracts YouTube video transcripts.

  ## Example Flow
- Upload Video: The user uploads a video file. The backend extracts the audio, converts it to text using speech recognition, and then generates a summary.
- Summary Generation: The generated text is processed using machine learning techniques to summarize the content into meaningful points. The summary is then translated into the desired languages (Hindi, Marathi, English).
- Download Summary: The user can download the translated summaries or view them on the platform.

## Contributing
- Fork the repository.
- Create a new branch for your feature.
- Make changes and commit them.
- Push the changes to your branch.
- Open a pull request to contribute to this project.
