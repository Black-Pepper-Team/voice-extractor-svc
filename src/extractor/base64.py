import io, base64


def base64_to_audio(base64_audio, output_filepath):
    """
    Converts a Base64 encoded audio file to a WAV file.

    Parameters:
    - base64_audio: Base64 encoded audio data as a string.
    - output_filepath: File path to save the decoded audio.
    """
    # Decode the Base64 audio
    audio_bytes = base64.b64decode(base64_audio)

    # Write the audio data to a file (considering it's in a compatible format)
    with open(output_filepath, 'wb') as audio_file:
        audio_file.write(audio_bytes)