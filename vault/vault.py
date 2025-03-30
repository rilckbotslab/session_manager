import hvac
from hvac.exceptions import InvalidPath, Forbidden
import os
from . import exceptions
from dataclasses import dataclass, field

VAULT_URL="http://174.138.67.217:8200/"

@dataclass
class CredUserPass:
    """
    Class to handle user and password credentials.
    """
    username: str
    password: str
@dataclass
class CredToken:
    """
    Class to handle token credentials.
    """
    token: str
    

def get_auth() -> CredUserPass | CredToken:
    """
    Get the authentication method.
    """
    token = os.environ.get("VAULT_TOKEN")
    user, password = os.environ.get("VAULT_USER"), os.environ.get("VAULT_PASSWORD")
    if token:
        return CredToken(token)
    elif user and password:
        return CredUserPass(user, password)
    else:
        raise exceptions.VaultConnection("No valid authentication method found. Please set VAULT_TOKEN or VAULT_USER and VAULT_PASSWORD.")
    
        
        

class Vault:
    prod = os.environ.get("PROD", "False").lower() == "true"
    client:hvac.Client = hvac.Client(url=VAULT_URL)
    
    def __init__(self):
        
        self.mount_point = os.getenv("PROJECT_NAME")
        if not self.mount_point:
            raise exceptions.VaultConnection("No mount point found. Please set PROJECT_NAME environment variable.")
        self.mount_point = self.mount_point.lower()
        
        auth = get_auth()
        
        if isinstance(auth, CredUserPass):
            self.client.auth.userpass.login(
                username=auth.username,
                password=auth.password
            )
        elif isinstance(auth, CredToken):
            self.client.token = auth.token
        assert self.client.is_authenticated(), exceptions.VaultAuthentication(
            "Vault authentication failed."
            )            

    def get_secret(self, path):
        """
        Get a secret from Vault.
        """        
        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path=f"{'dev' if not self.prod else 'prod'}/{path}",
                mount_point=self.mount_point,
            )
        except Forbidden as e:
            raise exceptions.Forbidden(f"You do not have permission to access this secret: {path}")
        except InvalidPath:
            raise exceptions.InvalidSecretPath(f"Invalid secret path: {path}")
        
        return secret['data']['data']