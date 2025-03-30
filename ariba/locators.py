
class Login:
    username:str = "//input[@name='loginfmt']" 
    password:str = "//input[@name='passwd']"
    avancar_button:str = "//input[@value='Avançar' or @value='Next']"
    entrar_button:str = "//input[@value='Entrar' or @value='Sign in']"
    continuar_connectado:str = "//div[text()='Continuar conectado?']"
    sim_button:str = "//input[@value='Sim']"

class Home:
    btn_gerenciar:str = "//a[@_mid='Manage']"
    search_button:str = "//button[@id='_oshrwb']"
    search_field:str = "//input[@id='_2wupab']"
    search_category_menu:str = "//span[@class='a-srch-portlet-category-dropdown']"

class Search:
    body:str = "//div[@class='searchBody']"
    result_message:str = "//div[@class='w-md-msg']"

class Locators:
    go_home_button:str = "//*[@title='Logotipo da empresa']"
    login:Login = Login
    home:Home = Home
    search:Search = Search

locators:Locators = Locators