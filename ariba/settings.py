""" Settings for the ariba module """

import os
from vault import vault

class Settings:
    """ Settings for the ariba module """    
    @property
    def BASE_URL(self) -> str:
        return vault.get_secret('website')['base_url']
    
    @property
    def login_url(self) -> str:
        return vault.get_secret('website')['login_url']

    @property
    def USERNAME(self) -> str:
        return vault.get_secret('website')['username']
    
    @property
    def PASSWORD(self) -> str:
        return vault.get_secret('website')['password']

settings = Settings()