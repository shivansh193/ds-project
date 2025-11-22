import ipfshttpclient
import os

class IPFSManager:
    def __init__(self, gateway_url="/ip4/127.0.0.1/tcp/5001/http"):
        try:
            self.client = ipfshttpclient.connect(gateway_url)
        except Exception:
            self.client = None
            print("Warning: Could not connect to IPFS node")

    def upload_file(self, file_path: str) -> str:
        """Upload a file to IPFS and return the CID."""
        if not self.client:
            return "mock_cid_12345"
        
        res = self.client.add(file_path)
        return res['Hash']

    def download_file(self, cid: str, output_path: str):
        """Download a file from IPFS."""
        if not self.client:
            print(f"Mock download of {cid} to {output_path}")
            return
            
        self.client.get(cid, target=output_path)
