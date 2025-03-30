
import os
from vault import vault
from database import YudqsLogs
from browser import Browser
from dotenv import load_dotenv
load_dotenv()

def main():
    # Create a new instance of the browser
    browser = Browser()

    # Navigate to a URL
    browser.navigate("https://www.google.com/")

    browser.driver.save_screenshot("screenshot.png")


    # Close the browser
    browser.close()
    
if __name__ == "__main__":
    main()