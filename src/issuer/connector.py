from __future__ import annotations

import requests
import logging

class IssuerConnector:
    """
    Class responsible for connecting to the issuer service.
    """
    
    CREDENTIAL_SCHEMA = "https://nftstorage.link/ipfs/bafkreidcbkn6bqyrsmj4b3oewezmxdgzy2aim7myddhdw56witqyurn3c4"
    AUTH_SECRET = "YWRtaW46YWFhMTIzYWFh"
        
    def __init__(self, base_url: str, issuer_id: str) -> None:
        self._base_url = base_url
        self._issuer_id = issuer_id
        
    def create_credential(self, credential: dict) -> int:
        """
        Creates a credential in the issuer service. Returns the claim ID.
        """
        
        # Validating the credential
        assert "did" in credential
        assert "user_id" in credential
        assert "embedding" in credential
        assert "public_key" in credential
        assert "metadata" in credential
        
        # Getting data from the credential data
        url = f"{self._base_url}/v1/{self._issuer_id}/claims"
        user_id = credential["user_id"]
        did = credential["did"]
        embedding = credential["embedding"]
        public_key = credential["public_key"]
        metadata = credential["metadata"]
        
        # Forming the data
        data = {
            "credentialSchema": IssuerConnector.CREDENTIAL_SCHEMA,
            "type": "bpleapcpker",
            "credentialSubject": {
                "id": did,
                "userid": user_id,
                "f": embedding,
                "pk": public_key,
                "metadata": metadata
            },
            "signatureProof": True,
            "mtProof": True
        }
        
        logging.error(f"Data for getting claim id: {data}")
        
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {IssuerConnector.AUTH_SECRET}",
            "content-type": "application/json",
        }
        
        response = requests.post(url, headers=headers, json=data)
        claim_id = response.json()["id"]
        return claim_id
    
    def get_revocation_nonce(self, claim_id: str) -> str:
        """
        Gets the revocation nonce for the claim
        """
        
        url = f"{self._base_url}/v1/{self._issuer_id}/claims/{claim_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {IssuerConnector.AUTH_SECRET}"
        }
        
        try:
            response = requests.get(url, headers=headers)
        except Exception as exception:
            logging.error(f"failed to get revocation nonce: {exception}")
            
        return response.json()["credentialStatus"]["revocationNonce"]
    
    def revoke_claim(self, claim_id: str) -> None:
        """
        Revokes the claim based on the claim ID
        """
        
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {IssuerConnector.AUTH_SECRET}",
            "content-type": "application/json",
        }
        try:
            revocation_nonce = self.get_revocation_nonce(claim_id)
            url = f"{self._base_url}/v1/{self._issuer_id}/claims/revoke/{revocation_nonce}"
            requests.post(url, headers=headers)
        except Exception as exception:
            logging.error(f"failed to revoke claim: {exception}")