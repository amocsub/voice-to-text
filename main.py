import tempfile
from pydub import AudioSegment
from uuid import uuid1
import os
import openai

def trigger(request):
    if 'file' not in request.files:
        return 'No file found in the request.'
    request_file = request.files['file']
    temp_dir = tempfile.mkdtemp()
    file_name = str(uuid1())
    temp_file = os.path.join(temp_dir, file_name)
    request_file.save(temp_file)
    audio = AudioSegment.from_file(temp_file)
    output_file = os.path.join(temp_dir, file_name+'output.mp3')
    audio.export(output_file, format='mp3')
    audio_file= open(output_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript