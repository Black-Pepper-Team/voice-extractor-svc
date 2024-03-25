from __future__ import annotations

import os
# from dotenv import load_dotenv

class EnvConfig:
    """Class responsible for loading environment variables"""
    
    DEFAULT_PORT = 5050
    
    def __init__(self) -> None:
        self._load_env()
        
    def _load_env(self) -> None:
        """
        Loads environment variables
        """
        
        # dotenv_path = os.getenv("DOTENV_FILE")
        # load_dotenv(dotenv_path=dotenv_path)

        self._issuer_id = os.getenv('ISSUER_ID')
        assert self._issuer_id is not None, "Issuer ID is not set"
        
        self._issuer_base_url = os.getenv('ISSUER_BASE_URL')
        assert self._issuer_base_url is not None, "Issuer base URL is not set"
        
        self._port = os.getenv('PORT')
        if self._port is None:
            self._port = EnvConfig.DEFAULT_PORT
        
    @property
    def issuer_base_url(self) -> str:
        """
        Returns the issuer base URL
        """
        
        return self._issuer_base_url
    
    @property
    def api_port(self) -> int:
        """
        Returns the API port
        """
        
        return self._port

    @property
    def issuer_id(self) -> str:
        """
        Returns the issuer id
        """
        return self._issuer_id

