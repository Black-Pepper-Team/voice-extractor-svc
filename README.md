# :sound: Voice Extractor service

Service for extracting features from the voice data. Handles two HTTP requests:

- Getting the closest public key based on the provided voice data.
- Outputting the `claim_id` from the `issuer` service by providing the voice recording and other metadata. Additionally verifies that the salt is correct.

To run the service, run

```bash
python3 main.py run-api
```
