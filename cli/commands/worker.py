import typer
import os
import time
import requests
import subprocess
import uuid
import tempfile
from rich.console import Console
from dotenv import load_dotenv

from core.security.encryption import EncryptionManager

load_dotenv()

app = typer.Typer()
console = Console()

COORDINATOR_URL = os.getenv("COORDINATOR_URL", "http://localhost:8000")
# Use a public gateway or Pinata gateway
IPFS_GATEWAY = "https://gateway.pinata.cloud/ipfs" 

@app.command("start")
def start_worker():
    """
    Start a worker node that polls for tasks and executes them.
    """
    worker_id = str(uuid.uuid4())
    console.print(f"[bold green]Worker started! ID: {worker_id}[/bold green]")
    console.print(f"Polling {COORDINATOR_URL} for tasks...")

    while True:
        try:
            # 1. Poll for Pending Bounties
            response = requests.get(f"{COORDINATOR_URL}/bounties?status=PENDING")
            bounties = response.json()
            
            if not bounties:
                time.sleep(5)
                continue
                
            # Pick the first one
            bounty = bounties[0]
            bounty_id = bounty["id"]
            console.print(f"[yellow]Found bounty {bounty_id}! Accepting...[/yellow]")
            
            # 2. Accept Bounty
            try:
                accept_resp = requests.post(
                    f"{COORDINATOR_URL}/bounties/{bounty_id}/accept",
                    params={"worker_id": worker_id}
                )
                accept_resp.raise_for_status()
            except Exception as e:
                console.print(f"[red]Failed to accept bounty: {e}[/red]")
                continue

            # 3. Download Encrypted File
            ipfs_cid = bounty["ipfs_cid"]
            console.print(f"[blue]Downloading file from IPFS: {ipfs_cid}[/blue]")
            
            # Allow user to provide their own working gateway (e.g. private Pinata gateway)
            custom_gateway = os.getenv("CUSTOM_IPFS_GATEWAY")
            
            gateways = [
                "https://gateway.pinata.cloud/ipfs",
                "https://ipfs.io/ipfs",
                "https://dweb.link/ipfs",
                "https://cloudflare-ipfs.com/ipfs"
            ]
            
            if custom_gateway:
                gateways.insert(0, custom_gateway)
            
            encrypted_data = None
            # Retry download for up to 30 seconds to allow for propagation
            start_time = time.time()
            while time.time() - start_time < 30:
                for gateway in gateways:
                    try:
                        file_url = f"{gateway}/{ipfs_cid}"
                        # console.print(f"Trying {gateway}...")
                        file_resp = requests.get(file_url, verify=False, timeout=5)
                        
                        if file_resp.status_code == 200:
                            encrypted_data = file_resp.content
                            console.print(f"[green]Successfully downloaded from {gateway}[/green]")
                            break
                    except Exception:
                        pass
                
                if encrypted_data:
                    break
                
                time.sleep(2)
                console.print("[yellow]Waiting for IPFS propagation...[/yellow]")
            
            if not encrypted_data:
                console.print(f"[red]Failed to download file from any gateway after retries[/red]")
                console.print(f"[bold]Try opening this link in your browser to check if it works:[/bold]")
                console.print(f"https://gateway.pinata.cloud/ipfs/{ipfs_cid}")
                continue
            
            # 4. Get Decryption Key & Result Key
            console.print("[blue]Waiting for keys...[/blue]")
            key = None
            result_key = None
            for _ in range(30): # Wait up to 60s
                try:
                    key_resp = requests.get(
                        f"{COORDINATOR_URL}/bounties/{bounty_id}/key",
                        params={"worker_id": worker_id}
                    )
                    if key_resp.status_code == 200:
                        data = key_resp.json()
                        key = data["key"]
                        result_key = data["result_key"]
                        break
                except:
                    pass
                time.sleep(2)
                
            if not key or not result_key:
                console.print("[red]Timed out waiting for keys[/red]")
                continue
                
            console.print("[green]Keys received! Decrypting...[/green]")
            
            # 5. Decrypt
            try:
                decrypted_code = EncryptionManager.decrypt_data(encrypted_data, key.encode())
            except Exception as e:
                console.print(f"[red]Decryption failed: {e}[/red]")
                continue

            # 6. Execute (Silently)
            filename = bounty["filename"]
            console.print(f"[bold magenta]Executing {filename}...[/bold magenta]")
            
            # Save to temp file in system temp dir
            fd, temp_exec_path = tempfile.mkstemp(suffix=".py")
            os.close(fd)
            
            with open(temp_exec_path, "wb") as f:
                f.write(decrypted_code)
                
            # Run it
            try:
                result = subprocess.run(
                    ["python", temp_exec_path], 
                    capture_output=True, 
                    text=True, 
                    timeout=30
                )
                
                # Combine stdout and stderr
                full_output = result.stdout
                if result.stderr:
                    full_output += "\n[STDERR]\n" + result.stderr
                
                console.print("[blue]Execution complete. Encrypting result...[/blue]")
                
                # 7. Encrypt Result
                encrypted_result = EncryptionManager.encrypt_file(None, result_key.encode(), data=full_output.encode())
                
                # Save encrypted result
                result_filename = f"result_{bounty_id}.enc"
                with open(result_filename, "wb") as f:
                    f.write(encrypted_result)
                    
                # 8. Upload Result to Pinata
                console.print("[blue]Uploading result to IPFS...[/blue]")
                # Re-instantiate PinataManager (assuming env vars are loaded)
                PINATA_API_KEY = os.getenv("PINATA_API_KEY")
                PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
                
                if not PINATA_API_KEY:
                     console.print("[red]Pinata keys missing for result upload[/red]")
                     continue

                from core.storage.ipfs_manager import PinataManager
                pinata = PinataManager(PINATA_API_KEY, PINATA_SECRET_API_KEY)
                result_cid = pinata.pin_file(result_filename)
                
                if not result_cid:
                    console.print("[red]Failed to upload result[/red]")
                    continue
                    
                console.print(f"[green]Result uploaded: {result_cid}[/green]")
                
                # Cleanup
                os.remove(result_filename)
                
                # 9. Submit Result to Coordinator
                console.print("[blue]Submitting result to Coordinator...[/blue]")
                submit_payload = {"ipfs_cid": result_cid}
                requests.post(f"{COORDINATOR_URL}/bounties/{bounty_id}/result", json=submit_payload)
                console.print("[green]Result submitted successfully![/green]")

            except subprocess.TimeoutExpired:
                console.print("[red]Execution timed out[/red]")
            except Exception as e:
                console.print(f"[red]Execution failed: {e}[/red]")
            finally:
                # Cleanup
                if os.path.exists(temp_exec_path):
                    os.remove(temp_exec_path)
                    
            console.print("[green]Task completed! Looking for next...[/green]")
            
        except Exception as e:
            console.print(f"[red]Worker error: {e}[/red]")
            time.sleep(5)
