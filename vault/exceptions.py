"""Vault exceptions."""

class VaultError(Exception):
    """Base class for Vault exceptions."""

class VaultConnection(VaultError):
    """Exception raised for connection errors."""

class VaultAuthentication(VaultError):
    """Exception raised for authentication errors."""

class InvalidSecretPath(VaultError):
    """Exception raised for invalid secret path errors."""

class Forbidden(VaultError):
    """Exception raised for forbidden errors."""