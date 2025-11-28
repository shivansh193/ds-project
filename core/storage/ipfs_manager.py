import os
import requests
import json
from typing import Optional, Dict, Any

class PinataManager:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.pinata.cloud"
        self.headers = {
            "pinata_api_key": self.api_key,
            "pinata_secret_api_key": self.api_secret
        }

    def pin_file(self, file_path: str) -> Optional[str]:
        """Uploads a file to Pinata and returns the IPFS CID."""
        url = f"{self.base_url}/pinning/pinFileToIPFS"
        
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, files=files, headers=self.headers)
                
            if response.status_code == 200:
                return response.json()['IpfsHash']
            else:
                print(f"Error pinning file: {response.text}")
                return None
        except Exception as e:
            print(f"Exception pinning file: {e}")
            return None

    def pin_json(self, data: Dict[str, Any]) -> Optional[str]:
        """Uploads JSON data to Pinata and returns the IPFS CID."""
        url = f"{self.base_url}/pinning/pinJSONToIPFS"
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()['IpfsHash']
            else:
                print(f"Error pinning JSON: {response.text}")
                return None
        except Exception as e:
            print(f"Exception pinning JSON: {e}")
            return None

    def test_authentication(self) -> bool:
        """Tests connection to Pinata API."""
        url = f"{self.base_url}/data/testAuthentication"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except Exception:
            return False
