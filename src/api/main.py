import ast
from datetime import datetime
from typing import TypeAlias, Tuple
import logging
import flask
import os
import hashlib

import src.api.errors as errs
from src.api.comparison import verify_salt, find_best_claim
from src.extractor.base64 import base64_to_audio
from src.config.env import EnvConfig
from src.issuer.connector import IssuerConnector

from pydub import AudioSegment

from src.model.claim import Claim

app = flask.Flask(__name__)
cfg = EnvConfig()

Response: TypeAlias = Tuple[dict, int] # Just a type alias for the response

def run_api() -> None:
    """
    Runs the API for serving feature extraction method
    """
    
    app.run(port=cfg.api_port, debug=True)

@app.route("/integrations/face-extractor-svc/extract", methods=["POST"])
def extract_features() -> None:
    def jsonify_error(err: errs.ErrorResponse) -> Response:
        json_err, status_code = err
        return flask.jsonify(json_err), status_code
    
    # Returning an error if got a wrong method
    if flask.request.method != "POST":
        return jsonify_error(errs.INVALID_METHOD)

    # Asserting that the request has the necessary data
    def validate_request() -> bool:
        if "data" not in flask.request.json:
            return False
        data = flask.request.json["data"]
        if "attributes" not in data:
            return False
        attributes = data["attributes"]
        return ("did" in attributes
            and "user_id" in attributes
            and "public_key" in attributes
            and "metadata" in attributes)

    if not validate_request():
        logging.error("Bad request!")
        return jsonify_error(errs.BAD_REQUEST)

    file_path = '/Users/mike/feature-extractor-svc/voice.m4a'
    connector = IssuerConnector(cfg.issuer_base_url, cfg.issuer_id)

    # Getting attributes
    attributes = flask.request.json["data"]["attributes"]
    did = attributes["did"]
    user_id = attributes["user_id"]
    public_key = attributes["public_key"]
    metadata = attributes["metadata"]
    audio_base64 = attributes["voice"]

    # Decoding the image and processing it
    try:
        base64_to_audio(audio_base64, file_path)
        m4a_file = file_path # I have downloaded sample audio from this link https://getsamplefiles.com/sample-audio-files/m4a
        wav_filename = 'output.wav'

        sound = AudioSegment.from_file(m4a_file, format='m4a')
        file_handle = sound.export(wav_filename, format='wav')

        # Verify salt
        if not verify_salt(wav_filename):
            delete_file(file_path)
            logging.error(f"wrong salt")
            return jsonify_error(errs.WRONG_SALT)

        print('1')
        is_found, best_claim, waveform_string = find_best_claim(wav_filename)
        # If we found a claim, and it's not submitted - resubmit the claim
        if is_found and not best_claim['is_submitted']:
            claim_id = resubmit_claim(best_claim, public_key, did, metadata, connector)
            return form_extract_response(best_claim["vector"], claim_id)

        print('2')
        # If we found a claim - we just revoke it
        if is_found:
            connector.revoke_claim(best_claim['claim_id'])
            Claim.delete().where(user_id == best_claim['user_id']).execute()

        print('3')
        claim_user_id = user_id if best_claim is None else best_claim['user_id']
        claim = Claim.create(user_id=claim_user_id, vector=waveform_string, metadata=metadata, pk=public_key, is_submitted=False)
        waveform_hash = hashlib.sha256(claim.vector.encode()).hexdigest()
        claim.save()
        print('4')
        claim_id = connector.create_credential({
            "user_id": claim_user_id,
            "embedding": waveform_hash,
            "public_key": public_key,
            "did": did,
            "metadata": metadata
        })
        claim.claim_id = claim_id
        claim.is_submitted = True
        claim.save()
        print('5')
        return form_extract_response(claim.vector, claim_id, user_id=claim_user_id if best_claim else None)
    except Exception as exception:
        logging.error(f"Internal error when processing request: {exception}")
        return jsonify_error(errs.INTERNAL_ERROR)
        
def form_extract_response(embedding: str, claim_id: str) -> Response:
    """
    Formats the response to be returned by the API
    """
    print(claim_id)
    print(embedding)
    return flask.jsonify({
        "data": {
            "id" : 1,
            "type": "embedding",
            "attributes": {
                "embedding": embedding,
                "claim_id": claim_id
            }
        }
    }), 200

def get_timestamp(): return datetime.utcnow().isoformat()

def delete_file(file_path: str):
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)

def resubmit_claim(claim: Claim, public_key: str, did: str, metadata: str, connector: IssuerConnector):
    waveform_hash = hashlib.sha256(claim['vector'].encode()).hexdigest()
    claim_id = connector.create_credential({
    "user_id": claim['user_id'],
        "embedding": waveform_hash,
        "public_key": public_key,
        "did": did,
        "metadata": metadata
    })

    Claim.update(claim_id = claim_id, is_submitted=True).where(Claim.id == claim['id']).execute()

def form_extract_response(embedding: str, claim_id: str, user_id: str = None) -> Response:
    """
    Formats the response to be returned by the API.
    If the `user_id` is None, it means that revoke did not happen.
    """
    print(claim_id)
    response = {
        "data": {
            "id" : 1,
            "type": "embedding",
            "attributes": {
                "embedding": embedding,
                "claim_id": claim_id,
            }
        }
    }
    if user_id is not None:
        # Adding user id to the response
        response["data"]["attributes"]["user_id"] = user_id
    
    return flask.jsonify(response), 200
    
    
def form_pk_response(public_key: str) -> Response:
    """
    Formats the response to be returned by the API.
    """
    
    return flask.jsonify({
        "data": {
            "id" : 1,
            "type": "pk",
            "attributes": {
                "public_key": public_key
            }
        }
    }), 200 