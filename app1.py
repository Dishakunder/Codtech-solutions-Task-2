import os
import uuid
import pyttsx3
from gtts import gTTS
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static1/audio1'

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to get available voices (for pyttsx3)
def get_voices():
    voices = engine.getProperty('voices')
    male_voices = []
    female_voices = []
    for voice in voices:
        if 'female' in voice.name.lower():
            female_voices.append({'id': voice.id, 'name': voice.name, 'gender': 'Female'})
        else:
            male_voices.append({'id': voice.id, 'name': voice.name, 'gender': 'Male'})
    return {'male': male_voices, 'female': female_voices}

# Languages for gTTS
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'de': 'German'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    voice_options = get_voices()  # For pyttsx3
    if request.method == 'POST':
        text = request.form['text']
        voice_id = request.form.get('voice')
        speed = request.form['speed']
        language = request.form['language']

        # Handle pyttsx3 if voice is selected
        if voice_id:
            engine.setProperty('voice', voice_id)
            if speed == 'slow':
                engine.setProperty('rate', 60)
            elif speed == 'fast':
                engine.setProperty('rate', 250)
            else:
                engine.setProperty('rate', 150)

            # Generate a unique filename for pyttsx3 audio
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            engine.save_to_file(text, filepath)
            engine.runAndWait()
        else:
            # Use gTTS for multilingual support
            tts = gTTS(text=text, lang=language, slow=(speed == 'slow'))
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            tts.save(filepath)

        return render_template('index1.html', voices=voice_options, languages=LANGUAGES, audio_file=filename)

    return render_template('index1.html', voices=voice_options, languages=LANGUAGES)

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('static1/audio1'):
        os.makedirs('static1/audio1')
    app.run(debug=True)
