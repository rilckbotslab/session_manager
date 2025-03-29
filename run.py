
import os
from vault import vault
from database import YudqsLogs
from browser import BrowserRemote
from dotenv import load_dotenv
load_dotenv()

def main():
    # Create a new instance of the browser
    browser = BrowserRemote(        
        remote_url="http://localhost:4444/wd/hub",        
    )

    # Open a new tab
    browser.new_tab()

    # Navigate to a URL
    browser.navigate("https://www.example.com")

    # Close the browser
    browser.close()
    
if __name__ == "__main__":
    main()