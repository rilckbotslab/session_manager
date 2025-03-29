import hvac
import os
from .exceptions import VaultConnectionError, VaultAuthenticationError

VAULT_URL="http://174.138.67.217:8200/"

class Vault:
    prod = os.environ.get("PROD", "False").lower() == "true"
    
    def __init__(self):
        token = os.environ.get("VAULT_TOKEN")
        if not token:
            raise VaultConnectionError("Vault token not found in environment variables.")
        
        self.client = hvac.Client(
            url=VAULT_URL,
            token=token
        )
        assert self.client.is_authenticated(), VaultAuthenticationError(
            "Vault authentication failed."
            )            

    def get_secret(self, path, mount_point='kv'):
        """
        Get a secret from Vault.
        """
        path = f"{'prod' if self.prod else 'dev'}/{path}"
        
        secret = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point=mount_point,
        )
        return secret['data']['data']