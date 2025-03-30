
from dotenv import load_dotenv
load_dotenv()
import os
from vault import vault
from database import YudqsLogs
from browser import Browser

from ariba import SupplierAward
from ariba.settings import settings

def main():
    # Create a new instance of the browser
    browser = SupplierAward(vnc=True)
    browser.login(
        settings.USERNAME,
        settings.PASSWORD,
    )
    
    # get cookies
    cookies = browser.driver.get_cookies()
    # store cookies
    import json
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)
    
    browser2 = SupplierAward(vnc=True)
    # Load cookies from file
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
    # Add cookies to the browser
    browser2.driver.get(settings.BASE_URL)
    for cookie in cookies:
        browser2.driver.add_cookie(cookie)
    # Navigate to the page
        
    # Navigate to a URL
    browser.driver.get("https://www.google.com/")

    browser.driver.save_screenshot("screenshot.png")

    # Close the browser
    browser.driver.quit()
    
if __name__ == "__main__":
    main()