"""Vault exceptions."""

class VaultError(Exception):
    """Base class for Vault exceptions."""

class VaultConnectionError(VaultError):
    """Exception raised for connection errors."""

class VaultAuthenticationError(VaultError):
    """Exception raised for authentication errors."""