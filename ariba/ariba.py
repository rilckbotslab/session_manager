from browser import Browser
from .settings import settings
from .locators import Locators
from logger import logger
from selenium.common.exceptions import StaleElementReferenceException

class Ariba(Browser):

    @logger.catch    
    def in_home(self):
        """Check if home element is visible."""
        return self.find_elements(Locators.home.btn_gerenciar, 'visible', wait=False)
    
    @logger.catch
    def search(self, category:str, search_text:str):
        """Search for a sourcing project in Ariba."""        
        while not self.in_home():
            self.click(Locators.go_home_button)
        
        locators_home = Locators.home
        locators_search = Locators.search
        closed_category_menu = f"//div[@id='SearchBarCategoryMenuId'][contains(@class, 'is-dnone')]"
        while self.find_elements(closed_category_menu, wait=False):            
            self.click(locators_home.search_category_menu)
        menu_category_locator = f"//div[@id='SearchBarCategoryMenuId']//a[@role='menuitem' and contains(text(), '{category}')]"
        self.find_element(menu_category_locator, condition='visible')
        self.click(menu_category_locator)
        self.send_text(
            xpath=locators_home.search_field, 
            text=search_text, 
            verify=True
        )
        # Click the search button until it disappears
        while self.find_elements(locators_home.search_button, wait=False):            
            try:
                self.click(locators_home.search_button, max_retries=1)
            except (StaleElementReferenceException, Exception):
                break
        
        # wait for result
        self.find_elements(locators_search.body, condition='visible')
        
        # check if there is an result
        # if there is an result it would have 2 forms inside result_div
        forms = self.find_elements(f"{locators_search.body}//form")
        if len(forms) < 2:            
            message = self.find_element(locators_search.result_message).text
            logger.warning(f"SDC {search_text} - {message}")
            return False
        
        return True

    def handle_unauthorized_request(self):
        # check if "Unauthorized request" in the page        
        while self.find_elements("//body[text()='Unauthorized request']", wait=False):
            logger.error('Unauthorized request')
            self.driver.get(settings.BASE_URL)
            self.driver.back()

    @logger.catch
    def login(self, username: str, password: str) -> None:
        """ Login to Ariba """
        locators = Locators.login
        logger.debug('Logging in to Ariba')

        self.driver.get(settings.LOGIN_URL)      

        self.handle_unauthorized_request()

        if self.find_elements(Locators.home.btn_gerenciar, wait=False):
            logger.debug('Already logged in')
            return

        self.send_text(
            locators.username,
            username
        )
        self.click(locators.avancar_button)
        self.send_text(
            locators.password,
            password
        )
        self.click(locators.entrar_button)

        # Handle "Continuar conectado?" screen
        if self.find_elements(locators.continuar_connectado):            
            logger.debug('Continuar conectado? screen found')
            self.click(locators.sim_button)
        
        # Wait for the home page to load
        self.find_element(
            Locators.home.btn_gerenciar,
            condition='clickable',
            retry=10
            )
        logger.debug('Logged in to Ariba')
