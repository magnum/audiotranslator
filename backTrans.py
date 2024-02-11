from flask import Flask, request, jsonify, send_file, after_this_request
import os
import io
from pydub import AudioSegment
from google.cloud import speech, translate_v2 as translate, texttospeech
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configura le credenziali per le API di Google Cloud
# Assicurati di avere un file JSON con le tue credenziali e di impostare la variabile di ambiente correttamente
# Esempio: export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"

@app.route('/translate-audio', methods=['POST'])
def translate_audio():
    # Prendi il file audio e la lingua di destinazione dalla richiesta
    audio_file = request.files['audio']
    target_language = request.form['target_language']
    source_language = request.form['source_language']

    # Trascrivi l'audio in testo
    text = transcribe_audio(audio_file, source_language)

    # Traduci il testo
    translated_text = translate_text(text, target_language)

    # Converti il testo tradotto in audio
    audio_content = text_to_speech(translated_text, target_language)

    # Salva l'audio e invia il percorso come risposta (o invia direttamente l'audio)
    output_filename = "translated_speech.mp3"
    with open(output_filename, "wb") as out:
        out.write(audio_content)


    @after_this_request
    def remove_file(response):
        try:
            os.remove(output_filename)
        except Exception as error:
            app.logger.error("Errore nella rimozione del file:", error)
        return response
    # Invia il file come risposta
    response = send_file(output_filename, as_attachment=True, mimetype='audio/mp3')

    # Pulisci: rimuovi il file dopo che è stato inviato

    return response

def transcribe_audio(audio_file, source_language):
    client = speech.SpeechClient()

    # Leggi il file audio e convertilo in formato WAV
    sound = AudioSegment.from_file_using_temporary_files(audio_file)
    sound = sound.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    buffer = io.BytesIO()
    sound.export(buffer, format="wav")
    audio_content = buffer.getvalue()

    # Configurazione per l'API di Google Speech-to-Text
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=source_language
    )

    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript

def translate_text(text, target_language):
    client = translate.Client()

    result = client.translate(text, target_language=target_language)
    return result['translatedText']

def text_to_speech(text, language_code):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content

if __name__ == '__main__':
    app.run(debug=True)
