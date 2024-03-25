import ast
import hashlib
import os

import torch
from speechbrain.inference import EncoderClassifier, SpeakerRecognition, EncoderDecoderASR

from src.model.claim import select_all_claims, Claim

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-wav2vec2-commonvoice-en")
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")


def find_best_claim(wav_filename: str) -> [bool, Claim, str]:
    waveform = classifier.load_audio(wav_filename)
    claims = select_all_claims()

    waveform_string = str(waveform.tolist())

    result = None
    result_score = 0
    for claim in claims:
        claim_waveform = torch.tensor(ast.literal_eval(claim["vector"]))

        score, more_than_threshold = verification.verify_batch(claim_waveform, waveform, threshold=0.55)
        print("score") 
        print(score[0][0]) 
        print(claim['id'])
        if more_than_threshold:
            print('setting result')
            result = claim
            result_score = score

    if result is not None:
        return True, result, waveform_string

    return False, None, waveform_string


def verify_salt(file_path: str) -> bool:
    str_check = asr_model.transcribe_file(file_path)
    return str_check.capitalize() == os.getenv('SALT_STRING').capitalize()
