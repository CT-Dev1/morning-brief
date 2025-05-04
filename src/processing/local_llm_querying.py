import os
import sys
import paramiko
import requests
import json
import time
from sshtunnel import SSHTunnelForwarder
import threading

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.config import SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PRIVATE_KEY
SSH_PORT = int(SSH_PORT) # Ensure SSH_PORT is an integer


class SecureOllamaClient:
    def __init__(self, ssh_host, ssh_port, ssh_username, ssh_private_key_path, 
                 remote_ollama_host='127.0.0.1', remote_ollama_port=11434):
        """
        Initialize the secure Ollama client
        
        Args:
            ssh_host: Your home PC's public IP or domain
            ssh_port: SSH port (usually 22)
            ssh_username: Your SSH username
            ssh_private_key_path: Path to your private key file
            remote_ollama_host: Host where Ollama is running on remote machine (usually localhost)
            remote_ollama_port: Port where Ollama is listening (usually 11434)
        """
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.ssh_private_key_path = ssh_private_key_path
        self.remote_ollama_host = remote_ollama_host
        self.remote_ollama_port = remote_ollama_port
        self.tunnel = None
        self.local_bind_port = None
    
    def start_tunnel(self):
        """Establish the SSH tunnel"""
        try:
            self.tunnel = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_username,
                ssh_pkey=self.ssh_private_key_path,
                remote_bind_address=(self.remote_ollama_host, self.remote_ollama_port),
                local_bind_address=('127.0.0.1', 0)  # 0 means pick a random available port
            )
            
            self.tunnel.start()
            self.local_bind_port = self.tunnel.local_bind_port
            print(f"SSH tunnel established. Local port: {self.local_bind_port}")
            
            # Give the tunnel a moment to establish
            time.sleep(1)
            
        except Exception as e:
            print(f"Failed to establish SSH tunnel: {e}")
            raise
    
    def stop_tunnel(self):
        """Close the SSH tunnel"""
        if self.tunnel:
            self.tunnel.stop()
            print("SSH tunnel closed")
    
    def query_ollama(self, model, prompt, stream=False):
        """
        Query the Ollama server through the secure tunnel
        
        Args:
            model: The model to use (e.g., "Llama-3-13b-Instruct:Q4KM")
            prompt: The prompt to send
            stream: Whether to stream the response
        
        Returns:
            The response from Ollama
        """
        if not self.tunnel or not self.tunnel.is_active:
            raise Exception("SSH tunnel is not active. Call start_tunnel() first.")
        
        url = f"http://127.0.0.1:{self.local_bind_port}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error querying Ollama: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry"""
        self.start_tunnel()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_tunnel()


# Example usage
if __name__ == "__main__":
    
    # Only run this script from an external machine (not the home PC) to use the SSH tunnel
    # Add functionality to check if the script is running on the home PC or not, then use the SSH tunnel accordingly
    # Alternively, just use the local Ollama server directly if running on the same machine
    
    # Using the client with context manager (recommended)
    with SecureOllamaClient(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PRIVATE_KEY) as client:
        # Query Ollama
        response = client.query_ollama(
            model="Llama-3-13b-Instruct:Q4KM",
            prompt="What's the oldest constitution in the world?"
        )
        
        print("Response:", response.get('response', 'No response'))
    
    # Alternative usage without context manager
    # client = SecureOllamaClient(SSH_HOST, SSH_PORT, SSH_USERNAME, SSH_PRIVATE_KEY)
    # try:
    #     client.start_tunnel()
    #     response = client.query_ollama(
    #         model="Llama-3-13b-Instruct:Q4KM",
    #         prompt="Hello from secure connection!"
    #     )
    #     print("Response:", response.get('response', 'No response'))
    # finally:
    #     client.stop_tunnel()