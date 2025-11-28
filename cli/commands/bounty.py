import typer
import os
import time
import requests
import json
import uuid
import tempfile
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

from core.pricing.calculator import CostCalculator
from core.security.encryption import EncryptionManager
from core.storage.ipfs_manager import PinataManager

load_dotenv()

app = typer.Typer()
console = Console()

COORDINATOR_URL = os.getenv("COORDINATOR_URL", "http://localhost:8000")
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")

@app.command("raise")
def raise_bounty(file_path: str):
    """
    Analyze a Python file, encrypt it, upload to IPFS, and post a bounty.
    """
    if not os.path.exists(file_path):
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(code=1)

    # 1. Calculate Cost
    console.print("[bold blue]Analyzing file complexity...[/bold blue]")
    calculator = CostCalculator()
    cost_data = calculator.calculate(file_path)
    
    table = Table(title="Bounty Estimate")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Complexity Score", str(cost_data["complexity_score"]))
    table.add_row("Estimated Cost", f"${cost_data['estimated_cost']}")
    console.print(table)

    if not typer.confirm("Do you want to proceed?"):
        raise typer.Abort()


    # 1.5 Inject Canary Token
    canary_token = str(uuid.uuid4())
    console.print(f"[blue]Injecting verification token: {canary_token}[/blue]")
    
    with open(file_path, "r") as f:
        original_code = f.read()
    
    # Inject a print statement that outputs the canary
    injected_code = f"{original_code}\n\nprint('VERIFICATION_TOKEN:{canary_token}')"
    
    # Create temp file in system temp dir
    fd, temp_file_path = tempfile.mkstemp(suffix=".py")
    os.close(fd)
    
    with open(temp_file_path, "w") as f:
        f.write(injected_code)

    # 2. Encrypt File
    console.print("[bold blue]Encrypting file...[/bold blue]")
    key = EncryptionManager.generate_key()
    result_key = EncryptionManager.generate_key() # Key for worker to encrypt result
    
    encrypted_data = EncryptionManager.encrypt_file(temp_file_path, key)
    
    # Create encrypted file in system temp dir
    fd_enc, encrypted_file_path = tempfile.mkstemp(suffix=".enc")
    os.close(fd_enc)
    
    with open(encrypted_file_path, "wb") as f:
        f.write(encrypted_data)
        
    # Cleanup injected temp file
    os.remove(temp_file_path)

    # 3. Upload to Pinata
    console.print("[bold blue]Uploading to Pinata...[/bold blue]")
    if not PINATA_API_KEY or not PINATA_SECRET_API_KEY:
        console.print("[red]Pinata keys not found in .env[/red]")
        raise typer.Exit(code=1)
        
    pinata = PinataManager(PINATA_API_KEY, PINATA_SECRET_API_KEY)
    # Pinata needs a filename, pass it explicitly if possible or rename temp file? 
    # PinataManager.pin_file takes a path. We should probably give it a meaningful name metadata if we could, 
    # but for now the content is what matters.
    ipfs_cid = pinata.pin_file(encrypted_file_path)
    
    if not ipfs_cid:
        console.print("[red]Failed to upload to IPFS[/red]")
        raise typer.Exit(code=1)
        
    console.print(f"[green]Uploaded to IPFS: {ipfs_cid}[/green]")
    
    # Cleanup encrypted file
    os.remove(encrypted_file_path)

    # 4. Post to Coordinator
    console.print("[bold blue]Posting bounty to Coordinator...[/bold blue]")
    bounty_payload = {
        "ipfs_cid": ipfs_cid,
        "complexity_score": cost_data["complexity_score"],
        "estimated_cost": cost_data["estimated_cost"],
        "filename": os.path.basename(file_path)
    }
    
    try:
        response = requests.post(f"{COORDINATOR_URL}/bounties", json=bounty_payload)
        response.raise_for_status()
        bounty = response.json()
        bounty_id = bounty["id"]
        console.print(f"[green]Bounty created! ID: {bounty_id}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to post bounty: {e}[/red]")
        raise typer.Exit(code=1)

    # 6. Send Keys (Decryption + Result)
    console.print("[bold blue]Sending keys...[/bold blue]")
    try:
        key_payload = {
            "key": key.decode(),
            "result_key": result_key.decode()
        }
        requests.post(f"{COORDINATOR_URL}/bounties/{bounty_id}/key", json=key_payload)
        console.print("[green]Keys sent successfully![/green]")
    except Exception as e:
        console.print(f"[red]Failed to send keys: {e}[/red]")

    # 7. Wait for Result
    console.print("[yellow]Waiting for worker to complete...[/yellow]")
    bounty = None
    with console.status("Polling coordinator for result..."):
        while True:
            try:
                response = requests.get(f"{COORDINATOR_URL}/bounties/{bounty_id}")
                if response.status_code == 404:
                     # If 404, it might be that the server restarted and lost data
                     console.print("[red]Bounty lost (Coordinator might have restarted).[/red]")
                     raise typer.Exit(code=1)
                     
                bounty = response.json()
                
                if bounty.get("status") == "COMPLETED":
                    console.print(f"[green]Worker {bounty.get('worker_id')} completed the task![/green]")
                    break
                
                time.sleep(2)
            except typer.Exit:
                raise
            except Exception as e:
                console.print(f"[red]Error polling: {e}[/red]")
                break
    
    if not bounty or bounty.get("status") != "COMPLETED":
        console.print("[red]Task did not complete successfully.[/red]")
        raise typer.Exit(code=1)

    # 8. Download and Verify Result
    result_cid = bounty.get("result_ipfs_cid")
    console.print(f"[blue]Downloading result: {result_cid}[/blue]")
    
    # Use public gateways for download
    gateways = [
        "https://gateway.pinata.cloud/ipfs",
        "https://ipfs.io/ipfs",
        "https://dweb.link/ipfs",
        "https://cloudflare-ipfs.com/ipfs"
    ]
    
    # Allow custom gateway override
    custom_gateway = os.getenv("CUSTOM_IPFS_GATEWAY")
    if custom_gateway:
        gateways.insert(0, custom_gateway)
    
    encrypted_result = None
    start_time = time.time()
    
    # Retry for up to 60 seconds
    while time.time() - start_time < 60:
        for gateway in gateways:
            try:
                # console.print(f"Trying {gateway}...")
                resp = requests.get(f"{gateway}/{result_cid}", verify=False, timeout=10)
                if resp.status_code == 200:
                    encrypted_result = resp.content
                    console.print(f"[green]Successfully downloaded from {gateway}[/green]")
                    break
            except:
                pass
        
        if encrypted_result:
            break
            
        time.sleep(2)
        console.print("[yellow]Waiting for IPFS propagation...[/yellow]")
            
    if not encrypted_result:
        console.print("[red]Failed to download result from any gateway after retries[/red]")
        console.print(f"[bold]Try opening this link in your browser to check if it works:[/bold]")
        console.print(f"https://gateway.pinata.cloud/ipfs/{result_cid}")
        raise typer.Exit(code=1)

    console.print("[blue]Decrypting result...[/blue]")
    try:
        decrypted_output = EncryptionManager.decrypt_data(encrypted_result, result_key)
        output_text = decrypted_output.decode()
        
        # Verify Canary
        if f"VERIFICATION_TOKEN:{canary_token}" in output_text:
            console.print("[bold green]VERIFICATION SUCCESSFUL! Canary token found.[/bold green]")
            # Remove the token line from output for clean display
            clean_output = output_text.replace(f"VERIFICATION_TOKEN:{canary_token}", "")
            console.print("[bold]Output:[/bold]")
            console.print(clean_output)
        else:
            console.print("[bold red]VERIFICATION FAILED! Canary token missing.[/bold red]")
            console.print("[bold]Raw Output:[/bold]")
            console.print(output_text)
            
    except Exception as e:
        console.print(f"[red]Failed to decrypt result: {e}[/red]")

